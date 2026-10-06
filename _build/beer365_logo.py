from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
def word(text, ttf, size, x0, base):
    f=TTFont(ttf); gs=f.getGlyphSet(); cmap=f.getBestCmap(); s=size/f["head"].unitsPerEm; x=x0; out=[]
    for ch in text:
        g=cmap[ord(ch)]; pen=SVGPathPen(gs); gs[g].draw(TransformPen(pen,(s,0,0,-s,x,base))); out.append(pen.getCommands()); x+=gs[g].width*s
    return " ".join(out), x
def width(text,ttf,size):
    return word(text,ttf,size,0,0)[1]
INK,YEL,GOLD="#0A0A0A","#F5E003","#E5B611"
PINT=lambda c: f'''<path d="M13.5 11.5h13l-1.8 16.6a1.6 1.6 0 0 1-1.6 1.4h-6.2a1.6 1.6 0 0 1-1.6-1.4z" fill="none" stroke="{c}" stroke-width="2.2" stroke-linejoin="round"/>
<path d="M14.1 15.3c1.2-1.1 2.5-1.1 3.7 0s2.5 1.1 3.7 0 2.5-1.1 3.7 0" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>
<path d="M16.8 25.4l2.4-2.8 2 1.5 2.6-4.3" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'''
# A: pint inside a ring with a gap, a year going round
RING=lambda ink: f'''<circle cx="20" cy="20" r="17.5" fill="none" stroke="{GOLD}" stroke-width="3.2" stroke-linecap="round" stroke-dasharray="102 8" transform="rotate(-62 20 20)"/>
<circle cx="31.8" cy="7.2" r="2.4" fill="{YEL}" stroke="{ink}" stroke-width="0"/>'''+PINT(ink)
# B: pint on a yellow disc
DISC=lambda ink: f'<circle cx="20" cy="20" r="20" fill="{YEL}"/>'+PINT("#0A0A0A")
def wordmark(ink, opt):
    if opt=="A":
        b,x=word("Beer","inter1.ttf",27,50,29.5); n,x2=word("365","inter0.ttf",27,x+1,29.5)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x2+2:.0f} 40" height="40">{RING(ink)}<path d="{b}" fill="{ink}"/><path d="{n}" fill="{ink}"/></svg>'
    if opt=="B":
        b,x=word("Beer","inter1.ttf",27,50,29.5); n,x2=word("365","inter0.ttf",27,x+1,29.5)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x2+2:.0f} 40" height="40">{DISC(ink)}<path d="{b}" fill="{ink}"/><path d="{n}" fill="{ink}"/></svg>'
    if opt=="C":   # "Beer" then 365 set inside a yellow circle
        b,x=word("Beer","inter1.ttf",29,0,30.5)
        nw=width("365","inter1.ttf",15.5); cx=x+4+20
        n,_=word("365","inter1.ttf",15.5,cx-nw/2,25.6)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cx+21:.0f} 40" height="40"><path d="{b}" fill="{ink}"/><circle cx="{cx:.1f}" cy="20" r="19.5" fill="{YEL}"/><path d="{n}" fill="#0A0A0A"/></svg>'
    if opt=="D":   # C plus a gold ring with a gap around the 365
        b,x=word("Beer","inter1.ttf",29,0,30.5)
        nw=width("365","inter1.ttf",14.5); cx=x+4+20
        n,_=word("365","inter1.ttf",14.5,cx-nw/2,25.2)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cx+21:.0f} 40" height="40"><path d="{b}" fill="{ink}"/>'
                f'<circle cx="{cx:.1f}" cy="20" r="17.6" fill="none" stroke="{GOLD}" stroke-width="3.2" stroke-linecap="round" stroke-dasharray="100 10.6" transform="rotate(-60 {cx:.1f} 20)"/>'
                f'<circle cx="{cx:.1f}" cy="20" r="13.2" fill="{YEL}"/><path d="{n}" fill="#0A0A0A"/></svg>')
for o in "ABCD":
    open(f"opt{o}.svg","w").write(wordmark("#0A0A0A",o)); open(f"opt{o}-light.svg","w").write(wordmark("#FFFFFF",o))
print("ok")
