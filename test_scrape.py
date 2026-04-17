import os
import sys
from pathlib import Path

import requests
from PIL import Image

OUT = Path(__file__).parent / "assets" / "images" / "test.jpg"
OUT.parent.mkdir(parents=True, exist_ok=True)

URLS = [
    "https://www.turntables.com.au/wp-content/uploads/CTX48-PR-hero.jpg",
    "https://picsum.photos/800/600",
]


def download(url: str) -> bool:
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200 and len(r.content) > 1000:
            OUT.write_bytes(r.content)
            return True
    except Exception as e:
        print(f"  failed {url}: {e}")
    return False


ok = False
for u in URLS:
    print(f"Trying: {u}")
    if download(u):
        ok = True
        break

if not ok:
    print("IMAGE SCRAPING FAILED")
    sys.exit(1)

size = OUT.stat().st_size
print(f"Saved: {OUT} ({size} bytes)")
with Image.open(OUT) as img:
    print(f"Valid image: {img.format} {img.size}")
print("IMAGE SCRAPING READY")
