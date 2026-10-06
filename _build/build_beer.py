"""Builds index.html, the Beer365 home page (run: python3 _build/build_beer.py), the beer intelligence landing page, from the shared shell.

Every claim on the page comes from somewhere already written down:
  savings method, proof protocol, POC timeline  -> vault Brewforce-Partner/content_*.py
  market numbers                                -> beverage-ai-radar dashboard/data.json
                                                    and vault Beer AI ROI Claims KB
  team background                               -> Ankur, 2026-10-02
The shell files are the home page's head and footer; re-extract them if the nav changes.
Re-run after editing; it overwrites beer.html.
"""
import json
import os
import re
from urllib.parse import quote
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from areas import AREAS, UC, cases, examples  # noqa: E402

SITE = os.path.expanduser("~/Documents/da-website")
HERE = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.expanduser("~/Documents/beverage-ai-radar/dashboard/data.json")

# ---- market numbers, computed rather than typed -------------------------------
rows = [c for c in json.load(open(RADAR)) if c.get("company_type") != "individual"]
beer = [c for c in rows if "beer" in (str(c.get("vertical")) + str(c.get("verticals"))).lower()]
N_ALL, N_BEER = len(rows), len(beer)
N_SHIP = sum(1 for c in beer if c.get("ai_maturity") == "shipping")
N_NONE = sum(1 for c in beer if c.get("ai_maturity") == "none")
RADAR_URL = "https://ankurnapa.github.io/beverage-ai-radar/"

