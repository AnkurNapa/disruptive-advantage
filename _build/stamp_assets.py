"""Cache-busting: point every page at assets/*.css|js?v=<content hash>, so a
deploy never shows new pages with a stylesheet the browser cached earlier
(GitHub Pages lets browsers keep assets for 10 minutes). Run last."""
import glob
import hashlib
import os
import re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = ["assets/site.css", "assets/theme.css", "assets/site.js", "assets/beer365-logo.svg", "assets/beer365-mark.svg"]
ver = {a: hashlib.sha1(open(os.path.join(SITE, a), "rb").read()).hexdigest()[:8] for a in ASSETS}
n = 0
for f in glob.glob(os.path.join(SITE, "*.html")) + [os.path.join(SITE, "_build", "shell_head.html"), os.path.join(SITE, "_build", "shell_foot.html")]:
    s = open(f).read()
    t = s
    for a, v in ver.items():
        t = re.sub(re.escape(a) + r'(\?v=[0-9a-f]+)?"', f'{a}?v={v}"', t)
    if t != s:
        open(f, "w").write(t)
        n += 1
print(n, "files stamped", ver)
