# Men Exclusive — Website Build Brief

Handover context for continuing work on `index.html`. Read this fully
before editing. It records what is **confirmed fact**, what is **still
unverified**, and what must **never be invented**.

---

## 1. The client

**Men Exclusive** — menswear boutique, Johannesburg CBD, South Africa.
Tagline: **DRESS TO IMPRESS**.

Retail menswear with **in-house tailoring**. They stock suits, shirts, coats
and accessories, then alter to fit on the premises. The shop fit-out is
genuinely upscale — black-green marble, gold-framed panelling, wood floors,
gold chrome mannequin heads.

### Confirmed contact details

| Field | Value |
|---|---|
| Phone / WhatsApp | `+27 63 051 2118` → `https://wa.me/27630512118` |
| Email | `Atmenexclusive4@gmail.com` |
| Facebook | `https://www.facebook.com/Loza20/` |
| Listed domain | `menexclusivesa.co.za` — **unverified, may be parked or dead** |

Because the domain is unverified, `og:url` and `<link rel="canonical">` are
**deliberately absent** from the HTML. A canonical pointing at a hostname that
does not serve the page is worse than no canonical at all. Comments mark both
spots. Add them together with the absolute `og:image` URL.

### ⚠️ Address is UNRESOLVED

- Facebook lists **98 Helen Joseph Street, Johannesburg, 2001**
- A store notice refers to government operations in **Small Street**

These streets intersect in the CBD, so it may be a corner site or the Small
Street Mall precinct. **Do not guess.** Whatever is used must match the Google
Business Profile character-for-character or the map pin drifts and local
ranking suffers. A comment marks the spot in the HTML.

Until it is resolved the Visit panel says "Johannesburg CBD, Gauteng" and
offers to send a pin over WhatsApp, and the JSON-LD `PostalAddress` carries
locality/region/country but **no `streetAddress` and no `postalCode`**. Fill
both places in the same edit.

---

## 2. Confirmed commercial facts

### Pricing (client-supplied, safe to publish)

| Item | Price |
|---|---|
| Double-breasted suit | R2 500 |
| Three-piece suit | R3 000 |
| Winter coat | R1 500 |
| Shirt | R450 |
| Tie | R150 |
| Alterations | Quoted on sight |

**Missing:** single-breasted two-piece suit. Almost certainly the volume
seller — its absence from a price list is conspicuous. A commented-out row
sits ready in the HTML.

### Turnaround (client-supplied)

- **Alterations: 20 minutes to 1 hour**, in-house, while you wait
- **Walk-in fittings: same day**
- **Delivery: up to 5 working days** where sizes are already known

The 20-minute figure is the strongest claim in the business and currently
leads the "creed" band. Competing made-to-measure operations quote in weeks.

### Payment — LIVE AND IMPORTANT

**Card only. Visa and Mastercard. No cash accepted.** In force since
**1 July 2026** — that date is now in the past, so the copy states it as
current policy rather than a coming change. If you are reading this before
1 July 2026, revert the wording to future tense.

A customer travelling into the CBD with cash and being turned away is the most
expensive failure this page can prevent. Stated in the price list, the Visit
panel, the enquiry form, the footer, and `paymentAccepted` in the JSON-LD.

### Premises

They trade from a **legally leased space** and issued a notice reassuring
customers during government operations in the area. Trust in the premises is
an active customer concern, not hypothetical. Stated plainly as fact in the
Visit panel — framed as reassurance, not defence.

---

## 3. Rules — do not break these

1. **Never invent a fact.** Two were caught and removed already: a lay-by
   scheme and a "no fitting fee" promise, both plausible-sounding and both
   false. If it wasn't supplied, don't write it.
2. **Never write "bespoke" or "made to measure."** The rails hold multiples of
   identical garments — this is retail plus alteration. Bespoke means a
   pattern drafted from scratch for one man. Approved language: *fitted*,
   *tailored to you*, *in-house tailoring*, *cut to fit*.
3. **Never fabricate reviews or testimonials.** There is no testimonial
   section for this reason. Add one only when three real, named reviews exist.
4. **Never reproduce Kingsman or any film IP.** The visual register comes from
   English bespoke houses (Savile Row), which is the same source the films
   borrow from. That tradition is fair game; the franchise's marks are not.
5. **Don't guess the address.** See above.
6. **Motion must respect `prefers-reduced-motion`.** Every effect is
   decorative and must switch off cleanly.

---

## 4. Design system

### Palette — sourced from the physical store

The gold-on-black-marble plaque in-store confirms the theme; this is not a
stylistic choice imposed on them.

```css
--noir:#08080A;      /* near-pure black, faintly warm */
--noir-2:#0E0E11;    /* raised surface */
--noir-3:#17171B;    /* borders on dark */
--gold:#C6A45C;      /* gold leaf — matches the plaque */
--gold-hi:#E7D3A1;
--gold-lo:#8A6E33;
--ivory:#EDE8DE;     /* body text */
--ivory-dim:#8B857A; /* secondary text */
```

