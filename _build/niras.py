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


def parent(page):
    if page.startswith("article-"):
        return '<a href="articles.html">Articles</a><span aria-hidden="true">›</span>'
    if page.startswith("whitepaper-"):
        return '<a href="resources.html">Resources</a><span aria-hidden="true">›</span>'
    if page.startswith("case-study-"):
        return '<a href="case-studies.html">Case studies</a><span aria-hidden="true">›</span>'
    return ""


def video_tag(name):
    return (f'<video class="nhero-bg" autoplay muted loop playsinline preload="metadata" poster="assets/video/{name}.jpg" aria-hidden="true">'
            f'<source src="assets/video/{name}.mp4" type="video/mp4"></video>')


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
    hero = s[i:j].replace('<section class="phero">', f'<section class="phero nhero dark">\n{media(page, photo)}', 1)
    hero = re.sub(r'<p class="kicker">[^<]*</p>\s*', "", hero, count=1)
    crumb = (f'\n<nav aria-label="Breadcrumb" class="wrap ncrumb"><a href="index.html">Home</a><span aria-hidden="true">›</span>'
             f'{parent(page)}<span aria-current="page">{label}</span></nav>')
    return s[:i] + hero + crumb + s[j:]


def drop_old_crumb(s):
    # the NIRAS breadcrumb under the hero replaces the strip above it
    return re.sub(r'<div class="crumb"><div class="wrap">.*?</div></div>\n?', "", s, count=1)


def rules(s):
    # NIRAS has no kicker labels: the heading carries a rule under it instead
    s = re.sub(r'<p class="kicker">[^<]*</p>\s*<h2([^>]*)>', lambda m: '<h2 class="nrule"' + m.group(1).replace(' class="', ' data-c="') + '>', s)
    return s


def videos(page, s):
    # pages converted on an earlier run (and the hand built hero pages) swap their still for the clip
    if page not in VIDEO or '<video class="nhero-bg"' in s:
        return s
    return re.sub(r'<img alt="" class="nhero-bg"[^>]*/?>', video_tag(VIDEO[page]), s, count=1)


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


for path in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    page = os.path.basename(path)
    s = open(path).read()
    if "http-equiv=\"refresh\"" in s or len(s) < 2000:
        continue
    out = videos(page, rules(drop_old_crumb(convert(page, home(s) if page == "index.html" else s))))
    if out != s:
        open(path, "w").write(out)
        print(page)
