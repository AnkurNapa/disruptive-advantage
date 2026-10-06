"""Puts the site's one icon family into every page, and tidies the form markup so
all forms share one system. Idempotent: an element that already carries an icon
is left alone. Runs near the end of build_all.sh, before stamping.

  python3 _build/apply_icons.py
"""
import glob
import os
import re
import sys

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from icons import AREA_ICON, MODULE_ICON, badge, icon  # noqa: E402

frag = lambda h: BeautifulSoup(h, "html.parser")
TRUST = ["shield", "eye", "filecheck", "key"]
CONTACT_H4 = {"General enquiries": "mail", "Ankur Napa": "user", "Australia": "pin", "India": "pin", "Careers": "briefcase"}


def has_icon(el):
    return el.find("svg", class_="ic") is not None or el.find(class_="badge") is not None


def inline_icons(s):
    """Small icons in front of phone numbers, emails and downloads."""
    for a in s.find_all("a", href=True):
        if has_icon(a):
            continue
        h = a["href"]
        if a.find_parent(class_=["sharebtn", "share"]) or "sharebtn" in a.get("class", []):
            continue
        if h.startswith("tel:"):
            a.insert(0, frag(icon("phone", "ic sm")))
        elif h.startswith("mailto:") and "@" in a.get_text():
            a.insert(0, frag(icon("mail", "ic sm")))
        elif a.has_attr("download"):
            a.insert(0, frag(icon("download", "ic")))
        elif "linkedin.com/in/" in h and a.get_text(strip=True).startswith("Ankur on LinkedIn"):
            a.insert(0, frag(icon("linkedin", "ic sm")))


def badges(s):
    for a in s.select("a.area"):
        if not has_icon(a):
            k = a["href"].split("#")[-1]
            if k in AREA_ICON:
                img = a.find("img")
                if img:
                    img.insert_after(frag(badge(AREA_ICON[k])))
                else:
                    a.insert(0, frag(badge(AREA_ICON[k])))
    for sec in s.select("section.solarea"):
        k = sec.get("id")
        kick = sec.select_one(".stext .kicker")
        if kick and k in AREA_ICON and not has_icon(sec.select_one(".stext")):
            kick.insert_before(frag(badge(AREA_ICON[k])))
    for card in s.select("article.mcard"):
        num = card.select_one(".num")
        if num and not has_icon(card):
            n = num.get_text(strip=True)
            if n in MODULE_ICON:
                num.insert_before(frag(badge(MODULE_ICON[n])))
    for i, k in enumerate(s.select(".trustg .kpi")):
        if not has_icon(k) and i < len(TRUST):
            k.insert(0, frag(badge(TRUST[i])))
    if s.body and "p-contact" in s.body.get("class", []):
        for h in s.find_all("h4"):
            t = h.get_text(strip=True)
            if t in CONTACT_H4 and not has_icon(h):
                h.insert(0, frag(icon(CONTACT_H4[t], "ic h4ic")))


def forms(s):
    """One form system: labelled controls, a real submit button, helpful notes."""
    for b in s.select("button.sub"):
        b["class"] = ["btn", "sub"]
        if not has_icon(b):
            b.insert(0, frag(icon("send", "ic")))
    for b in s.select(".form button"):
        if b.get_text(strip=True) == "Submit":
            b.string = "Subscribe"
        b["class"] = ["btn"]
    for p in s.select("p.formnote"):
        if not has_icon(p):
            p.insert(0, frag(icon("info", "ic sm")))
    for pill in s.select("button.pill"):
        if not pill.find("svg"):
            pill.insert(0, frag(icon("check", "ic tick")))


def main():
    pages = [p for p in glob.glob(os.path.join(SITE, "*.html")) if 'http-equiv="refresh"' not in open(p).read()]
    for p in pages:
        s = BeautifulSoup(open(p), "html.parser")
        inline_icons(s)
        badges(s)
        forms(s)
        open(p, "w").write(str(s))
    # the shared footer used by the generators
    f = os.path.join(HERE, "shell_foot.html")
    t = open(f).read()
    if 'class="ic sm"' not in t:
        t = re.sub(r'(<a href="tel:[^"]*">)', r"\1" + icon("phone", "ic sm"), t)
        t = re.sub(r'(<a href="mailto:[^"]*"[^>]*>)(?=[^<]*@)', r"\1" + icon("mail", "ic sm"), t)
        open(f, "w").write(t)
    print(len(pages), "pages iconed")


if __name__ == "__main__":
    main()