**Gold discipline is the whole game.** Cheap black-and-gold shimmers —
gradient text, glossy fills, glow. Gold here does three jobs only: hairline
rules, letterspaced caps, and price figures. Never a large fill, never a
gradient, never animated.

The stock is colourful — rust, lilac, camel, olive, navy. Those read expensive
against black and cheap against white. The dark field is load-bearing.

### Typography

| Role | Face | Notes |
|---|---|---|
| Wordmark, labels, buttons | **Montserrat** 500/600/700 | Matches their actual sign — heavy geometric caps, wide tracking |
| Headlines | **Libre Caslon Display** | Caslon, London 1722; echoes the serif on their stationery |
| Body | **Libre Franklin** 200–500 | Stays legible on a dark field where a fine serif would not |

On the physical sign the tagline is tracked roughly **twice** as wide as the
wordmark. Preserved: `.brand b` = `.3em`, `.brand i` = `.6em`.

### Ornament

The **hairline → open diamond → hairline** divider (`.rule`) is lifted
directly from their own printed notices. Reveals via `clip-path` so the
diamond doesn't distort. Use it instead of any plain line.

### Motion doctrine

> Slow, orchestrated, singular. Expensive things do not hurry and do not fidget.

- One easing curve everywhere: `--silk: cubic-bezier(.16,1,.3,1)`
- Durations 1.1s–1.5s. Nothing bounces, pulses or springs.
- **Masked line reveal** (`.line > span`) is the signature — text rises from
  behind an overflow-hidden edge, staggered ~120ms via `--d`. Do the most work
  with this one effect.
- **Overture** on load: emblem draws, wordmark sets, curtains part (~2.6s).
  Dismissed by any click/key/scroll/touch. Dismissal is a CSS animation with
  `forwards`, so it clears itself **even if JavaScript fails**. Never make
  this JS-dependent.
- Hero video drifts over 34s — slow enough to never be consciously noticed.

**Progressive enhancement:** every hidden initial state is scoped under
`html.js`, a class set by a one-line inline script in the head. If JavaScript
fails to run or throws, nothing is ever left invisible.

---

## 5. Architecture

Single file, no build step, no framework. Dependencies: Google Fonts only.

```
index.html                  the site — single file, no build step
CLAUDE.md                   this brief
tools/build-media.py        media pipeline (needs: pip install pillow)
tools/.media-manifest.json  GENERATED — change-detection state, committed
media/                      SOURCE OF TRUTH — raw photos, committed
  README.md                 shooting + upload guide
  _inbox/                   unsorted, deliberately NOT processed
  suits/{double-breasted,three-piece,two-piece}/
  outerwear/winter-coats/
  shirting/{shirts,accessories}/     ties live in accessories, not alone
  complete-look/            fully dressed stands, priced as one figure
  occasions/{weddings-lobola,matric-dance,corporate,winter}/
  store/{shopfront,interior,atelier,signage}/
  brand/                    emblem source files
  video/                    raw store video (encoded by hand, not the script)
assets/                     GENERATED — never edit by hand
  store/      interior.jpg  signage.jpg  atelier.jpg
  looks/      01-overcoat-olive.jpg  02-three-piece-navy-check.jpg
              03-blazer-camel.jpg    04-rail-rust.jpg
  collection/ (empty — category tiles borrow from looks/ for now)
  occasions/  (empty — needs occasion photography)
  hero/       (empty — video + poster)
  brand/      (empty — needs emblem.svg)
```

**No photography has been supplied yet.** Every `assets/` folder is currently
empty. The HTML already references the filenames above so the page completes
itself the moment they land; until then each `<img>` carries
`onerror="this.style.visibility='hidden'"` and sits inside a `.frame`, so a
missing photograph reads as a considered empty plate rather than a broken
image icon. Nothing needs rewiring when the real files arrive.

**Adding photographs:** drop originals in the matching `media/` folder, run
`python3 tools/build-media.py`. It applies EXIF rotation, strips GPS and
device metadata, crops to the tile ratio with an upward focal bias, writes
JPEG + WebP, and prints paste-ready `<img>` markup. Only changed files are
reprocessed. Crop ratios and focal points live in `RULES` at the top of the
script — add a category there when you add a folder. The `.frame--*` aspect
ratios in the stylesheet must stay in step with `RULES`.

**Never hand-edit `assets/`** — it is regenerated and your changes will be
overwritten. Edit the source in `media/` instead.

Section anchors: `#house` `#prices` `#occasions` `#visit` `#enquiry`

### Page order

1. Overture (load sequence)
2. Fixed header — 4 nav items, no dropdowns
3. Hero — video/still, masked headline, WhatsApp CTA
4. **The Creed** — 20 min / same day / five days
5. **The House** — atelier story + dress form
6. **The Collection** — category tiles + full-catalogue links
7. **The Price List** — the signature section
8. Occasions — 4 tiles
9. The Process — three steps
10. **The Complete Look** — whole outfits priced as one figure
11. Visit — address, payment, premises, plaque
12. Enquiry — WhatsApp composer
13. Footer + `ClothingStore` JSON-LD

