"""Strip the bottom-right AI watermark diamond from generated PNGs and promote
them to named JPG slots in assets/images/.

Strategy: the diamond sits ~40-60px inset from the bottom-right corner. Cropping
a horizontal strip ~100px tall from the bottom then resizing back to 1080x1920
cleanly removes it and keeps the car/composition intact (the subject is
centre-to-upper-third in every prompt we used)."""
from pathlib import Path
from PIL import Image

SRC = Path("C:/DEMO/generated_images")
DEST = Path("C:/DEMO/Demo/assets/images")
DEST.mkdir(parents=True, exist_ok=True)

# source filename → destination slot name
MAP = {
    "start.png":    "start.jpg",
    "hero.png":     "hero.jpg",
    "scene4-1.png": "scene4-1.jpg",
    "end.png":      "end.jpg",
}

CROP_BOTTOM_PX = 110    # strips the diamond clean
TARGET_SIZE    = (1080, 1920)
JPG_QUALITY    = 92

for src_name, dest_name in MAP.items():
    src  = SRC / src_name
    dest = DEST / dest_name
    img  = Image.open(src).convert("RGB")
    w, h = img.size

    # crop watermark strip from bottom, keep full width
    cropped = img.crop((0, 0, w, h - CROP_BOTTOM_PX))
    # resize to canonical 1080x1920 for consistent trailer composition
    final = cropped.resize(TARGET_SIZE, Image.LANCZOS)
    final.save(dest, "JPEG", quality=JPG_QUALITY, optimize=True)
    print(f"  {src_name:<15} -> {dest_name:<14}  "
          f"{w}x{h} -> {TARGET_SIZE[0]}x{TARGET_SIZE[1]}  "
          f"{dest.stat().st_size / 1024:.0f}KB")
