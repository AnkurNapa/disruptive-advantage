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
LICENCE = {"cc0": "CC0", "cc by 2.0": "CC BY 2.0", "mixkit free license": "Mixkit free licence"}
SOURCE = {"wikimedia": "Wikimedia Commons", "pxhere": "pxhere", "mixkit": "Mixkit"}
rows = "".join(f'<tr><td><img src="{E(x["file"])}" alt="" width="160" height="93" loading="lazy" style="border-radius:8px;width:160px;height:auto"></td>'
               f'<td>{E(x["title"])}</td><td>{E(x["creator"] or "Not named")}</td><td>{E(SOURCE.get(x["source"], x["source"]))}, {E(LICENCE.get(x["license"], x["license"]))}</td>'
               f'<td><a href="{E(x["landing"])}" target="_blank" rel="noopener">Original</a></td></tr>' for x in c)
head = head_for("Photo credits | Beer365", "Sources and licences for the photographs used on the Beer365 website.", BASE + "credits.html", "p-articles p-art", "")
main = f'''<main id="main"><section class="phero"><div class="wrap"><p class="kicker">Credits</p><h1>Photo and video credits</h1>
<p class="std">The photographs come from Wikimedia Commons and pxhere, and the hero video clips from Mixkit. Almost every photograph is public domain (CC0); one is CC BY 2.0 and is credited as its licence asks. The clips are under the Mixkit free licence. Few of these need a credit, but we give one for each. No brewery shown here is a Beer365 customer.</p></div></section>
<section><div class="wrap"><div class="scrollx"><table class="deftable"><thead><tr><th>Image</th><th>Title</th><th>By</th><th>Source and licence</th><th>Link</th></tr></thead><tbody>{rows}</tbody></table></div></div></section></main>'''
open(os.path.join(SITE, "credits.html"), "w").write(head + main + open(os.path.join(HERE, "shell_foot.html")).read())
print("credits.html")
