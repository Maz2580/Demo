# Recording the AT trailer

The trailer is `trailer.html` — a single self-contained file that autoplays a 30-second animation on load.

Total runtime: **30.0 seconds** (add ~0.5s lead-in black and trailing frame for a comfortable record window).

## Fastest path — Chrome DevTools + built-in recorder

1. Start a local server from this folder:
   ```
   npx serve . -p 3000 --no-clipboard
   ```
2. Open Chrome and navigate to:
   ```
   http://localhost:3000/trailer?exact
   ```
   (The `?exact` flag disables the fit-to-viewport scale so the stage renders at native 1080×1920.)

3. Open DevTools (`Ctrl+Shift+I`), click the device-toolbar icon (`Ctrl+Shift+M`), set **Responsive** dimensions to **1080 × 1920**, DPR 1.

4. Start a screen recording of just the viewport region:
   - **Windows:** `Win+G` → Xbox Game Bar → "Capture" → Record.
   - **OBS Studio:** source → Display Capture or Window Capture → crop to the 1080×1920 stage rectangle.

5. Press `Ctrl+R` to reload the page — the animation restarts. Record for ~31 seconds, then stop.

6. Trim in CapCut to exactly 30s. Layer music + SRT captions on top.

## Dev flags on the URL

| Flag           | Effect                                                                |
|----------------|-----------------------------------------------------------------------|
| `?exact`       | Disable auto-scale. Stage renders at native 1080×1920 pixels.         |
| `?seek=12.5`   | Freeze the timeline at 12.5s — useful for picking poster frames.      |
| `R` key        | Reloads the page (re-runs the trailer). Handy between takes.          |

Combine them with `&`, e.g. `?exact&seek=24`.

## Swapping assets without editing HTML

The trailer reads these filenames:

```
assets/images/hero.jpg        Scene 2 full-bleed hero
assets/images/scene4-1.jpg    Scene 4 gallery plate 1
assets/images/scene4-2.jpg    Scene 4 gallery plate 2
assets/images/scene4-3.jpg    Scene 4 gallery plate 3
```

Drop a new image in with the same name and hard-reload. The scraper that populated these is `scrape_images.py`; re-run it any time to pull fresh assets from turntables.com.au.

## Retinting the accent colour

Edit the first lines inside `<style>` in `trailer.html`:

```css
:root {
  --accent: #C9A961;   /* warm gold — default */
  /* --accent: #B87333;   burnished copper */
  /* --accent: #E5E4E2;   platinum */
}
```

## Copy changes

All on-screen copy sits inside `<section class="scene s*">` blocks in the markup — no JS needed. If you change phrase lengths significantly, the GSAP timeline in `<script>` at the bottom may need per-phrase timing tweaks (search for `duration:` comments).

## Known browser notes

- **Fonts**: `Fraunces` + `Inter` load from Google Fonts CDN. Trailer waits on `document.fonts.ready` before starting — so the first render is always with the correct typography.
- **Grain overlay**: SVG fractal-noise animated with `steps(4)` for subtle micro-jitter.
- **Tab throttling**: If Chrome throttles the tab (e.g. it's not focused during recording), timing will stretch. Keep the recording tab visible/focused.
