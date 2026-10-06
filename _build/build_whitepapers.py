"""White paper pages, their PDFs, and resources.html.

  python3 _build/build_whitepapers.py

Each _build/whitepapers/<slug>.json becomes whitepaper-<slug>.html and
downloads/<slug>.pdf (printed from the page by headless Chrome, with the print
styles in theme.css hiding the site chrome).
"""
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from build_articles import BASE, AUTHOR, ORG, E, head_for, inline, ld  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
KIND = {"brewery-business-cases": "Business cases"}


def blocks(bs):
    out = []
    for b in bs:
        if "p" in b:
            out.append(f"<p>{inline(b['p'])}</p>")
        elif "ul" in b:
            out.append('<ul class="caps">' + "".join(f"<li>{inline(x)}</li>" for x in b["ul"]) + "</ul>")
        elif "table" in b:
            t = b["table"]
            out.append('<div class="scrollx"><table class="deftable"><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in t["head"])
                       + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in t["rows"])
                       + "</tbody></table></div>")
        elif "stat" in b:
            out.append(f'<div class="wpstat"><b>{E(b["stat"]["value"])}</b><span>{inline(b["stat"]["label"])}</span></div>')
    return "".join(out)


def page(w):
    slug = w["slug"]
    kind = w.get("kind") or KIND.get(slug, "White paper")
    url = f"{BASE}whitepaper-{slug}.html"
    schema = ld({"@context": "https://schema.org", "@type": "Report", "headline": w["title"], "description": w["description"],
                 "datePublished": w["date"], "author": AUTHOR, "publisher": ORG, "keywords": ", ".join(w.get("keywords", [])),
                 "encoding": {"@type": "MediaObject", "contentUrl": f"{BASE}downloads/{slug}.pdf", "encodingFormat": "application/pdf"}})
    head = head_for(f"{w['title']} | Beer365", w["description"], url, "p-article-brewhouse-efficiency p-art p-wp", schema)
    toc = "".join(f'<li><a href="#w{i + 1}">{E(s["h2"])}</a></li>' for i, s in enumerate(w["sections"]))
    body = "".join(f'<h2 id="w{i + 1}">{E(s["h2"])}</h2>{blocks(s["blocks"])}' for i, s in enumerate(w["sections"]))
    findings = "".join(f"<li>{inline(x)}</li>" for x in w.get("summary", []))
    sources = "".join(f"<li>{inline(x)}</li>" for x in w.get("sources", []))
    main = f'''<main id="main">
<div class="crumb"><div class="wrap"><a href="resources.html">Resources</a>  /  {E(kind)}</div></div>
<section class="phero">
<div class="wrap">
<span class="topic">{E(kind)}</span>
<h1>{E(w["title"])}</h1>
<p class="std">{inline(w["subtitle"])}</p>
<div class="hmeta"><span>By Ankur Napa</span><span>{E(w["date"])}</span></div>
<div class="acts noprint"><a class="btn" href="downloads/{slug}.pdf" download>Download the PDF</a><a class="btn ghost" href="contact.html?produce=beer&amp;ask={E("I read your paper " + w["title"] + " and would like to discuss it.")}">Discuss it with us</a></div>
</div>
</section>
<section>
<div class="wrap article">
<aside class="side noprint">
<p class="blocklabel">In this paper</p>
<ol>{toc}</ol>
</aside>
<div class="prose">
<div class="findings"><p class="blocklabel">Key findings</p><ul>{findings}</ul></div>
{body}
<h2>Sources</h2><ul class="caps srcs">{sources}</ul>
<div class="author"><img src="assets/ankur-napa.jpg" alt="Ankur Napa" width="72" height="72"><div><p class="an">Written by Ankur Napa</p><p>R&amp;D brewer at United Breweries, SABMiller and AB InBev, then a data scientist on AI and generative AI for AB InBev&#39;s global business units. He leads Beer365 at Disruptive Advantage.</p><p><a href="https://www.linkedin.com/in/ankur-napa" target="_blank" rel="noopener">Ankur on LinkedIn</a></p></div></div>
</div>
</div>
</section>
<section class="talk noprint">
<div class="wrap inner">
<div><h2>Test it on <span>your</span> brewery</h2><p>Bring one week of brew sheets. We will run the same numbers on your records, on a call.</p></div>
<div class="talk-acts"><a class="btn" href="contact.html?produce=beer">Book a free demo</a><p><a href="downloads/Beer365-Readiness-Workbook.xlsx" download>Or start with the readiness workbook</a></p></div>
</div>
</section>
</main>'''
    foot = open(os.path.join(HERE, "shell_foot.html")).read()
    out = os.path.join(SITE, f"whitepaper-{slug}.html")
    open(out, "w").write(head + main + foot)
    pdf = os.path.join(SITE, "downloads", f"{slug}.pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=6000",
                    f"--print-to-pdf={pdf}", "file://" + out], check=True, capture_output=True)
    import fitz  # author in the PDF's own metadata, not only on the page
    doc = fitz.open(pdf)
    doc.set_metadata({"author": "Ankur Napa", "title": w["title"], "subject": w["subtitle"], "creator": "Beer365", "producer": "Beer365", "keywords": ", ".join(w.get("keywords", []))})
    doc.saveIncr()
    return w, kind


