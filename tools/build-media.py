#!/usr/bin/env python3
"""
build-media.py — Men Exclusive media pipeline

    pip install pillow
    python3 tools/build-media.py

Reads originals from media/, writes web-ready derivatives to assets/.

For every source photograph it:
  1. applies the EXIF orientation tag and then discards it (no sideways phones)
  2. strips ALL metadata — GPS coordinates, device model, serial numbers
  3. crops to the tile ratio for that category, biased UPWARD so heads,
     collars and lapels survive the crop instead of chins and belts
  4. writes a JPEG and a WebP at the same stem
  5. prints paste-ready <img> markup with real width/height attributes

Only changed files are reprocessed. Change detection is a content hash of
the source plus the rule that produced it, so editing RULES below correctly
invalidates every affected output.

NEVER hand-edit anything under assets/ — this script overwrites it. Edit the
source in media/ instead.

media/_inbox/ is deliberately NOT processed. It is the unsorted pile; move
photographs into a real category folder before they become part of the site.
media/video/ is skipped too — store video is encoded by hand (see CLAUDE.md).
"""

import hashlib
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is not installed.  Run:  pip install pillow")


ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "media"
ASSETS = ROOT / "assets"
MANIFEST = ROOT / "tools" / ".media-manifest.json"

JPEG_QUALITY = 82
WEBP_QUALITY = 80


# ─────────────────────────────────────────────────────────────────────────────
# RULES
#
# Keyed by path under media/, longest prefix wins.
#
#   out    — destination folder under assets/
#   ratio  — (w, h) the tile is displayed at; the crop matches it exactly
#   focus  — vertical anchor, 0.0 = top edge, 0.5 = dead centre, 1.0 = bottom.
#            Everything here sits ABOVE centre because garments are worn on
#            the top half of a body and a centred crop beheads the subject.
#   width  — output width in pixels; height follows from ratio
#
# Adding a folder to media/ means adding a rule here. A source under a folder
# with no rule is reported and skipped, never guessed at.
# ─────────────────────────────────────────────────────────────────────────────

RULES = {
    "store/interior":            {"out": "store",      "ratio": (16, 9), "focus": 0.45, "width": 1920},
    "store/shopfront":           {"out": "store",      "ratio": (4, 3),  "focus": 0.42, "width": 1600},
    "store/atelier":             {"out": "store",      "ratio": (2, 3),  "focus": 0.40, "width": 1200},
    "store/signage":             {"out": "store",      "ratio": (4, 3),  "focus": 0.44, "width": 1600},

    "suits":                     {"out": "looks",      "ratio": (3, 4),  "focus": 0.36, "width": 1200},
    "outerwear":                 {"out": "looks",      "ratio": (3, 4),  "focus": 0.36, "width": 1200},
    "shirting":                  {"out": "looks",      "ratio": (3, 4),  "focus": 0.34, "width": 1200},

    "complete-look":             {"out": "looks",      "ratio": (4, 3),  "focus": 0.38, "width": 1600},

    "occasions":                 {"out": "occasions",  "ratio": (3, 4),  "focus": 0.34, "width": 1200},

    "brand":                     {"out": "brand",      "ratio": (1, 1),  "focus": 0.50, "width": 800},
}

# Never walked.
SKIP_DIRS = {"_inbox", "video"}

SOURCE_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".heic", ".heif"}

# Frame classes in men-exclusive.html, so the printed markup drops straight in.
FRAME_CLASS = {
    (3, 4):  "frame--portrait",
    (2, 3):  "frame--tall",
    (4, 3):  "frame--wide",
    (16, 9): "frame--hero",
    (1, 1):  "frame--square",
}


def rule_for(rel: Path):
    """Longest matching prefix under media/ wins."""
    parts = rel.parts[:-1]
    for depth in range(len(parts), 0, -1):
        key = "/".join(parts[:depth])
        if key in RULES:
            return key, RULES[key]
    return None, None


def slug(text: str) -> str:
    keep = [c.lower() if c.isalnum() else "-" for c in text]
    out = "".join(keep)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-") or "image"


def signature(path: Path, rule: dict) -> str:
    h = hashlib.sha1()
    h.update(json.dumps(rule, sort_keys=True).encode())
    h.update(f"{JPEG_QUALITY}/{WEBP_QUALITY}".encode())
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def crop_to(img: Image.Image, ratio, focus: float) -> Image.Image:
    """Centre horizontally, anchor vertically on `focus`."""
    rw, rh = ratio
    target = rw / rh
    w, h = img.size
    current = w / h

    if abs(current - target) < 1e-6:
        return img

    if current > target:
        # Too wide — trim the sides, keep the middle.
        new_w = int(round(h * target))
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))

    # Too tall — trim top and bottom, biased upward.
    new_h = int(round(w / target))
    top = int(round((h - new_h) * focus))
    top = max(0, min(top, h - new_h))
    return img.crop((0, top, w, top + new_h))