head = open(os.path.join(HERE, "shell_head.html")).read()
foot = open(os.path.join(HERE, "shell_foot.html")).read()
TITLE = "Beer365, intelligence for the whole beer business"
DESC = ("Find the beer, extract and energy your brewery loses between brewhouse and pack. "
        "One live batch record inside your own Microsoft tenant, savings you can check.")
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, flags=re.S)
head = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{DESC}" name="description"/>', head)
head = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{TITLE}" property="og:title"/>', head)
head = re.sub(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{DESC}" property="og:description"/>', head)
head = head.replace('class="p-index"', 'class="p-index p-beer"')

idx = open(os.path.join(SITE, "index.html")).read()
panel = re.search(r'<figure[^>]*class="live"[^>]*>.*?</figure>', idx, flags=re.S).group(0)
ask = re.search(r'<section class="ask">.*?</section>', idx, flags=re.S).group(0)


def contact(ask):
    """A contact link that arrives with Beer chosen and the message already written."""
    return "contact.html?produce=beer&amp;ask=" + quote(ask)


def pain(q, a):
    ask = f"We keep asking: {q.replace('&#39;', chr(39))} I would like to see how you would answer it from our own records."
    return (f'<div class="pain"><p class="q">{q}</p><p class="a">{a}</p>'
            f'<a class="txtlink" href="{contact(ask)}">Show me this on our data</a></div>')


def leak(name, formula, assume, why):
    return (f'<article class="leak"><h3>{name}</h3><p class="f">{formula}</p>'
            f'<p class="as"><b>We assume</b> {assume}</p><p class="why">{why}</p></article>')


def step(n, h, p):
    return f'<div class="mod"><span class="num">{n:02d}</span><h4>{h}</h4><p>{p}</p></div>'


def week(w, h, get):
    return f'<div class="wk"><span class="wn">Weeks {w}</span><h4>{h}</h4><p>{get}</p></div>'


def area_card(a):
    k, n, d, _ = a
    qs = "".join(f"<li>{u['q']}</li>" for u in examples(a))
    return (f'<a class="area" href="solutions.html#{k}"><img class="aimg" src="assets/photos/{k}.jpg" alt="" width="1200" height="700" loading="lazy"><span class="an">{len(cases(a))} questions</span>'
            f'<h3>{n}</h3><p>{d}</p><ul>{qs}</ul><span class="more">See the solution</span></a>')


def faq(q, a):
    return f'<div class="fq"><h4>{q}</h4><p>{a}</p></div>'


MAIN = f'''<main id="main">

<section class="hero xh dark">
 <div class="wrap split">
 <div>
 <span class="eyebrow-x">Beer365, built by brewers</span>
 <h1>Find the beer your brewery loses between brewhouse and pack</h1>
 <p class="std">Every brew, tank and line on one live record, inside your own Microsoft tenant. You see where extract, beer and energy go, stage by stage, priced in money, and every figure traces back to your own brew sheets.</p>
 <div class="acts">
 <a class="btn" href="{contact("I would like a free demo of beer intelligence on our own brew sheets.")}">Book a free demo</a>
 <a class="btn ghost" href="roi.html">Work out my savings</a>
 </div>
 <p class="cta-note">30 minutes with a brewer, on your own numbers. No slides, nothing to sign.</p>
 <div class="trust"><span>Brewhouse to pack</span><span>Your Azure, your data</span><span>Built by a former AB InBev master brewer</span><span>Microsoft Partner</span></div>
 </div>
 {panel}
 </div>
</section>

<section>
 <div class="wrap">
 <div class="xhead"><div><p class="kicker">Sound familiar?</p><h2>The questions a brewery cannot answer by Friday</h2></div>
 </div>
 <div class="pains">
 {pain("Why did brew 4412 attenuate short?", "Every brew plotted against its own target curve, with the fermenter, the yeast generation and the temperature log beside it.")}
 {pain("Where did this month&#39;s two percent of extract go?", "Extract tracked from the malt&#39;s lab value through mash, lauter, kettle and fermenter, so the loss lands on a stage, not on the month.")}
 {pain("Which fermenter keeps running cold overnight?", "Live tank temperatures against the profile, and the vessels that drift flagged before the batch stalls.")}
 {pain("Can we fit another brew in before Friday?", "Tank turns and cellar capacity from what each vessel is actually doing, not from last week&#39;s plan.")}
 {pain("Why does the report never match the head brewer&#39;s notebook?", "One batch record behind every report, so brewhouse yield means the same number in the cellar and the boardroom.")}
 {pain("Is the duty return right, or only reconciled?", "Measured loss reconciled with the excise register, from data the plant already produces.")}
 </div>
 </div>
</section>

<section class="whole">
 <div class="wrap">
 <div class="xhead"><div><p class="kicker">The whole beer business</p><h2>From the malt lot to the excise return</h2>
 <p class="std">Beer365 is not a fermentation sensor or a line dashboard. It is one record of the whole brewery, so it serves every department: your head brewer, packaging lead, quality team, supply chain, sales and finance work from the same numbers.</p></div>
 <a class="btn" href="solutions.html">See the full solution</a></div>
 <div class="areas">{"".join(area_card(a) for a in AREAS)}</div>
 </div>
</section>

<section class="appshow">
 <div class="wrap">
 <div class="xhead"><div><p class="kicker">The Beer365 app</p><h2>What your team sees every morning</h2>
 <p class="std">Screens from the Beer365 brewery dashboard, built on Microsoft Fabric. Shown here on demo data for a 625 hL plant.</p></div>
 <a class="btn ghost" href="features.html">See all twelve modules</a></div>
 <div class="appgrid">
 <figure class="appbig"><div class="chrome"><i></i><i></i><i></i><span>Fermentation cellar</span></div><img src="assets/app/fermentation.jpg" alt="Beer365 fermentation cellar: 32 fermenters with live fill, temperature and state" width="1600" height="1000" loading="lazy"><figcaption>Every fermenter live: fill, state and the tank that needs attention.</figcaption></figure>
 <figure><div class="chrome"><i></i><i></i><i></i><span>Quality lab</span></div><img src="assets/app/quality-lab.jpg" alt="Beer365 quality gates per batch" width="1600" height="1000" loading="lazy"><figcaption>Quality gates per batch, from OG to micro.</figcaption></figure>
 <figure><div class="chrome"><i></i><i></i><i></i><span>Packaging</span></div><img src="assets/app/packaging.jpg" alt="Beer365 packaging lines and loss map" width="1600" height="1000" loading="lazy"><figcaption>Lines and the loss map, stage by stage.</figcaption></figure>
 <figure><div class="chrome"><i></i><i></i><i></i><span>Warehouse</span></div><img src="assets/app/warehouse.jpg" alt="Beer365 raw material and packaging inventory" width="1600" height="1000" loading="lazy"><figcaption>Raw materials and packaging cover against brews.</figcaption></figure>
 </div>
 </div>
</section>

<section class="tinted" id="method">
 <div class="wrap">
 <div class="xhead"><div><p class="kicker">How we count savings</p><h2>Five leaks, five formulas, no black box</h2>
 <p class="std">Each saving is your volume, times the improvement, times what it is worth. The improvements are planning assumptions until your first month measures the real starting point, and you can replace any of them with your own number.</p></div>
 <a class="btn" href="roi.html">Work out my savings</a></div>
 <div class="leaks">
 {leak("Beer loss", "hL a year &#215; points of loss recovered &#215; brewing cost per hL", "one point recovered.", "Lost beer is valued at what it costs to make, not its selling price, so the figure stays conservative.")}
 {leak("Extract", "hL a year &#215; malt cost per hL &#215; points gained &#247; efficiency today", "one point of brewhouse efficiency.", "Every malt lot arrives with its own lab value. Comparing each brew against it shows whether a short brew was the malt, the mill gap or the sparge.")}
 {leak("Energy", "hL a year &#215; energy cost per hL &#215; share saved", "five percent of power and steam.", "Tracking both by area against your own best day typically trims a few percent.")}
 {leak("Dumped batches", "hL a year &#215; share no longer dumped &#215; brewing cost per hL", "0.2 percent of volume.", "Catching fermentation drift early saves the occasional batch that would otherwise be dumped or reworked.")}
 {leak("Reporting", "hours spent compiling reports by hand &#215; what those hours cost", "one person&#39;s reporting time.", "The daily, weekly and month-end packs that someone builds in Excel today.")}
 </div>
 <div class="nocount">
 <div><h4>Larger plants already run tighter</h4><p>So for big sites we assume three quarters of these improvements, and for the largest half. Year one counts half the saving while the system goes live.</p></div>
 <div><h4>What we never count</h4><p>Lost sales in sold-out months, faster complaint answers, smaller recalls, water, and packaging on beer no longer lost. Real, but left out.</p></div>
 </div>
 </div>
</section>

<section>
 <div class="wrap">
 <div class="xhead"><div><p class="kicker">How the saving is proved</p><h2>Signed by your plant controller, not by us</h2></div></div>
 <div class="modlist proof">
 {step(1, "Measure the baseline", "The first month runs on your records only, and we sign the starting point off with you.")}
 {step(2, "Count against it", "Each month the software reports loss, extract and energy against that baseline, in hL, cases and money, adjusted for volume.")}
 {step(3, "Show the source", "Every figure traces back to your brew sheets, dips, counts, meters and excise register.")}
 </div>
 <p class="rule-line">When we publish a result, it is a signed saving over a stated period, less 25 percent for risk, approved by the brewery before anyone sees it.</p>
 </div>
</section>

<section class="tinted">
 <div class="wrap">
 <div class="xhead"><div><p class="kicker">Proof of concept</p><h2>Twenty weeks from your spreadsheets to signed savings</h2>
 <p class="std">The first two weeks are the fixed-price assessment on our <a href="pricing.html">pricing page</a>. It works from the Excel records you already keep, across the brewhouse, cellar and every packaging line, and your head brewer and packing lead give about two hours a week.</p></div></div>
 <div class="weeks">
 {week("1 to 2", "Assessment: connect your records", "Every measurement checked, an error band on each figure, a list of any meter that needs fixing, and a fixed scope and price for the rest.")}
 {week("3 to 6", "Baseline month", "A signed baseline and agreed values per unit.")}
 {week("7 to 8", "Leak review with your team", "The three biggest leaks, by stage and by line.")}
 {week("9 to 20", "Fix, track and sign off", "Three signed monthly statements.")}
 </div>
 <p class="keep"><b>Whatever you decide afterwards,</b> you keep the signed baseline, the leak analysis, the monthly statements and all of your data.</p>
 <div class="acts cta-row"><a class="btn" href="{contact("We would like to talk about a 20-week proof of concept on our brewhouse, cellar and packaging lines.")}">Start a proof of concept</a><a class="btn ghost" href="#faq">Read what brewers ask first</a></div>
 </div>
</section>

{ask}

<section class="dark market">
 <div class="wrap">
 <div class="xhead"><div><p class="kicker">Where we sit in the market</p><h2 style="color:#fff">We map the beer AI market. Most of it watches one thing.</h2>
 <p class="std">Our open Beverage AI Radar tracks {N_ALL:,} companies applying data and AI to beer, whisky and wine. Most of the tools that ship watch a single point: one fermenter, one filler, one motor. Most brewery software is built for the taproom. We build for production plants, with several packaging lines and an excise register, and join every point into one batch record.</p></div>
 <a class="btn" href="{RADAR_URL}" target="_blank" rel="noopener">Explore the beer AI radar</a></div>
 <div class="mstats">
 <div><span class="mn">{N_BEER}</span><p>companies on the radar work in beer</p></div>
 <div><span class="mn">{N_SHIP}</span><p>of them ship AI today</p></div>
 <div><span class="mn">{N_NONE}</span><p>make no AI claim at all</p></div>
 <div><span class="mn">13</span><p>of 95 beer AI sellers we studied publish a price. About 5 explain how a saving is worked out.</p></div>
 </div>
 <p class="mnote">Counts from the radar as published, and from our September 2026 study of how beer AI vendors prove value. We put our method on this page because so few do.</p>
 </div>
</section>

<section>
 <div class="wrap">
 <div class="xhead"><div><p class="kicker">Inside your Azure</p><h2>Your plant data never leaves your tenant</h2></div></div>
 <div class="grid g4 gap24 trustg">
 <div class="kpi"><b>Your tenant and region</b><span>Built in your own Microsoft Azure and Fabric, under your identity system and on your subscription. We do not keep a copy.</span></div>
 <div class="kpi"><b>It reads, it never writes</b><span>Dashboards and the intelligence layer read from the plant. Nothing is written back to the systems that run it.</span></div>
 <div class="kpi"><b>Answers cite their source</b><span>Ask in plain English. Every answer names the batch, the tank and the record it came from, and says so when the data has a gap.</span></div>
 <div class="kpi"><b>You own the outcome</b><span>Every report, model and record is yours, whether or not you continue with us.</span></div>
 </div>
 <p class="morelink"><a class="txtlink" href="{contact("Our IT team has questions about security and where our data would live.")}">Bring your IT team&#39;s questions</a></p>
 </div>
</section>

<section class="tinted">
 <div class="wrap team">
 <div>
 <p class="kicker">Who builds it</p>
 <h2>A brewer who codes, not a vendor who learned the words</h2>
 <figure class="teamph"><img src="assets/ankur-napa-speaking.jpg" alt="Ankur Napa presenting to brewers" width="720" height="800" loading="lazy"><figcaption>Ankur Napa, presenting to brewers</figcaption></figure>
 </div>
 <div>
 <p class="std">Our beverage work is led by Ankur Napa. He was an R&amp;D brewer at United Breweries, SABMiller and AB InBev, then a data scientist on AI and GenAI for AB InBev&#39;s global business units.</p>
 <ul class="caps">
 <li>MSc Brewing Science and Technology</li>
 <li>MSc Data Science and Artificial Intelligence</li>
 <li>Microsoft Certified Fabric Analytics Engineer</li>
 <li>Delivery teams in North Sydney and Bangalore</li>
 </ul>
 <div class="acts"><a class="btn ghost" href="{contact("I would like to talk to Ankur about our brewery.")}">Talk to Ankur</a><a class="txtlink" href="about.html">About Disruptive Advantage</a></div>
 </div>
 </div>
</section>

<section id="faq">
 <div class="wrap">
 <div class="xhead"><div><p class="kicker">Brewers ask us</p><h2>Before the first call</h2></div><a class="btn ghost" href="{contact("I have a question before we book a call: ")}">Ask your own question</a></div>
 <div class="fqs">
 {faq("Our records live in Excel. Is that enough?", "Yes. The proof of concept starts from the brew sheets, dips and counts you already keep. Sensors and historian data come later, if they earn their place.")}
 {faq("Do we have to replace our ERP, MES or SCADA?", "No. We read from what you run and sit above it. Control and execution stay exactly where they are.")}
 {faq("How soon do we see something real?", "The three biggest leaks, by stage and by line, in weeks seven and eight of the proof of concept.")}
 {faq("What will it cost?", "A fixed assessment fee, credited in full against delivery, then a monthly fee. Microsoft bills you directly and we never mark it up.")}
 </div>
 <p class="morelink"><a class="txtlink" href="pricing.html">See pricing</a></p>
 </div>
</section>

<section class="talk">
 <div class="wrap inner">
 <div><h2>Bring one week of <span>brew sheets</span></h2><p>We will show you where the beer went, on a call, before anyone signs anything.</p></div>
 <div class="talk-acts"><a class="btn" href="{contact("I would like a free demo of beer intelligence on our own brew sheets.")}">Book a free demo</a>
 <p>or write to <a href="mailto:info@disruptive-advantage.com">info@disruptive-advantage.com</a></p></div>
 </div>
</section>
</main>
<div class="stickcta" id="stickcta" hidden><span>Find the beer your brewery loses</span><a class="btn sm" href="{contact("I would like a free demo of beer intelligence on our own brew sheets.")}">Book a free demo</a></div>'''

# Beer365 is the whole site now, so this page is the home page (2026-10-06).
open(os.path.join(SITE, "index.html"), "w").write(head + MAIN + foot)
print("index.html", N_ALL, N_BEER, N_SHIP, N_NONE)
