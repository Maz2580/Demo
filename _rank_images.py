"""Re-rank scraped images by pixel count + aspect ratio, assign best to slots."""
from pathlib import Path
from PIL import Image
import shutil, json

root = Path(__file__).parent / "assets" / "images"
scraped = root / "scraped"

info = []
for p in scraped.iterdir():
    try:
        with Image.open(p) as im:
            info.append({"path": p, "w": im.size[0], "h": im.size[1], "bytes": p.stat().st_size})
    except Exception:
        continue

info.sort(key=lambda x: -(x["w"] * x["h"]))
print("Top 15 by resolution:")
for i, x in enumerate(info[:15], 1):
    ar = x["w"] / x["h"]
    shape = "landscape" if ar > 1.2 else ("portrait" if ar < 0.9 else "square ")
    print(f"  {i:2}. {x['w']:>5}x{x['h']:<5} ar={ar:4.2f} {shape} {x['bytes']/1024:>6.0f}KB  {x['path'].name}")

# Pick best: hero = largest landscape, scene4 slots = next 3 distinct, detail = square-ish
landscapes = [x for x in info if 1.2 < (x["w"] / x["h"]) < 2.4 and x["w"] >= 1200]
portraits = [x for x in info if (x["w"] / x["h"]) < 0.9 and x["h"] >= 1200]
squareish = [x for x in info if 0.9 <= (x["w"] / x["h"]) <= 1.2 and x["w"] >= 800]

print(f"\nlandscapes: {len(landscapes)}, portraits: {len(portraits)}, squareish: {len(squareish)}")

picks = {}
used = set()

def pick(pool, key):
    for x in pool:
        if x["path"].name not in used:
            used.add(x["path"].name)
            picks[key] = x
            return x
    return None

pick(landscapes, "hero")
pick(landscapes, "scene4-1")
pick(landscapes, "scene4-2")
pick(landscapes, "scene4-3")
pick(squareish or landscapes, "detail")

for slot, x in picks.items():
    if x is None:
        continue
    dst = root / f"{slot}.jpg"
    # ensure jpg; convert if png
    with Image.open(x["path"]) as im:
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im.save(dst, "JPEG", quality=88, optimize=True)
    print(f"  {slot:<12} <- {x['path'].name} ({x['w']}x{x['h']})")

(root / "manifest.json").write_text(json.dumps(
    {slot: {"src": x["path"].name, "w": x["w"], "h": x["h"]} for slot, x in picks.items() if x},
    indent=2,
))
