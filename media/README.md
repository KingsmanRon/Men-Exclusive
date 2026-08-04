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

Encoded by hand, not by the build script. **Currently live:** a 12s loop cut
from `video/VID2.mp4` (43s–56s), 720×1280, audio stripped, 2.7 MB.

### Why it loops without a jump

The camera is walking, so the first and last frames of any cut are different
and a plain loop would hard-cut. Instead the last second is crossfaded back
over the first second, and the result is reordered so **both** joins land
mid-motion:

```
output = crossfade(tail, head)  +  body
         └─ 1s ─┘                  └─ 11s ─┘
```

Playback reaches the end of `body` and wraps to the start of the crossfade,
which begins on the same frame `body` ended on — continuous. Measured: the
loop join is ~4.5× smoother than an arbitrary cut in the same clip.

### The commands

```bash
# 1. pull the segment out at high quality first
ffmpeg -ss 43 -t 13 -i media/video/VID2.mp4 -an \
       -c:v libx264 -crf 16 -preset slow /tmp/seg.mp4

# 2. crossfade the tail back over the head, scale, encode
FILTER="[0:v]trim=start=0:end=1,setpts=PTS-STARTPTS[head];\
[0:v]trim=start=1:end=12,setpts=PTS-STARTPTS[body];\
[0:v]trim=start=12:end=13,setpts=PTS-STARTPTS[tail];\
[tail][head]blend=all_expr='A*(1-(T/1))+B*(T/1)'[x];\
[x][body]concat=n=2:v=1:a=0,scale=720:1280:flags=lanczos,format=yuv420p[v]"

ffmpeg -i /tmp/seg.mp4 -filter_complex "$FILTER" -map "[v]" -an \
       -c:v libx264 -profile:v high -crf 25 -preset slow \
       -pix_fmt yuv420p -movflags +faststart -r 30 assets/hero/store.mp4

# 3. WebM/VP9 alongside — ~30% smaller on Android
ffmpeg -i assets/hero/store.mp4 -an -c:v libvpx-vp9 -crf 36 -b:v 0 \
       -row-mt 1 -deadline good -cpu-used 2 assets/hero/store.webm

# 4. poster = the video's OWN first frame, so there is no jump on play
ffmpeg -i assets/hero/store.mp4 -frames:v 1 -q:v 3 assets/hero/poster.jpg

# 5. og:image, 1200x630
ffmpeg -ss 6 -i assets/hero/store.mp4 \
       -vf "scale=1200:-1:flags=lanczos,crop=1200:630" -frames:v 1 -q:v 3 \
       assets/hero/og.jpg
```

`-an` is not optional — an audio track on an autoplaying hero video will get
the whole element blocked by the browser. Neither is `-movflags +faststart`,
which moves the index to the front so playback can begin before the file has
finished downloading.

### Known limitation

`VID2.mp4` is **478×850 — a portrait phone clip**. The hero is full-bleed
landscape on desktop, so the video is scaled roughly 3× and looks soft. The
dark veil over it hides most of that, and it looks genuinely good on a phone
where it is close to a 1:1 fit. **A landscape reshoot at 1080p is the single
biggest visual upgrade available to this page.** Shoot it walking slowly, in
landscape, and hold the camera level.

`VID1.mp4` (3.2 MB, also uploaded) is unused so far.