def process(src: Path, rel: Path, rule: dict):
    with Image.open(src) as im:
        # 1. Honour the orientation tag, then drop it. exif_transpose returns a
        #    copy with no orientation key, so the pixels are already upright.
        im = ImageOps.exif_transpose(im)

        # 2. Flatten transparency onto the page black rather than white — a
        #    white halo on this site is instantly visible.
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            ground = Image.new("RGBA", im.size, (8, 8, 10, 255))
            im = Image.alpha_composite(ground, im).convert("RGB")
        elif im.mode != "RGB":
            im = im.convert("RGB")

        im = crop_to(im, rule["ratio"], rule["focus"])

        rw, rh = rule["ratio"]
        out_w = min(rule["width"], im.width)
        out_h = int(round(out_w * rh / rw))
        if (out_w, out_h) != im.size:
            im = im.resize((out_w, out_h), Image.LANCZOS)

        dest_dir = ASSETS / rule["out"]
        dest_dir.mkdir(parents=True, exist_ok=True)
        stem = slug(src.stem)

        jpg = dest_dir / f"{stem}.jpg"
        webp = dest_dir / f"{stem}.webp"

        # 3. Saving without passing exif/icc_profile is what strips GPS,
        #    device model and serial numbers. Do not "helpfully" pass them on.
        im.save(jpg, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        im.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)

    return {
        "jpg": jpg.relative_to(ROOT).as_posix(),
        "webp": webp.relative_to(ROOT).as_posix(),
        "w": out_w,
        "h": out_h,
        "ratio": tuple(rule["ratio"]),
        "src": rel.as_posix(),
    }


def markup(rec) -> str:
    cls = FRAME_CLASS.get(tuple(rec["ratio"]), "frame")
    label = Path(rec["src"]).parent.name.replace("-", " ").title()
    return (
        f'<div class="frame {cls}" data-label="{label}">\n'
        f'  <img src="{rec["jpg"]}" width="{rec["w"]}" height="{rec["h"]}"\n'
        f'       alt="TODO describe this photograph" loading="lazy"\n'
        f'       onerror="this.style.visibility=\'hidden\'">\n'
        f'</div>'
    )


def main():
    if not MEDIA.exists():
        sys.exit(f"No media/ folder at {MEDIA}")

    try:
        manifest = json.loads(MANIFEST.read_text())
    except (OSError, ValueError):
        manifest = {}

    built, skipped, unruled, seen = [], 0, [], set()

    for src in sorted(MEDIA.rglob("*")):
        if not src.is_file() or src.suffix.lower() not in SOURCE_EXT:
            continue

        rel = src.relative_to(MEDIA)
        if SKIP_DIRS & set(rel.parts):
            continue

        key, rule = rule_for(rel)
        if rule is None:
            unruled.append(rel.as_posix())
            continue

        seen.add(rel.as_posix())
        sig = signature(src, rule)
        prev = manifest.get(rel.as_posix())

        if prev and prev.get("sig") == sig and all(
            (ROOT / prev[k]).exists() for k in ("jpg", "webp")
        ):
            skipped += 1
            continue

        try:
            rec = process(src, rel, rule)
        except Exception as exc:                      # one bad file must not
            print(f"  !! {rel}  —  {exc}")            # stop the whole run
            continue

        rec["sig"] = sig
        manifest[rel.as_posix()] = rec
        built.append(rec)

    # Forget sources that no longer exist. Their outputs are left on disk —
    # deleting generated files a page might still reference is not this
    # script's call to make.
    for gone in [k for k in manifest if k not in seen]:
        manifest.pop(gone)

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print(f"\n  built {len(built)}   unchanged {skipped}\n")

    if unruled:
        print("  No RULES entry — skipped, not guessed at:")
        for u in unruled:
            print(f"    {u}")
        print("  Add the folder to RULES at the top of this script.\n")

    if built:
        print("  ── paste-ready markup " + "─" * 46 + "\n")
        for rec in built:
            print(f"  /* {rec['src']} */")
            for ln in markup(rec).splitlines():
                print(f"  {ln}")
            print()


if __name__ == "__main__":
    main()
