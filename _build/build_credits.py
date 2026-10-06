"""credits.html from photo_credits.json.  python3 _build/build_credits.py"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from build_articles import BASE, head_for  # noqa: E402

E = lambda s: html.escape(str(s or ""), quote=True)
c = json.load(open(os.path.join(HERE, "photo_credits.json")))
sources = sorted({{"wikimedia": "Wikimedia Commons", "flickr": "Flickr", "rawpixel": "rawpixel", "stocksnap": "StockSnap"}.get(x["source"], x["source"]) for x in c})
rows = "".join(f'<tr><td><img src="{E(x["file"])}" alt="" width="160" height="93" loading="lazy" style="border-radius:8px;width:160px;height:auto"></td>'
               f'<td>{E(x["title"])}</td><td>{E(x["creator"] or "Not named")}</td><td>{E(x["source"])}, {E(x["license"]).upper()}</td>'
               f'<td><a href="{E(x["landing"])}" target="_blank" rel="noopener">Original</a></td></tr>' for x in c)
head = head_for("Photo credits | Beer365", "Sources and licences for the photographs used on the Beer365 website.", BASE + "credits.html", "p-articles p-art", "")
main = f'''<main id="main"><section class="phero"><div class="wrap"><p class="kicker">Credits</p><h1>Photo credits</h1>
<p class="std">Every photograph on this site is public domain (CC0), found through Openverse, from {", ".join(sources[:-1])} and {sources[-1]}. No attribution is required; we credit them anyway. Colours are graded to match the site. Breweries named in a photo's title are where the photo was taken, not Beer365 customers.</p></div></section>
<section><div class="wrap"><div class="scrollx"><table class="deftable"><thead><tr><th>Photo</th><th>Title</th><th>By</th><th>Source and licence</th><th>Link</th></tr></thead><tbody>{rows}</tbody></table></div></div></section></main>'''
open(os.path.join(SITE, "credits.html"), "w").write(head + main + open(os.path.join(HERE, "shell_foot.html")).read())
print("credits.html")