def resources(papers):
    cards = "".join(f'<a class="acard" href="whitepaper-{w["slug"]}.html"><span class="topic">{E(k)}</span><h3>{E(w["title"])}</h3>'
                    f'<p>{inline(w["subtitle"])}</p><span class="ameta">Web page and PDF</span></a>' for w, k in papers)
    head = head_for("Resources: white papers, business cases and the readiness workbook | Beer365",
                    "White papers on beer AI, modelled brewery business cases and a readiness workbook to download, for brewery decision makers.",
                    BASE + "resources.html", "p-articles p-art", "")
    main = f'''<main id="main">
<section class="phero"><div class="wrap">
<p class="kicker">Resources</p>
<h1>For the people who sign it off</h1>
<p class="std">White papers built on real research, business cases with every assumption shown, and a workbook to get your brewery ready. No email gate.</p>
</div></section>
<section><div class="wrap">
<div class="dl">
<div><span class="topic">Workbook</span><h2>Beer365 readiness workbook</h2>
<p class="body">Where your records live and how much you trust them, the meters behind the numbers, up to twelve baseline months with brewhouse yield, loss, energy and water worked out, the five savings formulas fed by your own figures, and all 221 questions to score. Excel, no macros.</p>
<div class="acts"><a class="btn" href="downloads/Beer365-Readiness-Workbook.xlsx" download>Download the workbook</a><a class="btn ghost" href="roi.html">Or try the calculator</a></div></div>
</div>
<h2 class="aguide">White papers and business cases</h2>
<div class="acards">{cards}</div>
<h2 class="aguide">Also useful</h2>
<div class="acards">
<a class="acard" href="use-cases.html"><span class="topic">Use cases</span><h3>Every question Beer365 answers</h3><p>221 questions across the whole beer business, by area and build wave.</p></a>
<a class="acard" href="articles.html"><span class="topic">Articles</span><h3>Notes from the floor and the model</h3><p>Practitioner articles on beer data, AI and generative AI, from the malt lot to the excise return.</p></a>
<a class="acard" href="pricing.html"><span class="topic">Pricing</span><h3>What it costs, before you ask</h3><p>The fixed assessment fee and how Microsoft bills you directly.</p></a>
</div>
</div></section>
</main>'''
    foot = open(os.path.join(HERE, "shell_foot.html")).read()
    open(os.path.join(SITE, "resources.html"), "w").write(head + main + foot)


if __name__ == "__main__":
    os.makedirs(os.path.join(SITE, "downloads"), exist_ok=True)
    order = ["brewery-business-cases", "how-beer-ai-vendors-prove-value", "state-of-beer-ai-2026"]
    ws = {json.load(open(f))["slug"]: json.load(open(f)) for f in glob.glob(os.path.join(HERE, "whitepapers", "*.json"))}
    papers = [page(ws[s]) for s in order if s in ws] + [page(w) for s, w in ws.items() if s not in order]
    resources(papers)
    print(len(papers), "papers")
