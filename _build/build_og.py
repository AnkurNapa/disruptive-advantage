"""One Open Graph image per page (og/<page>.jpg, 1200 x 630) plus the og:image and
twitter:image tags on every page. Run last, after every other builder.

  python3 _build/build_og.py
"""
import base64
import glob
import html
import json
import os
import re

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
BASE = "https://ankurnapa.github.io/disruptive-advantage/"
E = lambda s: html.escape(str(s), quote=True)

AREA_OF = json.load(open(os.path.join(HERE, "article_photos.json")))  # written by build_articles.py
PAGE_PHOTO = {"index.html": "brewhouse", "use-cases.html": "cellar", "solutions.html": "brewhouse", "features.html": "cellar",
              "roi.html": "brewhouse", "pricing.html": "business", "about.html": "business", "careers.html": "business",
              "contact.html": "layer", "case-studies.html": "brewhouse", "case-study-extract-loss.html": "brewhouse",
              "articles.html": "raw", "resources.html": "business", "credits.html": "raw",
              "article-brewhouse-efficiency.html": "brewhouse"}
KICK = {"index.html": "Beer intelligence for the whole beer business"}


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


LOGO = data_uri(os.path.join(SITE, "assets", "beer365-logo-light.svg"), "image/svg+xml")


def card(title, kicker, photo):
    img = data_uri(os.path.join(SITE, "assets", "photos", f"{photo}.jpg"), "image/jpeg")
    size = 64 if len(title) < 50 else 54 if len(title) < 75 else 46
    return f'''<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@600;800&display=swap"><style>
*{{margin:0;box-sizing:border-box}} body{{width:1200px;height:630px;font-family:Inter,sans-serif;background:#000;color:#fff;position:relative;overflow:hidden}}
.ph{{position:absolute;inset:0;background:linear-gradient(95deg,#000 0%,rgba(0,0,0,.92) 48%,rgba(0,0,0,.35) 100%),url({img}) right center/cover}}
.in{{position:absolute;inset:0;padding:64px 72px;display:flex;flex-direction:column}}
.logo{{height:52px;width:auto;align-self:flex-start}}
.k{{margin-top:auto;font-size:24px;font-weight:600;color:#F5E003}}
h1{{margin-top:16px;font-size:{size}px;line-height:1.08;font-weight:800;letter-spacing:-.035em;max-width:880px}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:12px;background:#F5E003}}
</style></head><body><div class="ph"></div><div class="in"><img class="logo" src="{LOGO}"><p class="k">{E(kicker)}</p><h1>{E(title)}</h1></div><div class="bar"></div></body></html>'''


def page_title(h):
    m = re.search(r'property="og:title"[^>]*content="([^"]*)"|content="([^"]*)"[^>]*property="og:title"', h)
    t = html.unescape((m.group(1) or m.group(2)) if m else re.search(r"<title>(.*?)</title>", h, re.S).group(1))
    return re.sub(r"\s*\|\s*Beer365\s*$", "", t).strip()


def kicker_for(name):
    if name in KICK:
        return KICK[name]
    if name.startswith("article-"):
        return "Beer365 article by Ankur Napa"
    if name.startswith("whitepaper-"):
        return "Beer365 white paper"
    return "Beer365"


def set_meta(h, url):
    h = re.sub(r'\s*<meta[^>]*(?:property="og:image(?::\w+)?"|name="twitter:image")[^>]*/?>', "", h)
    tags = (f'<meta content="{url}" property="og:image"/><meta content="1200" property="og:image:width"/>'
            f'<meta content="630" property="og:image:height"/><meta content="{url}" name="twitter:image"/>')
    return h.replace("</head>", tags + "\n</head>", 1)


def main():
    os.makedirs(os.path.join(SITE, "og"), exist_ok=True)
    pages = [p for p in sorted(glob.glob(os.path.join(SITE, "*.html"))) if 'http-equiv="refresh"' not in open(p).read()]
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for p in pages:
            name = os.path.basename(p)
            h = open(p).read()
            photo = AREA_OF.get(name) or PAGE_PHOTO.get(name) or ("business" if name.startswith("whitepaper-") else "brewhouse")
            pg.set_content(card(page_title(h), kicker_for(name), photo), wait_until="networkidle")
            out = os.path.join(SITE, "og", name.replace(".html", ".jpg"))
            pg.screenshot(path=out, type="jpeg", quality=82)
            open(p, "w").write(set_meta(h, BASE + "og/" + os.path.basename(out)))
        b.close()
    print(len(pages), "OG images")


if __name__ == "__main__":
    main()
