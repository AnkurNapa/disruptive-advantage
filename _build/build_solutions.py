"""solutions.html: the Beer365 solution across the whole beer business, one
section per area, built from the use case catalogue and the articles.
Ankur, 2026-10-06: cover every aspect inside the solution and the articles,
not as a separate list page.

  python3 _build/build_solutions.py
"""
import glob
import json
import os
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from areas import AREAS, cases  # noqa: E402
from build_articles import BASE, E, head_for, inline  # noqa: E402

HEADLINE = {
    "raw": "Know what every malt and hop lot really delivers",
    "brewhouse": "Every point of extract, brew by brew",
    "cellar": "Every tank following the plan written for it",
    "packaging": "Every line, every pack, every millilitre",
    "quality": "One record from the laboratory to the complaint",
    "plant": "Energy, water and kit measured per hectolitre",
    "market": "From the warehouse to the outlet and the taproom",
    "business": "True cost, defensible duty and the knowledge behind both",
    "layer": "Ask the whole brewery a question",
}
MODULES = {"raw": ["01", "10"], "brewhouse": ["03", "05"], "cellar": ["02", "03", "05"], "packaging": ["04", "05"],
           "quality": ["06", "08"], "plant": ["01", "07"], "market": ["11"], "business": ["08", "12"], "layer": ["02", "09"]}
MOD_NAME = {"01": "Telemetry", "02": "Digital twin", "03": "Fermentation", "04": "Packaging", "05": "Yield and loss",
            "06": "Quality", "07": "Energy", "08": "Excise", "09": "Copilot", "10": "Raw materials", "11": "Supply chain and sales",
            "12": "Finance and people"}
RANK = {"NOW": 0, "NEXT": 1, "LATER": 2}
APP = {"cellar": "fermentation", "quality": "quality-lab", "packaging": "packaging", "market": "warehouse"}  # demo-data dashboard screens

arts = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "articles", "*.json"))) if not os.path.basename(f).startswith("_")]


def section(i, a):
    k, name, desc, _ = a
    feats = sorted(cases(a), key=lambda u: (RANK[u["when"]], u["conf"] != "strong", u["id"]))[:6]
    flist = "".join(f'<li><b>{E(u["title"])}</b><span>{E(u["q"])}</span></li>' for u in feats)
    mine = [x for x in arts if x.get("area") == k][:4]
    reads = "".join(f'<li><a href="article-{E(x["slug"])}.html">{E(x["title"])}</a></li>' for x in mine)
    mods = " ".join(f'<a class="mchip" href="features.html">{m} {E(MOD_NAME[m])}</a>' for m in MODULES[k])
    ask = quote(f"We would like to talk about {name.lower()} at our brewery.")
    band = "tinted" if i % 2 else ""
    return f'''<section class="{band} solarea" id="{k}">
 <div class="wrap sgrid">
 <div class="stext">
 <p class="kicker">{E(name)}</p>
 <h2>{E(HEADLINE[k])}</h2>
 <p class="std">{E(desc)}</p>
 <ul class="sfeat">{flist}</ul>
 <p class="smods"><span>Modules</span>{mods}</p>
 <div class="acts"><a class="btn" href="contact.html?produce=beer&amp;ask={ask}">Talk about {E(name.lower())}</a></div>
 </div>
 <aside class="sside">
 {f'<figure class="sapp"><div class="chrome"><i></i><i></i><i></i><span>Beer365 app</span></div><img src="assets/app/{APP[k]}.jpg" alt="Beer365 app screen for {E(name.lower())}" width="1600" height="1000" loading="lazy"></figure>' if k in APP else f'<img src="assets/photos/{k}.jpg" alt="" width="1200" height="700" loading="lazy">'}
 {f'<p class="blocklabel">Read more</p><ul class="sreads">{reads}</ul>' if reads else ""}
 </aside>
 </div>
</section>'''


FEATURED = [  # (page, tag, photo): the "Selected work" mosaic, NIRAS style
    ("case-study-extract-loss", "Case study", "raw-2"),
    ("whitepaper-state-of-beer-ai-2026", "White paper", "layer"),
    ("whitepaper-brewery-business-cases", "White paper", "business-2"),
    ("whitepaper-how-beer-ai-vendors-prove-value", "White paper", "quality-2"),
    ("article-generative-ai-for-breweries", "Article", "cellar-2"),
    ("article-brewery-digital-twin", "Article", "plant-2"),
]
RELATED = [("about.html", "About Beer365", "ankur-napa-speaking.jpg"), ("case-studies.html", "Case studies", "photos/packaging.jpg"),
           ("pricing.html", "Pricing", "photos/market-2.jpg")]


