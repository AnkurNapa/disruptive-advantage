"""One-off pass that makes the site beer-only (Ankur, 2026-10-06: "this whole
website beer specific"). Whisky and wine content is removed, not hidden; git
history keeps it. Safe to re-run: every step checks before it changes."""
import glob
import os
import re

from bs4 import BeautifulSoup

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(SITE)
frag = lambda h: BeautifulSoup(h, "html.parser")


def load(f):
    return BeautifulSoup(open(f), "html.parser")


def save(f, s):
    open(f, "w").write(str(s))


FOOT_COL = ('<div><h5>Beer365</h5><a href="use-cases.html">Use cases</a><br/>'
            '<a href="features.html">Features</a><br/><a href="roi.html">Calculator</a><br/>'
            '<a href="pricing.html">Pricing</a></div>')


def chrome(s):
    """Menu and footer, the same on every page."""
    for a in s.select('#sitenav a[href="beer.html"]'):
        a["href"] = "use-cases.html"
        a.string = "Use cases"
        a.attrs.pop("aria-current", None)
    for h5 in s.select("footer h5"):
        if h5.get_text(strip=True) == "Solutions":
            h5.parent.replace_with(frag(FOOT_COL))
    for a in s.find_all("a", href=True):
        if a["href"].startswith("beer.html"):
            a["href"] = a["href"].replace("beer.html", "index.html", 1)
        if a["href"].startswith("case-study-spirit-account.html"):
            a["href"] = "case-study-extract-loss.html"


# ---- solutions -----------------------------------------------------------------
def solutions(s):
    h1 = s.select_one(".phero h1")
    h1.string = "Built for the way beer is actually made"
    s.select_one(".phero .std").string = (
        "One data foundation under the whole brewery, configured for how yours runs: "
        "brewhouse, cellar, packaging, quality and the business around them.")
    j = s.select_one(".jump")
    if j:
        j.decompose()
    for k in ("whisky", "wine"):
        sec = s.select_one(f"section.sol.{k}")
        if sec:
            sec.decompose()
    for sec in s.select("main > section.tinted"):
        if sec.find("table", class_="matrix"):
            sec.replace_with(frag(
                '<section class="tinted"><div class="wrap"><div class="xhead"><div>'
                '<p class="kicker">The whole beer business</p>'
                '<h2>221 questions, from the malt lot to the excise return</h2>'
                '<p class="std">Brewhouse and cellar are where most breweries start. The same record '
                'then answers the questions your packaging, quality, supply chain, sales and finance '
                'teams ask.</p></div>'
                '<a class="btn" href="use-cases.html">See every question</a></div></div></section>'))


# ---- features: module 04 becomes packaging ------------------------------------------
def features(s):
    for card in s.select("article.mcard"):
        h = card.find("h4")
        if h and "Distillation" in h.get_text():
            h.string = "Packaging and line performance"
            card.find("p").string = ("Bottle, can and keg lines measured the same way: fill level and "
                                     "give-away, dissolved oxygen, rejects, changeovers and efficiency by "
                                     "line, shift and pack.")
            ul = card.find("ul")
            ul.clear()
            for t in ("Give-away priced per line", "Changeovers costed", "Oxygen pick-up caught early"):
                li = s.new_tag("li")
                li.string = t
                ul.append(li)
    for p in s.find_all("p"):
        t = p.get_text()
        if "the extract, the spirit and the packaged volume" in t:
            p.string = t.replace("the extract, the spirit and the packaged volume",
                                 "the extract, the beer and the packaged volume")


# ---- case studies ------------------------------------------------------------------
def case_studies(s):
    for c in s.select(".csc"):
        if c.get("data-ind") != "beer":
            c.decompose()
    bar = s.select_one(".bar")
    if bar:
        (bar.find_parent("section") or bar).decompose()
    for p in s.find_all("p"):
        t = p.get_text(" ", strip=True)
        if t.startswith("Representative engagements across beer"):
            p.string = "Representative engagements in brewing, written from delivered work and anonymised."
        if t.startswith("What we are seeing in brewery, distillery"):
            p.string = "What we are seeing in brewery data. No product announcements."
    count = s.select_one("#csCount")
    if count:
        count.string = str(len(s.select(".csc")))
    cards = s.select(".csc")
    if len(cards) > 1:  # only the extract study has a full write-up so far
        a = cards[1].select_one("a.txtlink")
        if a:
            a.replace_with(frag('<span class="txtlink" style="color:var(--soft)">Full study coming</span>'))


def contact(s):
    lbl = s.select_one("#producelabel")
    if lbl:
        lbl.string = "What kind of brewery"
    for btn, (val, txt) in zip(s.select(".pill[data-produce]"),
                               [("beer", "Production brewery"), ("craft", "Craft brewery or brewpub"),
                                ("contract", "Contract brewer"), ("other", "Something else")]):
        btn["data-produce"] = val
        btn.string = txt


