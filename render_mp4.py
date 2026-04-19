"""
Deterministic MP4 export for trailer.html.

Pipeline:
  1. Launch headless Chromium at 1080x1920
  2. For each frame in [0, 34s * fps):
       navigate to ?exact&seek=N (timeline freezes at that time)
       wait a beat for GSAP to settle
       capture PNG to frames/########.png
  3. ffmpeg stitches the PNG sequence into trailer.mp4 (H.264, CRF 18)

Assumes:
  - Local server running on http://localhost:3000
  - ffmpeg on PATH
  - playwright[chromium] installed in the active Python env
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT     = Path(__file__).parent
FRAMES   = ROOT / "frames"
OUT_MP4  = ROOT / "trailer.mp4"
URL_BASE = "http://localhost:3000/trailer.html"

FPS        = 30
DURATION_S = 37.9
WIDTH, HEIGHT = 1080, 1920
TOTAL_FRAMES  = int(FPS * DURATION_S)


def render_frames() -> None:
    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)

    print(f"rendering {TOTAL_FRAMES} frames at {WIDTH}x{HEIGHT}@{FPS}fps "
          f"({DURATION_S}s)")

    t0 = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=1,
        )
        page = ctx.new_page()

        # navigate ONCE — fonts, images, GSAP timeline prime here
        page.goto(f"{URL_BASE}?exact&seek=0", wait_until="networkidle")
        page.wait_for_function("window.__trailerReady === true", timeout=30_000)
        page.evaluate("() => { window.__tl.pause(); }")

        # Canvas + ImageBitmap: onUpdate's ctx.drawImage lands pixels
        # synchronously in the canvas backing buffer. One RAF for the
        # compositor to pick it up and we're good.
        seek_and_wait = """
        async (t) => {
          window.__tl.seek(t, false);
          await new Promise(r => requestAnimationFrame(() =>
                               requestAnimationFrame(r)));
        }
        """

        for i in range(TOTAL_FRAMES):
            t = i / FPS
            page.evaluate(seek_and_wait, t)
            out = FRAMES / f"{i:08d}.png"
            page.screenshot(path=str(out), full_page=False, type="png")

            if i % 30 == 0 or i == TOTAL_FRAMES - 1:
                elapsed = time.time() - t0
                rate    = (i + 1) / elapsed
                eta     = (TOTAL_FRAMES - i - 1) / max(rate, 0.01)
                print(f"  frame {i+1:4d}/{TOTAL_FRAMES}  "
                      f"t={t:5.2f}s  {rate:4.1f} fps  ETA {eta:5.1f}s")

        browser.close()

    print(f"rendered in {time.time() - t0:.1f}s")


def stitch_mp4() -> None:
    print("stitching with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i",         str(FRAMES / "%08d.png"),
        "-c:v",       "libx264",
        "-pix_fmt",   "yuv420p",
        "-crf",       "18",
        "-preset",    "slow",
        "-movflags",  "+faststart",
        str(OUT_MP4),
    ]
    subprocess.run(cmd, check=True)

    size_mb = OUT_MP4.stat().st_size / (1024 * 1024)
    print(f"wrote {OUT_MP4.name} ({size_mb:.1f} MB)")


def main() -> int:
    render_frames()
    stitch_mp4()
    return 0


if __name__ == "__main__":
    sys.exit(main())