def title_of(page):
    html = open(os.path.join(SITE, page + ".html")).read()
    return html.split("<title>", 1)[1].split("</title>", 1)[0].replace(" | Beer365", "")


def tile(page, tag, photo, big):
    return (f'<a class="ntile{" big" if big else ""}" href="{page}.html"><img src="assets/photos/{photo}.jpg" alt="" width="1200" height="700" loading="lazy">'
            f'<span class="ntag">{E(tag)}</span><b>{E(title_of(page))}</b></a>')


def mosaic():
    rows = [FEATURED[i:i + 3] for i in range(0, len(FEATURED), 3)]
    out = []
    for r, row in enumerate(rows):
        big, small = tile(*row[0], True), "".join(tile(*x, False) for x in row[1:])
        out.append(f'<div class="nrow{" flip" if r % 2 else ""}">{big}<div class="nstack">{small}</div></div>')
    return "".join(out)


arrow = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
services = "".join(f'<li><a class="nsvc" href="#{k}"><span>{E(n)}</span><small>{len(cases(a))} questions</small>{arrow}</a></li>'
                   for a in AREAS for k, n in [a[:2]])
related = "".join(f'<a class="nrel" href="{h}"><img src="assets/{img}" alt="" width="1200" height="800" loading="lazy"><span>{E(t)}</span></a>' for h, t, img in RELATED)
total = sum(len(cases(a)) for a in AREAS)
head = head_for("Solutions for the whole beer business | Beer365",
                "Beer365 across the whole brewery: raw materials, brewhouse, cellar, packaging, quality, plant, supply chain, sales, marketing, finance and people.",
                BASE + "solutions.html", "p-articles p-art p-sol", "")
head = head.replace('<a href="solutions.html">Solutions</a>', '<a aria-current="page" href="solutions.html">Solutions</a>', 1)
main = f'''<main id="main">
<section class="nhero">
 <img class="nhero-bg" src="assets/photos/brewhouse-2.jpg" alt="" width="1200" height="700" fetchpriority="high">
 <div class="wrap">
 <h1>One solution for the whole beer business</h1>
 <p>Beer365 joins the brewhouse, cellar, packaging, quality, plant, supply chain, sales and finance on one batch record, inside your own Microsoft tenant.</p>
 </div>
</section>
<nav class="wrap ncrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">›</span><span aria-current="page">Solutions</span></nav>
<section class="nintro">
 <div class="wrap">
 <h2 class="nrule">One record, every department</h2>
 <div class="nprose">
 <p>Most breweries already hold the numbers that explain their losses. They sit in a brew log, a laboratory sheet, a packaging report and the finance ledger, and nobody joins them.</p>
 <p>Beer365 answers {total} questions a brewer asks, grouped into nine areas of the business. Every answer reads from the same batch record, so the cellar and the finance team see one number.</p>
 <p>Start with the area that costs you most; every other area reads from the same record.</p>
 </div>
 </div>
</section>
<section class="nwork">
 <div class="wrap">
 <h2 class="nrule right">Selected work:</h2>
 {mosaic()}
 </div>
</section>
<section class="nareas">
 <div class="wrap">
 <h2 class="nrule">Areas of the business</h2>
 <ul class="nsvcs">{services}</ul>
 </div>
</section>
{"".join(section(i, a) for i, a in enumerate(AREAS))}
<section class="ncontact">
 <div class="wrap">
 <h2 class="nrule">Want to know more?</h2>
 <div class="ncard">
 <img src="assets/ankur-napa.jpg" alt="Ankur Napa" width="480" height="480" loading="lazy">
 <div>
 <p class="nname">Ankur Napa</p>
 <p class="nrole">Leads beverage work, Disruptive Advantage</p>
 <p class="nloc">Bengaluru, India</p>
 <p class="nlinks"><a href="tel:+917755909445">+91 7755 909445</a><a href="mailto:ankur.napa@disruptive-advantage.com">E-mail</a></p>
 </div>
 </div>
 </div>
</section>
<section class="nrelated">
 <div class="wrap">
 <h2 class="nrule">You might also find interest in:</h2>
 <div class="nrels">{related}</div>
 </div>
</section>
<section class="talk">
 <div class="wrap inner">
 <div><h2>Start with the area that <span>hurts</span></h2><p>Tell us which part of the brewery costs you most. We will show you how it is answered from your own records.</p></div>
 <div class="talk-acts"><a class="btn" href="contact.html?produce=beer">Book a free demo</a><p><a href="features.html">See all twelve modules</a></p></div>
 </div>
</section>
</main>'''
open(os.path.join(SITE, "solutions.html"), "w").write(head + main + open(os.path.join(HERE, "shell_foot.html")).read())
print("solutions.html")
