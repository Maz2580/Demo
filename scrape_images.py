"""
Scrape product images from turntables.com.au for the AT trailer.

Strategy:
- Fetch a handful of known-useful pages.
- Extract <img> tags + srcset, resolve to absolute URLs.
- Prefer full-resolution versions (last entry in srcset).
- Filter out obvious UI (icons/logos/svg/menus).
- Download to assets/images/scraped/, dedupe by filename.
- Rank by filesize and promote top N to friendly names used by trailer.html.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
OUT = ROOT / "assets" / "images"
SCRAPED = OUT / "scraped"
OUT.mkdir(parents=True, exist_ok=True)
SCRAPED.mkdir(parents=True, exist_ok=True)

BASE = "https://www.turntables.com.au"
PAGES = [
    "/",
    "/gallery/",
    "/products/",
    "/car-turntables/",
    "/how-it-works/",
    "/residential/",
    "/commercial/",
]
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)
HEAD = {"User-Agent": UA, "Accept": "*/*"}

SKIP = re.compile(
    r"(icon|logo-|favicon|sprite|emoji|avatar|menu|placeholder|loading|arrow)",
    re.I,
)


def largest_from_srcset(srcset: str) -> str | None:
    """Return the URL with the highest width descriptor in srcset."""
    best = None
    best_w = -1
    for part in srcset.split(","):
        bits = part.strip().split()
        if len(bits) < 2:
            continue
        url, w = bits[0], bits[1]
        try:
            w_int = int(re.sub(r"\D", "", w))
        except ValueError:
            continue
        if w_int > best_w:
            best_w = w_int
            best = url
    return best


def collect_image_urls() -> set[str]:
    urls: set[str] = set()
    for path in PAGES:
        url = BASE + path
        try:
            r = requests.get(url, headers=HEAD, timeout=30)
        except Exception as e:
            print(f"  skip {path}: {type(e).__name__}: {e}")
            continue
        if r.status_code != 200:
            print(f"  skip {path}: HTTP {r.status_code}")
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        page_urls: set[str] = set()
        for img in soup.find_all("img"):
            src = (
                img.get("data-src")
                or img.get("data-lazy-src")
                or img.get("src")
                or ""
            )
            srcset = img.get("srcset") or img.get("data-srcset")
            if srcset:
                bigger = largest_from_srcset(srcset)
                if bigger:
                    src = bigger
            if not src:
                continue
            if src.startswith("data:"):
                continue
            if "wp-content/uploads" not in src and "/uploads/" not in src:
                continue
            abs_url = urljoin(BASE, src)
            page_urls.add(abs_url)
        print(f"  {path}: found {len(page_urls)} candidate imgs")
        urls |= page_urls
    return urls


def download(url: str) -> tuple[Path, int] | None:
    name = url.rsplit("/", 1)[-1].split("?")[0]
    if SKIP.search(name) or name.endswith(".svg"):
        return None
    dest = SCRAPED / name
    if dest.exists() and dest.stat().st_size > 0:
        return dest, dest.stat().st_size
    try:
        r = requests.get(url, headers=HEAD, timeout=45)
    except Exception as e:
        print(f"  fail {name}: {type(e).__name__}")
        return None
    if r.status_code != 200 or len(r.content) < 40_000:
        return None
    dest.write_bytes(r.content)
    return dest, len(r.content)


def main() -> int:
    print(f"scraping {BASE} ...")
    urls = collect_image_urls()
    print(f"total unique candidate URLs: {len(urls)}")

    results: list[tuple[Path, int]] = []
    for u in urls:
        hit = download(u)
        if hit:
            results.append(hit)
    print(f"downloaded {len(results)} images to {SCRAPED}")

    # Rank by filesize (proxy for resolution/quality).
    results.sort(key=lambda x: -x[1])

    # Promote top images to deterministic names the trailer uses.
    # hero, scene4-1, scene4-2, scene4-3, detail.
    slots = ["hero.jpg", "scene4-1.jpg", "scene4-2.jpg", "scene4-3.jpg", "detail.jpg"]
    assigned: list[dict] = []
    for slot, (path, size) in zip(slots, results):
        dest = OUT / slot
        shutil.copy2(path, dest)
        assigned.append({"slot": slot, "src": path.name, "bytes": size})
        print(f"  {slot:<14} <- {path.name} ({size:,}B)")

    (OUT / "manifest.json").write_text(
        json.dumps(
            {
                "scraped_total": len(results),
                "assigned": assigned,
                "all_scraped": [{"file": p.name, "bytes": s} for p, s in results],
            },
            indent=2,
        )
    )
    return 0 if assigned else 1


if __name__ == "__main__":
    sys.exit(main())
