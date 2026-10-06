"""Builds use-cases.html: every question Beer365 answers, grouped by area of the
beer business, from the vault catalogue (use_cases.json). Run after build_beer.py
re-extracts nothing; it reads the same shell files.  python3 _build/build_usecases.py"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from areas import AREAS, UC, WAVE, cases  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
E = lambda s: html.escape(s, quote=True)
TITLE = "Every question Beer365 answers | Beer365"
DESC = (f"{len(UC)} questions across the whole beer business, from the malt lot to the "
        "excise return, each answered from your own brewery's records.")

head = open(os.path.join(HERE, "shell_head.html")).read()
foot = open(os.path.join(HERE, "shell_foot.html")).read()
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, flags=re.S)
head = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{DESC}" name="description"/>', head)
head = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{TITLE}" property="og:title"/>', head)
head = re.sub(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{DESC}" property="og:description"/>', head)
head = head.replace('https://ankurnapa.github.io/disruptive-advantage/"', 'https://ankurnapa.github.io/disruptive-advantage/use-cases.html"')
head = head.replace('class="p-index"', 'class="p-index p-uc"')

chips = '<button class="chip is-on" type="button" data-area="all" aria-pressed="true">Everything</button>' + "".join(
    f'<button class="chip" type="button" data-area="{k}" aria-pressed="false">{E(n)}</button>' for k, n, _, _ in AREAS)


def item(u):
    w = u["when"]
    return (f'<li class="uc" data-wave="{w}"><p class="ucq">{E(u["q"])}</p>'
            f'<p class="uct">{E(u["title"])}<span class="wave w-{w.lower()}">{WAVE[w]}</span></p></li>')


groups = "".join(
    f'<section class="ucg" id="{k}" data-area="{k}"><div class="ucg-h"><h2>{E(n)}</h2>'
    f'<span class="ucn">{len(cases(a))} questions</span></div><p class="ucd">{E(d)}</p>'
    f'<ul class="ucl">{"".join(item(u) for u in cases(a))}</ul></section>'
    for a in AREAS for k, n, d, _ in [a])

MAIN = f'''<main id="main">
<section class="phero">
 <div class="wrap">
 <p class="kicker">Use cases</p>
 <h1>Every question Beer365 answers</h1>
 <p class="std">{len(UC)} questions across the whole beer business, from the malt lot to the excise return. Each one is answered from your own brewery&#39;s records, and each is marked by when we build it: the first wave goes live with your first modules.</p>
 </div>
</section>
<section class="tight ucbar">
 <div class="wrap">
 <div class="ucfilters" role="group" aria-label="Filter by area">{chips}</div>
 <div class="ucsearch"><label for="ucq" class="vh">Search the questions</label>
 <input id="ucq" type="search" placeholder="Search, for example: extract, keg, excise" autocomplete="off">
 <span class="uccount"><b id="ucShown">{len(UC)}</b> of {len(UC)} shown</span></div>
 </div>
</section>
<section>
 <div class="wrap">{groups}
 <p class="ucnone" id="ucNone" hidden>No question matches that. Try a shorter word, or <a href="contact.html?produce=beer">ask us yours</a>.</p>
 </div>
</section>
<section class="talk">
 <div class="wrap inner">
 <div><h2>Which question is <span>yours?</span></h2><p>Tell us the one that costs you most. We will show you how it is answered from your records.</p></div>
 <div class="talk-acts"><a class="btn" href="contact.html?produce=beer&amp;ask=The%20question%20that%20costs%20us%20most%20is%3A%20">Book a free demo</a>
 <p>or write to <a href="mailto:info@disruptive-advantage.com">info@disruptive-advantage.com</a></p></div>
 </div>
</section>
</main>
<script>
(function () {{
  'use strict';
  var chips = Array.prototype.slice.call(document.querySelectorAll('.ucfilters .chip'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('.ucg'));
  var q = document.getElementById('ucq'), shown = document.getElementById('ucShown'), none = document.getElementById('ucNone');
  var area = 'all';
  function run() {{
    var term = q.value.trim().toLowerCase(), n = 0;
    groups.forEach(function (g) {{
      var inArea = area === 'all' || g.getAttribute('data-area') === area, inG = 0;
      Array.prototype.forEach.call(g.querySelectorAll('.uc'), function (li) {{
        var ok = inArea && (!term || li.textContent.toLowerCase().indexOf(term) !== -1);
        li.hidden = !ok; if (ok) {{ inG++; }}
      }});
      g.hidden = inG === 0; n += inG;
    }});
    shown.textContent = String(n); none.hidden = n !== 0;
  }}
  function pick(a) {{
    area = a;
    chips.forEach(function (c) {{ var on = c.getAttribute('data-area') === a; c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', String(on)); }});
    run();
  }}
  chips.forEach(function (c) {{ c.addEventListener('click', function () {{ pick(c.getAttribute('data-area')); }}); }});
  q.addEventListener('input', run);
  var h = window.location.hash.slice(1);
  if (h && document.querySelector('.ucg[data-area="' + h + '"]')) {{ pick(h); }}
}})();
</script>'''

open(os.path.join(SITE, "use-cases.html"), "w").write(head + MAIN + foot)
print("use-cases.html", len(UC))
