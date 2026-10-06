"""Builds every article page, the articles index, sitemap.xml, robots.txt and
llms.txt from the JSON files in _build/articles/.

  python3 _build/build_articles.py

Article JSON schema is in _build/articles/_BRIEF.md. Dates are assigned here, not
by the writers: newest first in the order of DATES below, so re-running is stable.
"""
import datetime as dt
import glob
import html
import json
import os
import re
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from areas import AREAS  # noqa: E402

BASE = "https://ankurnapa.github.io/disruptive-advantage/"
AREA = {k: n for k, n, _, _ in AREAS}
E = lambda s: html.escape(str(s), quote=True)
ARTDIR = os.path.join(HERE, "articles")


def inline(t):
    """Escape, then allow **bold** only."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", E(t))


def load():
    arts = []
    for f in sorted(glob.glob(os.path.join(ARTDIR, "*.json"))):
        if os.path.basename(f).startswith("_"):
            continue
        a = json.load(open(f))
        a.setdefault("area", "layer")
        a["pillar"] = a.get("uc_id") is None
        words = sum(len(re.sub(r"<[^>]+>", " ", json.dumps(s)).split()) for s in a["sections"])
        a["read_min"] = max(3, round(words / 220))
        arts.append(a)
    # Dates: pillars newest, then the rest interleaved by area so any week reads varied.
    pillars = [a for a in arts if a["pillar"]]
    rest = [a for a in arts if not a["pillar"]]
    by_area = {}
    for a in rest:
        by_area.setdefault(a["area"], []).append(a)
    mixed = []
    while any(by_area.values()):
        for k in [k for k, *_ in AREAS]:
            if by_area.get(k):
                mixed.append(by_area[k].pop(0))
    ordered = pillars + mixed
    keys = [k for k, *_ in AREAS if k != "layer"]
    seen = {}
    for i, a in enumerate(ordered):
        if a["pillar"]:
            k = keys[i % len(keys)]
            a["photo"] = k if (i // len(keys)) % 2 == 0 else (k + "-2" if os.path.exists(os.path.join(SITE, "assets", "photos", k + "-2.jpg")) else k)
        else:
            n = seen.get(a["area"], 0)
            seen[a["area"]] = n + 1
            alt = a["area"] + "-2"
            a["photo"] = alt if n % 2 and os.path.exists(os.path.join(SITE, "assets", "photos", alt + ".jpg")) else a["area"]
    json.dump({f"article-{a['slug']}.html": a["photo"] for a in ordered}, open(os.path.join(HERE, "article_photos.json"), "w"), indent=1)
    day = dt.date(2026, 10, 5)
    for i, a in enumerate(ordered):
        a["date"] = day - dt.timedelta(days=round(i * 2.6))
    return ordered


def head_for(title, desc, url, body_cls, extra=""):
    h = open(os.path.join(HERE, "shell_head.html")).read()
    h = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", h, flags=re.S)
    h = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{E(desc)}" name="description"/>', h)
    h = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{E(title)}" property="og:title"/>', h)
    h = re.sub(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{E(desc)}" property="og:description"/>', h)
    h = re.sub(r'<link href="[^"]*" rel="canonical"/>', f'<link href="{url}" rel="canonical"/>', h)
    h = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{url}" property="og:url"/>', h)
    h = h.replace('<meta content="website" property="og:type"/>', '<meta content="article" property="og:type"/>') if "article-" in url else h
    h = h.replace("</head>", extra + "\n</head>", 1)
    h = re.sub(r'<body class="[^"]*">', f'<body class="{body_cls}">', h)
    if "articles" in url or "article-" in url:
        h = h.replace('<a href="articles.html">Articles</a>', '<a aria-current="page" href="articles.html">Articles</a>', 1)
    return h


def block(b):
    if "p" in b:
        return f"<p>{inline(b['p'])}</p>"
    if "ul" in b:
        return "<ul class=\"caps\">" + "".join(f"<li>{inline(x)}</li>" for x in b["ul"]) + "</ul>"
    if "eq" in b:
        q = b["eq"]
        note = f'<p style="font-size:15px;color:var(--mid)">{inline(q["note"])}</p>' if q.get("note") else ""
        return f'<div class="eq"><b>{E(q.get("label", ""))}</b><code>{E(q["code"])}</code>{note}</div>'
    if "table" in b:
        t = b["table"]
        th = "".join(f"<th>{E(x)}</th>" for x in t["head"])
        rows = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in t["rows"])
        return f'<div class="scrollx"><table class="deftable"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>'
    return ""


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


ORG = {"@type": "Organization", "name": "Beer365", "url": BASE,
       "logo": BASE + "assets/beer365-logo.svg",
       "parentOrganization": {"@type": "Organization", "name": "Disruptive Advantage"}}
AUTHOR = {"@type": "Person", "name": "Ankur Napa", "jobTitle": "Growth Officer, Beverage R&D", "image": BASE + "assets/ankur-napa.jpg",
          "sameAs": ["https://www.linkedin.com/in/ankur-napa"]}


def article_page(a, arts):
    url = f"{BASE}article-{a['slug']}.html"
    desc = a.get("description") or a["standfirst"]
    area_name = AREA.get(a["area"], "Brewing")
    schema = [ld({"@context": "https://schema.org", "@type": "Article", "headline": a["title"],
                  "description": desc, "datePublished": a["date"].isoformat(), "dateModified": a["date"].isoformat(),
                  "author": AUTHOR, "publisher": ORG, "mainEntityOfPage": url,
                  "keywords": ", ".join(a.get("keywords", [])) or None, "articleSection": area_name})]
    if a.get("faq"):
        schema.append(ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in a["faq"]]}))
    head = head_for(f"{a['title']} | Beer365", desc, url, "p-article-brewhouse-efficiency p-art", "\n".join(schema))
    secs = a["sections"]
    toc = "".join(f'<li><a href="#s{i + 1}">{E(s["h2"])}</a></li>' for i, s in enumerate(secs))
    body = "".join(f'<h2 id="s{i + 1}">{E(s["h2"])}</h2>' + "".join(block(b) for b in s["blocks"]) for i, s in enumerate(secs))
    if a.get("faq"):
        body += '<h2 id="faq">Questions people ask</h2>' + "".join(
            f'<div class="afq"><h3>{E(q["q"])}</h3><p>{inline(q["a"])}</p></div>' for q in a["faq"])
        toc += '<li><a href="#faq">Questions people ask</a></li>'
    related = [r for r in arts if r is not a and r["area"] == a["area"]][:3]
    if len(related) < 3:
        related += [r for r in arts if r is not a and r not in related and r["pillar"]][:3 - len(related)]
    rel = "".join(card(r) for r in related)
    ask = quote(f"I read your article \"{a['title']}\" and would like to talk about it for our brewery.")
    main = f'''<main id="main">
<div class="crumb"><div class="wrap"><a href="articles.html">Articles</a>  /  {E(area_name)}</div></div>
<section class="phero">
<div class="wrap">
<span class="topic">{E(area_name)}</span>
<h1>{E(a["title"])}</h1>
<p class="std">{inline(a["standfirst"])}</p>
<div class="hmeta"><span>By Ankur Napa</span><span>{a["read_min"]} min read</span><span>{a["date"].strftime("%-d %B %Y")}</span></div>
<figure class="ahero"><img src="assets/photos/{E(a["photo"])}.jpg" alt="" width="1200" height="700"></figure>
</div>
</section>
<section>
<div class="wrap article">
<aside class="side">
<p class="blocklabel">On this page</p>
<ol>{toc}</ol>
<div class="sidecta"><p>Want this answered from your own records?</p><a class="btn sm" href="contact.html?produce=beer&amp;ask={ask}">Book a free demo</a></div>
</aside>
<div class="prose">{body}
<p class="ucline">Part of the Beer365 solution for <a href="solutions.html#{E(a["area"])}">{E(area_name.lower())}</a>.</p>
<div class="author"><img src="assets/ankur-napa.jpg" alt="Ankur Napa" width="72" height="72"><div><p class="an">Written by Ankur Napa</p><p>R&amp;D brewer at United Breweries, SABMiller and AB InBev, then a data scientist on AI and generative AI for AB InBev&#39;s global business units. MSc Brewing Science and Technology, MSc Data Science and AI, Microsoft Certified Fabric Analytics Engineer. He leads Beer365 at Disruptive Advantage.</p><p><a href="tel:+917755909445">+91 7755 909445</a> · <a href="mailto:ankur.napa@disruptive-advantage.com">ankur.napa@disruptive-advantage.com</a><br/><a href="https://www.linkedin.com/in/ankur-napa" target="_blank" rel="noopener">Ankur on LinkedIn</a> · <a href="contact.html?produce=beer&amp;ask=I%20would%20like%20to%20talk%20to%20Ankur%20about%20our%20brewery.">Talk to Ankur</a></p></div></div>
</div>
</div>
</section>
<section class="tinted">
<div class="wrap">
<div class="xhead"><div><p class="kicker">Keep reading</p><h2>More on {E(area_name.lower())}</h2></div><a class="btn ghost" href="articles.html">All articles</a></div>
<div class="acards">{rel}</div>
</div>
</section>
<section class="talk">
<div class="wrap inner">
<div><h2>Bring one week of <span>brew sheets</span></h2><p>We will show you where the beer went, on a call, before anyone signs anything.</p></div>
<div class="talk-acts"><a class="btn" href="contact.html?produce=beer&amp;ask={ask}">Book a free demo</a><p class="direct">Or talk to Ankur directly: <a href="tel:+917755909445">+91 7755 909445</a> · <a href="mailto:ankur.napa@disruptive-advantage.com">ankur.napa@disruptive-advantage.com</a></p></div>
</div>
</section>
</main>'''
    foot = open(os.path.join(HERE, "shell_foot.html")).read()
    open(os.path.join(SITE, f"article-{a['slug']}.html"), "w").write(head + main + foot)


def card(a, big=False):
    return (f'<a class="acard{" big" if big else ""}" href="article-{a["slug"]}.html" data-area="{E(a["area"])}">'
            f'<img class="cimg" src="assets/photos/{E(a.get("photo", a["area"]))}.jpg" alt="" width="1200" height="700" loading="lazy">'
            f'<span class="topic">{E(AREA.get(a["area"], "Brewing"))}</span><h3>{E(a["title"])}</h3>'
            f'<p>{inline(a["standfirst"])}</p><span class="ameta">{a["date"].strftime("%-d %b %Y")} · {a["read_min"]} min read</span></a>')


LEGACY = {"slug": "brewhouse-efficiency", "area": "brewhouse", "pillar": False, "read_min": 12,
          "title": "Brewhouse efficiency is three different numbers, and your team is quoting all of them",
          "standfirst": "Mash conversion, lauter efficiency and brewhouse yield get used interchangeably, which is why the report never matches the head brewer's notebook.",
          "date": dt.date(2026, 3, 16)}


def index_page(arts):
    allarts = arts + [LEGACY]
    chips = '<button class="chip is-on" type="button" data-area="all" aria-pressed="true">Everything</button>' + "".join(
        f'<button class="chip" type="button" data-area="{k}" aria-pressed="false">{E(n)}</button>'
        for k, n, _, _ in AREAS if any(a["area"] == k for a in allarts))
    pillars = [a for a in arts if a["pillar"]]
    lead = pillars[0] if pillars else arts[0]
    guides = "".join(card(a) for a in pillars[1:7])
    cards = "".join(card(a) for a in allarts if a is not lead)
    head = head_for("Articles on beer data, AI and brewing | Beer365",
                    f"{len(allarts)} practitioner articles on brewery data, AI and generative AI, Azure, AWS and Google Cloud, from the brewhouse to the excise return.",
                    BASE + "articles.html", "p-articles p-art",
                    ld({"@context": "https://schema.org", "@type": "Blog", "name": "Beer365 articles", "url": BASE + "articles.html", "publisher": ORG}))
    main = f'''<main id="main">
<section class="phero">
<div class="wrap">
<p class="kicker">Articles</p>
<h1>Notes from the floor and the model</h1>
<p class="std">{len(allarts)} practitioner articles on beer data, AI and generative AI across the whole brewery, written by a brewer who codes.</p>
</div>
</section>
<section>
<div class="wrap">
<div class="alead">{card(lead, True)}</div>
{f'<h2 class="aguide">Start here: the guides</h2><div class="acards">{guides}</div>' if guides else ""}
</div>
</section>
<section class="tight ucbar">
<div class="wrap">
<div class="ucfilters" role="group" aria-label="Filter by area">{chips}</div>
<div class="ucsearch"><label for="aq" class="vh">Search the articles</label>
<input id="aq" type="search" placeholder="Search, for example: Azure, keg, diacetyl, forecast" autocomplete="off">
<span class="uccount"><b id="aShown">{len(cards and allarts) - 1}</b> articles</span></div>
</div>
</section>
<section>
<div class="wrap"><div class="acards" id="alist">{cards}</div>
<p class="ucnone" id="aNone" hidden>No article matches that yet. <a href="contact.html?produce=beer">Ask us the question</a> and it may become the next one.</p></div>
</section>
<section class="tinted">
<div class="wrap news">
<div><h2>One note a month, from the floor</h2><p class="body">What we are seeing in brewery data. No product announcements.</p></div>
<div><div class="form"><input aria-label="Work email address" placeholder="Work email address" type="email"><button type="button">Submit</button></div>
<p class="body" style="font-size:.8125rem;margin-top:10px">We use this to send the monthly note and nothing else.</p></div>
</div>
</section>
</main>
<script>
(function () {{
  'use strict';
  var chips = Array.prototype.slice.call(document.querySelectorAll('.ucfilters .chip'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('#alist .acard'));
  var q = document.getElementById('aq'), shown = document.getElementById('aShown'), none = document.getElementById('aNone'), area = 'all';
  function run() {{
    var t = q.value.trim().toLowerCase(), n = 0;
    cards.forEach(function (c) {{
      var ok = (area === 'all' || c.getAttribute('data-area') === area) && (!t || c.textContent.toLowerCase().indexOf(t) !== -1);
      c.hidden = !ok; if (ok) {{ n++; }}
    }});
    shown.textContent = String(n); none.hidden = n !== 0;
  }}
  chips.forEach(function (c) {{ c.addEventListener('click', function () {{
    area = c.getAttribute('data-area');
    chips.forEach(function (x) {{ var on = x === c; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', String(on)); }});
    run();
  }}); }});
  q.addEventListener('input', run);
}})();
</script>'''
    foot = open(os.path.join(HERE, "shell_foot.html")).read()
    open(os.path.join(SITE, "articles.html"), "w").write(head + main + foot)


def site_files(arts):
    pages = sorted(p for p in glob.glob(os.path.join(SITE, "*.html"))
                   if "http-equiv=\"refresh\"" not in open(p).read())
    today = dt.date.today().isoformat()
    urls = []
    for p in pages:
        name = os.path.basename(p)
        loc = BASE if name == "index.html" else BASE + name
        a = next((x for x in arts if f"article-{x['slug']}.html" == name), None)
        urls.append(f"<url><loc>{loc}</loc><lastmod>{a['date'].isoformat() if a else today}</lastmod></url>")
    open(os.path.join(SITE, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(SITE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    lines = ["# Beer365", "",
             "> Beer365 is beer intelligence for the whole beer business, built by Disruptive Advantage on Microsoft Azure "
             "and Microsoft Fabric inside the brewery's own tenant. It joins brewhouse, cellar, packaging, quality, supply "
             "chain, sales and finance data into one batch record, with dashboards, a digital twin and a generative AI "
             "copilot whose answers cite the batch and tag they came from.", "",
             "## Key pages", f"- [Home]({BASE}): what Beer365 does, how savings are counted and proved",
             f"- [Solutions]({BASE}solutions.html): Beer365 across the whole beer business, area by area",
             f"- [Calculator]({BASE}roi.html): brewhouse savings from your own figures",
             f"- [Pricing]({BASE}pricing.html)", f"- [Contact]({BASE}contact.html)", "", "## Guides"]
    lines += [f"- [{a['title']}]({BASE}article-{a['slug']}.html): {a.get('description') or a['standfirst']}" for a in arts if a["pillar"]]
    lines += ["", "## White papers and business cases"]
    for f in sorted(glob.glob(os.path.join(HERE, "whitepapers", "*.json"))):
        w = json.load(open(f))
        lines.append(f"- [{w['title']}]({BASE}whitepaper-{w['slug']}.html): {w['description']} PDF: {BASE}downloads/{w['slug']}.pdf")
    lines += [f"- [Beer365 readiness workbook (Excel)]({BASE}downloads/Beer365-Readiness-Workbook.xlsx)", f"- [Resources]({BASE}resources.html)"]
    lines += ["", "## Articles"]
    lines += [f"- [{a['title']}]({BASE}article-{a['slug']}.html)" for a in arts if not a["pillar"]]
    open(os.path.join(SITE, "llms.txt"), "w").write("\n".join(lines) + "\n")


def home_schema():
    p = os.path.join(SITE, "index.html")
    h = open(p).read()
    if '"@type": "SoftwareApplication"' in h:
        return
    s = ld({"@context": "https://schema.org", "@graph": [
        {**ORG, "@type": "Organization"},
        {"@type": "WebSite", "name": "Beer365", "url": BASE},
        {"@type": "SoftwareApplication", "name": "Beer365", "applicationCategory": "BusinessApplication",
         "operatingSystem": "Microsoft Azure, Microsoft Fabric",
         "description": "Beer intelligence for the whole beer business: one batch record from brewhouse to pack, "
                        "dashboards, a digital twin and a generative AI copilot that cites its sources.",
         "publisher": ORG}]})
    open(p, "w").write(h.replace("</head>", s + "\n</head>", 1))


if __name__ == "__main__":
    arts = load()
    for a in arts:
        article_page(a, arts)
    index_page(arts)
    home_schema()
    site_files(arts)
    print(f"{len(arts)} articles, {sum(a['pillar'] for a in arts)} guides")