On narrow screens the four nav items restack into a single tracked row beneath
the wordmark. No dropdown, no overlay, no JavaScript — it simply reflows.

### Why the price list, not a product grid

A boutique with no studio catalogue that builds a product grid ends up with
empty cards — which reads *unfinished*, not exclusive. Prices are set like a
fine-dining menu instead: gold leader dots, figures in the display face, no
images required. Publishing prices plainly is a confidence signal. **Do not
replace this with a shop grid** unless real product photography exists for
every SKU.

### Complete Look pricing

Totals are **honest sums of confirmed prices — no bundle discount is applied**,
because none has been agreed with the client. Do not invent one. If a discount
is agreed, keep the itemised lines and show the bundle figure beneath the sum.

Only garments with confirmed prices get a look card. The camel blazer is held
back because it is a jacket over separate trousers and no standalone blazer
price exists. The three published cards check out:

| Look | Parts | Sum |
|---|---|---|
| The Boardroom | 3 000 + 450 + 150 | **R3 600** |
| The Occasion | 2 500 + 450 + 150 | **R3 100** |
| The Winter Standard | 1 500 + 3 000 + 450 + 150 | **R5 100** |

### Why WhatsApp, not a contact form

The enquiry form composes a WhatsApp message client-side and opens it. No
backend, no form service, no database. **No personal information is ever
stored**, which keeps the site outside POPIA processing obligations entirely.
For a client whose infrastructure is a Gmail address, this is the right trade.
Do not replace it with a form that POSTs anywhere without discussing POPIA
implications first.

---

## 6. Outstanding work

### Blocking

- [ ] **Emblem SVG.** Three placeholders in the HTML (overture, header,
      footer/plaque), each with the exact `<img>` tag to paste in. Request a
      **single flat path SVG** — the mark inverts (gold-on-cream on
      stationery, black-on-gold on the plaque), so one recolourable path beats
      two files. The overture currently draws a plain open diamond, which is
      their own ornament, not an invented logo — replace it, don't ship it.
- [ ] **Store video.** Encode before uploading:
      MP4/H.264, 1920×1080, 10–16s seamless loop, **audio track stripped**,
      under 4 MB. Export WebM/VP9 alongside (~30% smaller on Android).
      Poster is already wired to `assets/store/interior.jpg`. Keep `muted` and
      `playsinline` or iOS refuses to autoplay. Uncomment the `<video>` block
      and delete the `<img class="shot">` beneath it.
- [ ] **Any photography at all.** `assets/` is empty. The four store and looks
      filenames referenced in the HTML are the ones the page expects.

### Content gaps

- [ ] Single-breasted two-piece price (commented row ready)
- [ ] Actual trading hours — currently placeholder Mon–Fri 09:00–18:00,
      Sat 09:00–15:00. Kept **out of the JSON-LD** on purpose so Google does
      not ingest unverified opening times; add
      `openingHoursSpecification` once confirmed.
- [ ] Resolve the address — HTML Visit panel **and** JSON-LD `PostalAddress`
- [ ] Occasion photography — 4 remaining `.slot` placeholders. Needs a groom,
      a matriculant, a corporate fitting, a winter coat. Reusing the mannequin
      crops here would read as padding.
- [ ] Shopfront **exterior** with the street number legible
- [ ] `og:image` — 1200×630, one frame from the video, absolute URL

### Before launch

- [ ] **Google Business Profile first.** For a CBD retailer the Maps pack
      outranks the website. The JSON-LD is already wired to feed it.
- [ ] Gate the overture to once per visit via `sessionStorage` — the block is
      written and commented in the closing script, ready to uncomment. It's a
      real conversion tax and Google measures LCP from page load regardless of
      what covers the screen.
- [ ] Convert JPEGs to WebP (~30% off, no visible difference). The build
      script already emits `.webp` beside every `.jpg`; switch the markup to
      `<picture>` once photographs exist.
- [ ] Confirm turnaround claims with the client before publishing. A published
      promise is the one thing that generates complaints when it slips.
- [ ] Confirm the domain, then add `og:url`, `canonical`, and `url` in JSON-LD.

---

## 7. Working notes

- Verify structure after edits: CSS brace balance, JSON-LD parses, no dangling
  `#` anchors, every `<img>` has `alt`, every `assets/` path resolves.
- `assets/brand/emblem.svg` appears in three references that are **inside HTML
  comments** — these are instructions, not live, and will show as "missing"
  in naive link checks.
- Deploys as static files. Relative paths already work on Vercel as-is.
- **The site file must stay named `index.html`.** A static host serves `/`
  from `index.html` and nothing else. It was briefly called
  `men-exclusive.html`, which built and deployed green while every visitor to
  the root URL got a 404 — the deploy status says nothing about whether
  anything answers `/`. Renaming it is not cosmetic; it takes the site down.
