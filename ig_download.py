"""Download best IG post thumbnails for the AT trailer. Signed URLs expire fast — run immediately after scraping."""
import requests, pathlib, sys

OUT = pathlib.Path(__file__).parent / "assets" / "images" / "ig"
OUT.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
HEAD = {"User-Agent": UA, "Accept": "image/avif,image/webp,image/*,*/*;q=0.8"}

# Top picks from IG grid — URLs harvested via Playwright evaluate
TARGETS = {
    "ig-ferrari-glasshouse.jpg": "https://instagram.fcbr1-1.fna.fbcdn.net/v/t51.71878-15/640416624_1609203850222713_4895791488012141467_n.jpg?stp=dst-jpg_e35_s640x640_sh0.08_tt6&_nc_ht=instagram.fcbr1-1.fna.fbcdn.net&_nc_cat=109&_nc_oc=Q6cZ2gG1VxTqh2ZxGpzoYHR9IZowJ--CifFRzsUGTS1Or1bLd34PlttGswijaYj61EZ2gSs&_nc_ohc=rEjrwNbUn3MQ7kNvwHgqE7c&_nc_gid=4XZ8UyxA3LEnucllv6Zcwg&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_Af3xmuQ1hdBji18AkXiofRwhytemmT_a5MSY3_EkA-hY-w&oe=69E9228A&_nc_sid=8b3546",
    "ig-lambos-garage.jpg": "https://instagram.fcbr1-1.fna.fbcdn.net/v/t51.82787-15/656214741_18421230595120794_7144089250748809148_n.jpg?stp=dst-jpg_e35_p640x640_sh0.08_tt6&_nc_ht=instagram.fcbr1-1.fna.fbcdn.net&_nc_cat=106&_nc_oc=Q6cZ2gG1VxTqh2ZxGpzoYHR9IZowJ--CifFRzsUGTS1Or1bLd34PlttGswijaYj61EZ2gSs&_nc_ohc=Dgi6V3D4OogQ7kNvwHIO24J&_nc_gid=4XZ8UyxA3LEnucllv6Zcwg&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_Af0AxUa0fHX_snyq8zI2MN1hCfhpiTSRn7cUWjm_TeAc8g&oe=69E8FF4B&_nc_sid=8b3546",
    "ig-gold-showroom.jpg": "https://instagram.fcbr1-1.fna.fbcdn.net/v/t51.82787-15/635735592_18412761589120794_2704449710017732190_n.jpg?stp=dst-jpg_e35_p640x640_sh0.08_tt6&_nc_ht=instagram.fcbr1-1.fna.fbcdn.net&_nc_cat=106&_nc_oc=Q6cZ2gG1VxTqh2ZxGpzoYHR9IZowJ--CifFRzsUGTS1Or1bLd34PlttGswijaYj61EZ2gSs&_nc_ohc=KpWECoZ4o4IQ7kNvwHPn9nt&_nc_gid=4XZ8UyxA3LEnucllv6Zcwg&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_Af3iptjA9Kk6Ox5aqYyqvudriUayTzIUjx9eK8QRn8S1tw&oe=69E900F7&_nc_sid=8b3546",
    "ig-racecar-building.jpg": "https://instagram.fcbr1-1.fna.fbcdn.net/v/t39.30808-6/492998976_1254276130034719_775000756690402862_n.jpg?stp=dst-jpg_e35_s640x640_sh0.08_tt6&_nc_ht=instagram.fcbr1-1.fna.fbcdn.net&_nc_cat=107&_nc_oc=Q6cZ2gG1VxTqh2ZxGpzoYHR9IZowJ--CifFRzsUGTS1Or1bLd34PlttGswijaYj61EZ2gSs&_nc_ohc=eJRBL3SKNjkQ7kNvwG7Wsq5&_nc_gid=4XZ8UyxA3LEnucllv6Zcwg&edm=AOQ1c0wAAAAA&ccb=7-5&oh=00_Af1AV_f0OmAxvGYRar6-6dFh8g4a15GV10VUHSGPLB7zig&oe=69E90457&_nc_sid=8b3546",
    "ig-porsche-spinsy.jpg": "https://instagram.fcbr1-1.fna.fbcdn.net/v/t51.71878-15/626538679_1468341634714809_7081113657482687834_n.jpg?stp=dst-jpg_e15_tt6&_nc_ht=instagram.fcbr1-1.fna.fbcdn.net&_nc_cat=109&_nc_oc=Q6cZ2gG1VxTqh2ZxGpzoYHR9IZowJ--CifFRzsUGTS1Or1bLd34PlttGswijaYj61EZ2gSs&_nc_ohc=QV2Dx8dk108Q7kNvwFpm9jE&_nc_gid=4XZ8UyxA3LEnucllv6Zcwg&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_Af0SYzN5yPfUhC8Bw0p5fu0T3kEpOMp3mmYb4MNnw3cVBA&oe=69E8FAC4&_nc_sid=8b3546",
    "ig-vintage-red.jpg": "https://instagram.fcbr1-1.fna.fbcdn.net/v/t51.82787-15/620413094_18406508995120794_4096739458383238102_n.jpg?stp=dst-jpg_e35_p640x640_sh0.08_tt6&_nc_ht=instagram.fcbr1-1.fna.fbcdn.net&_nc_cat=106&_nc_oc=Q6cZ2gG1VxTqh2ZxGpzoYHR9IZowJ--CifFRzsUGTS1Or1bLd34PlttGswijaYj61EZ2gSs&_nc_ohc=5Uq9RziFbdUQ7kNvwGT0Y2x&_nc_gid=4XZ8UyxA3LEnucllv6Zcwg&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_Af0nwjeO6lf5l0ZRgLAK-no9zi6cAQ_qLFIW-8SHDYS23A&oe=69E9241D&_nc_sid=8b3546",
}

ok, fail = 0, 0
for name, url in TARGETS.items():
    dest = OUT / name
    try:
        r = requests.get(url, headers=HEAD, timeout=30)
        if r.status_code == 200 and len(r.content) > 20_000:
            dest.write_bytes(r.content)
            print(f"  OK  {name:<28} {len(r.content):>8,} B")
            ok += 1
        else:
            print(f"  FAIL {name:<28} status={r.status_code} size={len(r.content)}")
            fail += 1
    except Exception as e:
        print(f"  ERR  {name:<28} {type(e).__name__}: {e}")
        fail += 1

print(f"\n{ok} ok / {fail} failed")
sys.exit(0 if ok else 1)
