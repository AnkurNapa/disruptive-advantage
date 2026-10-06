"""Beer365 logo: a yellow tile holding a pint glass with a rising data line in it,
then the wordmark. Letters are converted to outlines so the SVG renders the same
in an <img>, a favicon or a document, with no font loading."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

def word(text, ttf, size, x0, base):
    f = TTFont(ttf); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm
    s = size / upm; x = x0; out = []
    for ch in text:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, base)))
        out.append(pen.getCommands()); x += gs[g].width * s
    return " ".join(out), x

MARK = '''<rect width="40" height="40" rx="10" fill="#F5E003"/>
<path d="M11.5 9.5h17l-2.3 21.2a2 2 0 0 1-2 1.8h-8.4a2 2 0 0 1-2-1.8z" fill="none" stroke="#0A0A0A" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M12.2 14.2c1.6-1.4 3.2-1.4 4.8 0s3.2 1.4 4.8 0 3.2-1.4 4.8 0" fill="none" stroke="#0A0A0A" stroke-width="2" stroke-linecap="round"/>
<path d="M15.6 27l3.1-3.6 2.6 1.9 3.4-5.6" fill="none" stroke="#0A0A0A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'''

def build(ink, name):
    beer, x = word("Beer", "inter1.ttf", 27, 50, 29.5)
    num, x2 = word("365", "inter0.ttf", 27, x + 1, 29.5)
    w = round(x2 + 2)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40" role="img" aria-label="Beer365">'
           f'<title>Beer365</title>{MARK}<path d="{beer}" fill="{ink}"/><path d="{num}" fill="{ink}"/></svg>')
    open(name, "w").write(svg); return w

print(build("#0A0A0A", "beer365-logo.svg"), build("#FFFFFF", "beer365-logo-light.svg"))
open("beer365-mark.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="40" height="40">{MARK}</svg>')
