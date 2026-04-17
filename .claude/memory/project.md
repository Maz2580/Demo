---
name: Australian Turntables trailer
description: 30s Instagram Reel trailer for turntables.com.au — creative spine, status, and levers.
type: project
---

**Client:** Australian Turntables (turntables.com.au · @australianturntables).
Motorised vehicle turntables for premium residential + commercial installs.
Featured on The Block 2023.

**Brief:** 30-second cinematic trailer for Instagram Reels — 1080×1920,
autoplay, dark / premium / cinematic. Rotation is the creative spine.
Screen-recordable in Chrome → imported to CapCut for music + captions.
User brief: *"Must feel like it cost $5,000 to produce."*

**Status (2026-04-17):** Shipped. `trailer.html` is built, images scraped
from the client's site, every scene screenshot-verified at native
1080×1920. Nothing blocks recording.

**Six-scene timeline** (total 30.0s):

| # | t       | Beat                                             |
|---|---------|--------------------------------------------------|
| 1 | 0–4s    | Black → wordmark "Australian / Turntables" + gold rule + "EST. MELBOURNE" kicker |
| 2 | 4–10s   | Hero reveal via expanding circle mask, caption "Rotate. / Don't *reverse*."     |
| 3 | 10–15s  | Schematic dial, 24 tick marks, car silhouette sweeps 0° → 180°                 |
| 4 | 15–22s  | Three gallery plates, Ken-Burns drift, "01/03" counter                         |
| 5 | 22–27s  | Giant "DRIVE OUT." + italic gold "Never back." + hashtag kicker                 |
| 6 | 27–30s  | Outro lockup: wordmark + handle + url + "AS SEEN ON THE BLOCK · 2023"          |

**Visual system:**
- Palette: bg `#07070A` · ink `#F4F0E8` · accent `#C9A961`
- Type: Fraunces (display serif, variable opsz 144) + Inter (UI sans)
- GSAP 3.12.5 from cdnjs (47KB); `expo.inOut` easing default
- Polish: SVG fractal grain w/ `steps(4)` jitter, radial vignette, corner
  cinema-marks, sub-pixel stage "breath", gold progress bar

**Open creative levers Maz may ask about:**
- Accent colour variant (gold / copper / platinum) — single CSS var `--accent`
- Scene 4 plate framing (strips ↔ portrait) — CSS width tweak
- Scene 5 statement copy — plain HTML edit

**Why:** locks the agent's understanding to the creative brief so future
suggestions stay on-concept. Any "let's switch to React" or "let's add video
backgrounds" suggestion violates the single-file / screen-record constraint.

**How to apply:** before recommending changes, confirm they preserve: single
self-contained HTML file, 30.0s runtime, 1080×1920 target, rotation-as-verb
principle.