def about(s):
    h = [x for x in s.find_all("h2") if "Industries" in x.get_text()]
    if not h:
        return
    sec = h[0].find_parent("section")
    items = [("Production breweries", "Several packaging lines and an excise register"),
             ("Craft breweries", "From the brew sheet up, without a data team"),
             ("Brewpubs and taprooms", "The brewing and the bar on one record"),
             ("Contract brewers", "Every tank day priced against the contract"),
             ("Brewery groups", "Several sites compared on one set of numbers"),
             ("New brewery projects", "The data designed in before the first brew")]
    cards = "".join(f'<div class="scard"><b>{b}</b><span>{t}</span></div>' for b, t in items)
    sec.replace_with(frag(
        f'<section class="tinted"><div class="wrap"><h2>Who Beer365 is for</h2>'
        f'<p class="std">Breweries where the operation is the business, from a single craft site to a '
        f'multi-line production plant.</p><div class="serve">{cards}</div></div></section>'))


def careers(s):
    for h in s.find_all("h3"):
        if h.get_text(strip=True) == "Process Engineer, Beverage":
            h.string = "Process Engineer, Brewing"
    for p in s.find_all("p"):
        if "brewing, distilling and winemaking practice" in p.get_text():
            p.string = "Translate brewing practice into models."
    for a in s.find_all("a", href=True):
        a["href"] = a["href"].replace("Process%20Engineer%2C%20Beverage", "Process%20Engineer%2C%20Brewing")


# ---- the beer case study, replacing the whisky one ----------------------------------
STUDY = '''<div class="crumb"><div class="wrap"><a href="case-studies.html">Case Studies</a>  /  Extract loss at month end</div></div>
<section class="phero">
<div class="wrap">
<span class="tag">Beer</span><span class="lbl">Representative engagement</span>
<h1>Extract loss that only showed up at month end</h1>
<p class="std">A regional ale brewery could reconcile brewhouse yield monthly but never per brew. Stage level extract accounting put the loss on a named vessel inside the first week of live data.</p>
<div class="hmeta">
<div class="facts">
<div class="fact"><span>Sector</span><b>Regional ale brewery</b></div>
<div class="fact"><span>Region</span><b>[REGION]</b></div>
<div class="fact"><span>Modules</span><b>01, 05</b></div>
<div class="fact"><span>Went live</span><b>[DATE]</b></div>
</div>
<div class="share">
<button aria-label="Copy link to this case study" class="sharebtn" data-share="copy" type="button"><svg fill="none" stroke="currentColor" stroke-width="1.6" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"></path><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"></path></svg></button>
<a aria-label="Share on LinkedIn" class="sharebtn" data-share="linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fankurnapa.github.io%2Fdisruptive-advantage%2Fcase-study-extract-loss.html" rel="noopener" target="_blank"><svg fill="none" stroke="currentColor" stroke-width="1.6" viewBox="0 0 24 24"><rect height="18" width="18" x="3" y="3"></rect><path d="M7 10v7M7 7v.01M11 17v-4a2 2 0 0 1 4 0v4"></path></svg></a>
<a aria-label="Share by email" class="sharebtn" href="mailto:?subject=Beer365%20case%20study&amp;body=https%3A%2F%2Fankurnapa.github.io%2Fdisruptive-advantage%2Fcase-study-extract-loss.html"><svg fill="none" stroke="currentColor" stroke-width="1.6" viewBox="0 0 24 24"><rect height="14" width="18" x="3" y="5"></rect><path d="M3 7l9 6 9-6"></path></svg></a>
</div>
</div>
</div>
</section>
<section>
<div class="wrap article">
<aside class="side">
<p class="blocklabel">At a glance</p>
<ul>
<li><b>The problem</b>Brewhouse yield was reconciled monthly, never per brew</li>
<li><b>What we read</b>Grist weights, malt certificates, vessel volumes, gravity readings, brew sheets</li>
<li><b>What we built</b>Extract accounting per brew and per stage, from mash tun to fermenter</li>
<li><b>Who uses it</b>Head brewer, brewhouse team, finance</li>
</ul>
</aside>
<div class="prose">
<h3>The situation</h3>
<p>Every month the brewery compared the malt it used with the beer it made, and every month the gap was a little wider than it should have been. Nobody could say where it went. The brew sheets held the readings, but they were filed rather than joined, and a monthly figure hides which brew, which vessel and which step lost the extract.</p>
<p>The head brewer's question was simple: is it the malt, the mill, the lauter or the transfers? Without a figure per brew, every answer was a guess.</p>
<h3>What we read</h3>
<p>Grist weights and the malt certificates of analysis, so each brew had a theoretical extract to measure against. Kettle and fermenter volumes, corrected to temperature. Gravity readings at each transfer. All of it read only, from the records the brewery already kept, with nothing written back to the systems that run the brewhouse.</p>
<h3>What we built</h3>
<p>Extract accounting per brew, in kilograms rather than percentages, at each stage: charged, in the kettle and into the fermenter. Each stage carries its own loss figure, so the monthly gap breaks down into steps and vessels.</p>
<p>Within the first week of live data the loss sat on one named vessel rather than spread across the month. That turned an argument about a number into a maintenance job.</p>
<div class="outcome">
<p>What changed</p>
<ul>
<li>Brewhouse yield is known per brew, the day after it is brewed</li>
<li>Loss is attributed to a stage and a vessel, not to the month</li>
<li>Malt lots are compared with what they actually delivered</li>
<li>The month-end reconciliation agrees with the brew sheets</li>
</ul>
</div>
<h3>Where it went next</h3>
<p>The same extract record now runs on into the cellar and packaging, so loss can be followed from the mash tun to the pack on one set of numbers.</p>
</div>
</div>
</section>
<section class="tinted">
<div class="wrap">
<p class="blocklabel">Other case studies</p>
<div class="others">
<article class="oc" style="--k:var(--beer)">
<span class="tag">Beer</span>
<h4>Fifteen fermenters and one shared spreadsheet</h4>
<p>A live digital twin of the cellar replaced the sheet, and the brew schedule started being planned against real tank availability.</p>
<a class="txtlink" href="case-studies.html">All case studies</a>
</article>
</div>
</div>
</section>
<section class="talk">
<div class="wrap inner">
<div><h2>Your extract is probably reconciled <span>monthly</span> too</h2><p>Show us how you work out brewhouse yield today and we will show you what it looks like per brew.</p></div>
<div class="talk-acts"><a class="btn" href="contact.html?produce=beer&amp;ask=We%20reconcile%20brewhouse%20yield%20monthly%20and%20would%20like%20to%20see%20it%20per%20brew.">Book a free demo</a></div>
</div>
</section>'''


