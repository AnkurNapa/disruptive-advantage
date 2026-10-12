"""Give every page the niras.com anatomy: a full bleed photo (or video) hero,
a breadcrumb under it and ruled headings in place of kicker labels.
Idempotent; runs after the page builders in build_all.sh.

  python3 _build/niras.py
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
ART_PHOTO = json.load(open(os.path.join(HERE, "article_photos.json")))
PAGES = {  # page: (crumb label, photo); parents are worked out from the name
    "about.html": ("About", "business"), "careers.html": ("Careers", "plant-2"),
    "case-studies.html": ("Case studies", "packaging"), "contact.html": ("Contact", "market-2"),
    "credits.html": ("Photo credits", "layer-2"), "features.html": ("Features", "layer"),
    "pricing.html": ("Pricing", "business-2"), "roi.html": ("Calculator", "quality"),
    "resources.html": ("Resources", "cellar-2"), "articles.html": ("Articles", "brewhouse"),
    "case-study-extract-loss.html": ("Extract loss", "raw-2"),
    "whitepaper-state-of-beer-ai-2026.html": ("State of beer AI 2026", "layer"),
    "whitepaper-brewery-business-cases.html": ("Brewery business cases", "business-2"),
    "whitepaper-how-beer-ai-vendors-prove-value.html": ("How vendors prove value", "quality-2"),
}
VIDEO = json.load(open(os.path.join(HERE, "videos.json"))) if os.path.exists(os.path.join(HERE, "videos.json")) else {}


COMPACT = ("article-", "whitepaper-", "case-study-")


def parent(page):
    if page.startswith("article-"):
        return '<a href="articles.html">Articles</a><span aria-hidden="true">›</span>'
    if page.startswith("whitepaper-"):
        return '<a href="resources.html">Resources</a><span aria-hidden="true">›</span>'
    if page.startswith("case-study-"):
        return '<a href="case-studies.html">Case studies</a><span aria-hidden="true">›</span>'
    return ""


def video_tag(name):
    # no <source> here: site.js attaches it on wide screens without data saver or reduced motion
    return (f'<video class="nhero-bg" muted loop playsinline preload="none" poster="assets/video/{name}.jpg" '
            f'data-src="assets/video/{name}.mp4" aria-hidden="true"></video>')


def media(page, photo):
    if page in VIDEO:
        return video_tag(VIDEO[page])
    return f'<img alt="" class="nhero-bg" fetchpriority="high" height="700" src="assets/photos/{photo}.jpg" width="1200"/>'


def convert(page, s):
    if '<section class="phero">' not in s:
        return s
    if page.startswith("article-"):
        label, photo = re.search(r"<h1>(.*?)</h1>", s).group(1), ART_PHOTO.get(page, "brewhouse")
    else:
        label, photo = PAGES[page]
    i = s.index('<section class="phero">')
    j = s.index("</section>", i) + len("</section>")
    compact = " ncompact" if page.startswith(COMPACT) or page == "contact.html" else ""
    hero = s[i:j].replace('<section class="phero">', f'<section class="phero nhero dark{compact}">\n{media(page, photo)}', 1)
    hero = re.sub(r'<p class="kicker">[^<]*</p>\s*', "", hero, count=1)
    crumb = (f'\n<nav aria-label="Breadcrumb" class="wrap ncrumb"><a href="index.html">Home</a><span aria-hidden="true">›</span>'
             f'{parent(page)}<span aria-current="page">{label}</span></nav>')
    return s[:i] + hero + crumb + s[j:]


def drop_old_crumb(s):
    # the NIRAS breadcrumb under the hero replaces the strip above it
    return re.sub(r'<div class="crumb"><div class="wrap">.*?</div></div>\n?', "", s, count=1)


def drop_hero_figure(s):
    # the article photo is already the hero background; showing it again pushes the text a screen down
    return re.sub(r'<figure class="ahero">.*?</figure>\s*', "", s, count=1, flags=re.S)


def rules(s):
    # NIRAS has no kicker labels: the heading carries a rule under it instead
    s = re.sub(r'<p class="kicker">[^<]*</p>\s*<h2([^>]*)>', lambda m: '<h2 class="nrule"' + m.group(1).replace(' class="', ' data-c="') + '>', s)
    return s


def videos(page, s):
    """Bring an already converted page up to date: current clip (or the still), compact hero where it belongs."""
    old = re.search(r'<video[^>]*class="nhero-bg"[^>]*>.*?</video>|<img[^>]*class="nhero-bg"[^>]*/?>', s, flags=re.S)
    if not old:
        return s
    if page in VIDEO:
        new = video_tag(VIDEO[page])
    else:
        photo = PAGES.get(page, ("", "brewhouse"))[1] if not page.startswith("article-") else ART_PHOTO.get(page, "brewhouse")
        new = old.group(0) if old.group(0).startswith("<img") else f'<img alt="" class="nhero-bg" fetchpriority="high" height="700" src="assets/photos/{photo}.jpg" width="1200"/>'
    if re.sub(r"\s+", " ", old.group(0)) == new or ('data-src="assets/video/' + VIDEO.get(page, "?") + '.mp4"') in old.group(0):
        new = old.group(0)  # already current (attribute order may differ after the icon pass)
    s = s.replace(old.group(0), new, 1)
    if (page.startswith(COMPACT) or page == "contact.html") and "ncompact" not in s:
        s = re.sub(r'<section class="phero nhero dark"', '<section class="phero nhero dark ncompact"', s, count=1)
    return s


def home(s):
    """index.html is rebuilt by build_beer.py; reshape it on the niras.com homepage."""
    if '<section class="hero xh dark">' not in s:
        return s
    sol = open(os.path.join(SITE, "solutions.html")).read()

    def section(html, start):
        i = html.index(start)
        return i, html.index("</section>", i) + len("</section>")

    # 1. hero -> NIRAS photo hero, breadcrumb, feature split, selected work
    i, j = section(s, '<section class="hero xh dark">')
    old = s[i:j]
    h1 = re.search(r"<h1>.*?</h1>", old).group(0)
    lead = re.search(r'<p class="std">.*?</p>', old).group(0).replace(' class="std"', "")
    acts = re.search(r'<div class="acts">.*?</div>', old, re.S).group(0)
    note = re.search(r'<p class="cta-note">.*?</p>', old).group(0)
    wi, wj = section(s, '<section class="whole">')
    whole = s[wi:wj]
    wh2 = re.search(r"<h2>.*?</h2>", whole).group(0)
    wstd = re.search(r'<p class="std">.*?</p>', whole).group(0)
    ni, nj = section(sol, '<section class="nwork">')
    hero = f'''<section class="nhero dark">
    <img alt="" class="nhero-bg" fetchpriority="high" height="700" src="assets/photos/brewhouse.jpg" width="1200"/>
    <div class="wrap">
    {h1}
    {lead}
    {acts}
    {note}
    </div>
    </section>
    <nav aria-label="Breadcrumb" class="wrap ncrumb"><span aria-current="page">Home</span></nav>
    <section class="nfeature">
    <div class="wrap nsplit">
    <img alt="" height="700" loading="lazy" src="assets/photos/cellar.jpg" width="1200"/>
    <div>
    {wh2}
    {wstd}
    <a class="txtlink" href="solutions.html">See the full solution</a>
    </div>
    </div>
    </section>
    {sol[ni:nj]}'''
    s = s[:i] + hero + s[j:]

    # 2. nine area cards -> NIRAS service list, pointing at the solutions page
    wi, wj = section(s, '<section class="whole">')
    ai, aj = section(sol, '<section class="nareas">')
    s = s[:wi] + sol[ai:aj].replace('href="#', 'href="solutions.html#') + s[wj:]

    # 3. NIRAS newsletter band -> savings calculator band, before the method
    band = '''<section class="nband">
    <div class="wrap inner">
    <div><h2>Work out what your losses are worth</h2><p>Your volume, times the improvement, times what it is worth. Five formulas, no black box.</p></div>
    <a class="btn" href="roi.html">Work out my savings</a>
    </div>
    </section>
    '''
    s = s.replace('<section class="tinted" id="method">', band + '<section class="tinted" id="method">', 1)

    # 4. kicker + h2 -> NIRAS ruled heading
    s = re.sub(r'<p class="kicker">[^<]*</p>\s*<h2([^>]*)>', r'<h2 class="nrule"\1>', s)
    s = s.replace('<h2 class="nrule" style="color:#fff">', '<h2 class="nrule">')

    # 5. who builds it -> NIRAS "Join us" split
    s = s.replace('<div class="wrap team">', '<div class="wrap team njoin">', 1)
    return s


HOME_ORDER = ["nhero", "pains", "nfeature", "nareas", "appshow", "nband", "method", "proof", "poc", "ask",
              "trust", "team", "market", "nwork", "faq", "talk"]
HOME_KEY = {"nhero": 'class="nhero', "pains": 'class="pains"', "nfeature": 'class="nfeature"', "nareas": 'class="nareas"',
            "appshow": 'class="appshow"', "nband": 'class="nband"', "method": 'id="method"', "proof": "modlist proof",
            "poc": 'class="weeks"', "ask": 'class="ask"', "trust": "trustg", "team": "njoin", "market": "dark market",
            "nwork": 'class="nwork"', "faq": 'id="faq"', "talk": 'class="talk"'}
BANDED = {"pains", "nfeature", "nareas", "appshow", "method", "proof", "poc", "trust", "team", "nwork", "faq"}


def home_story(s):
    """Problem first, then what it is, what it saves, the proof, trust and the questions."""
    if 'data-story="1"' in s:
        return s
    a, b = s.index('<main id="main">') + len('<main id="main">'), s.index("</main>")
    secs = re.findall(r"<section.*?</section>", s[a:b], flags=re.S)
    by = {k: next(x for x in secs if HOME_KEY[k] in x) for k in HOME_ORDER}
    assert len(secs) == len(HOME_ORDER), [x[:60] for x in secs]
    # the five formulas stay one click away instead of filling three screens
    m = by["method"]
    i, j = m.index('<div class="leaks">'), m.rindex("</div>\n</section>")
    by["method"] = m[:i] + '<details class="nmore"><summary>See the five formulas and what we never count</summary>' + m[i:j] + "</details>\n" + m[j:]
    # the savings band straight above already carries this button
    by["method"] = re.sub(r'<a class="btn" href="roi.html">Work out my savings</a>', "", by["method"], count=1)
    by["nwork"] = by["nwork"].replace("Selected work:", "Read before you call")
    out, band = [], False
    for k in HOME_ORDER:
        x = re.sub(r'^<section class="([^"]*)"', lambda m: '<section class="' + " ".join(c for c in m.group(1).split() if c != "tinted") + '"', by[k])
        x = x.replace('<section class="">', "<section>", 1).replace('<section class="" ', "<section ", 1)
        if k in BANDED:
            if band:
                x = x.replace("<section>", '<section class="tinted">', 1) if x.startswith("<section>") else x.replace('<section class="', '<section class="tinted ', 1)
            band = not band
        out.append(x)
    return s[:a] + "\n" + "\n".join(out).replace("<section", '<section data-story="1"', 1) + "\n" + s[b:]


for path in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    page = os.path.basename(path)
    s = open(path).read()
    if "http-equiv=\"refresh\"" in s or len(s) < 2000:
        continue
    out = videos(page, rules(drop_hero_figure(drop_old_crumb(convert(page, home(s) if page == "index.html" else s)))))
    out = home_story(out) if page == "index.html" else out
    if out != s:
        open(path, "w").write(out)
        print(page)
