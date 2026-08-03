# media/ — source of truth

Raw photographs live here and are **committed**. Everything under `assets/` is
generated from this folder and can be thrown away and rebuilt at any time.

```
python3 tools/build-media.py      # needs: pip install pillow
```

The script applies EXIF rotation, **strips GPS and device metadata**, crops to
the tile ratio with an upward focal bias, writes JPEG + WebP, and prints
paste-ready `<img>` markup. Only changed files are reprocessed.

> **Never hand-edit `assets/`.** It is regenerated and your changes will be
> overwritten. Edit the source here instead.

---

## Where things go

| Folder | Goes to | Shot as |
|---|---|---|
| `suits/double-breasted/` `suits/three-piece/` `suits/two-piece/` | `assets/looks/` | 3:4 portrait |
| `outerwear/winter-coats/` | `assets/looks/` | 3:4 portrait |
| `shirting/shirts/` `shirting/accessories/` | `assets/looks/` | 3:4 portrait |
| `complete-look/` | `assets/looks/` | 4:3 |
| `occasions/{weddings-lobola,matric-dance,corporate,winter}/` | `assets/occasions/` | 3:4 portrait |
| `store/{shopfront,interior,atelier,signage}/` | `assets/store/` | varies — see `RULES` |
| `brand/` | `assets/brand/` | 1:1 |
| `video/` | **not processed** — encoded by hand | — |
| `_inbox/` | **not processed** — unsorted pile | — |

Ties live in `shirting/accessories/`, not in a folder of their own.

Adding a new folder means adding a rule to `RULES` at the top of
`tools/build-media.py`. A photograph in a folder with no rule is reported and
skipped — the script never guesses a crop.

---

## Shooting guide

**Light.** Shoot in the shop, not outside. The fit-out — black-green marble,
gold-framed panelling, wood floors — is the reason the site looks the way it
does. Daylight from the shopfront on one side, nothing bounced back. Do not use
the on-camera flash; it flattens the panelling and turns the gold grey.

**Background.** Dark. The stock is rust, lilac, camel, olive and navy, and
those colours read expensive against black and cheap against white. Never shoot
a garment against a white wall.

**Framing.** Leave headroom and space at the sides. The script crops to a fixed
ratio and it can only ever cut *in* — a tight frame cannot be rescued. Crops are
biased **upward** so lapels, collars and knots survive; the bottom of the frame
is what gets sacrificed.

**Orientation.** Portrait for garments. Landscape for the room and the
shopfront.

**Resolution.** Straight off the phone is fine — bigger is better, the script
resizes down. Do not pre-crop, do not pre-compress, do not apply a filter.

**Steady.** No motion blur. Brace against a rail if you have to.

### What is still needed

- [ ] **Shopfront exterior with the street number legible** — this is the one
      photograph that resolves the address question visually.
- [ ] **Occasions**, four shots: a groom, a matriculant, a corporate fitting,
      a winter coat. Reusing mannequin crops here reads as padding.
- [ ] **Store video** — 10–16s of the shop floor. See CLAUDE.md for encoding.

### Privacy

If a customer is recognisable in a shot, get their say-so before it goes up.
The script removes GPS coordinates from the file, but it cannot remove a face.

---

## Store video

Encoded by hand, not by this script. Drop the raw clip in `video/` and export:

- MP4 / H.264, 1920×1080, 10–16s seamless loop, **audio track stripped**,
  under 4 MB
- WebM / VP9 alongside (~30% smaller on Android)

Output goes to `assets/hero/store.mp4` and `assets/hero/store.webm`.