def make_study():
    if not os.path.exists("case-study-spirit-account.html"):
        return
    s = load("case-study-spirit-account.html")
    main = s.find("main")
    main.clear()
    main.append(frag(STUDY))
    s.title.string = "Extract loss that only showed up at month end | Beer365"
    for m in s.find_all("meta"):
        if m.get("name") == "description" or m.get("property") == "og:description":
            m["content"] = "A regional ale brewery reconciled brewhouse yield monthly, never per brew. Stage level extract accounting put the loss on a named vessel."
        if m.get("property") == "og:title":
            m["content"] = "Extract loss that only showed up at month end | Beer365"
        if m.get("property") == "og:url":
            m["content"] = "https://ankurnapa.github.io/disruptive-advantage/case-study-extract-loss.html"
    for l in s.find_all("link", rel="canonical"):
        l["href"] = "https://ankurnapa.github.io/disruptive-advantage/case-study-extract-loss.html"
    s.body["class"] = ["p-case-study-spirit-account"]  # keeps the page layout rules in site.css
    chrome(s)
    save("case-study-extract-loss.html", s)
    os.remove("case-study-spirit-account.html")


def redirect(old, new, title):
    open(old, "w").write(f'<!doctype html><html lang="en-AU"><head><meta charset="utf-8">'
                         f'<title>{title}</title><meta http-equiv="refresh" content="0; url={new}">'
                         f'<link rel="canonical" href="{new}"><meta name="robots" content="noindex"></head>'
                         f'<body><p>This page has moved to <a href="{new}">{new}</a>.</p></body></html>')


make_study()
PAGE_FIX = {"solutions.html": solutions, "features.html": features, "case-studies.html": case_studies,
            "contact.html": contact, "about.html": about, "careers.html": careers}
for f in sorted(glob.glob("*.html")):
    if f in ("beer.html", "case-study-spirit-account.html"):
        continue
    s = load(f)
    if not s.find("main"):
        continue
    chrome(s)
    if f in PAGE_FIX:
        PAGE_FIX[f](s)
    save(f, s)

# the shared shell the generators build from
# (string edits: they are fragments, and a parser would close their open tags)
p = os.path.join("_build", "shell_head.html")
h = open(p).read().replace('<a href="beer.html">Beer365</a>', '<a href="use-cases.html">Use cases</a>')
open(p, "w").write(h)
p = os.path.join("_build", "shell_foot.html")
t = open(p).read()
t = re.sub(r"<div>\s*<h5>Solutions</h5>.*?</div>", FOOT_COL, t, count=1, flags=re.S)
open(p, "w").write(t)
redirect("case-study-spirit-account.html", "case-study-extract-loss.html", "Moved | Beer365")
print("done")
