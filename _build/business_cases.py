"""Writes whitepapers/brewery-business-cases.json: modelled business cases at four
brewery sizes. Constants copied from vault Brewforce-Partner/pricing.py (the source
of the savings method), so the website, the price sheets and this paper agree.
These are planning figures, never customer results."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
BREW_COST_HL, GRAIN_HL, ENERGY_HL, BHE_BASE = 2000, 16 * 38, 200, 95   # INR per hL; efficiency %
def levers(hl):
    if hl <= 280_000: return (1.0, 1.0, 0.05, 500_000, 0.002)
    if hl <= 600_000: return (0.75, 0.75, 0.05, 800_000, 0.0015)
    return (0.5, 0.5, 0.04, 1_000_000, 0.001)
def sav(hl):
    l, e, en, rep, d = levers(hl)
    return {"Beer loss": hl * l / 100 * BREW_COST_HL, "Extract": hl * GRAIN_HL * e / BHE_BASE,
            "Energy": hl * ENERGY_HL * en, "Reporting": rep, "Dumped batches": hl * d * BREW_COST_HL}
SIZES = [(50_000, "Craft production brewery"), (150_000, "Regional brewery"), (500_000, "Large regional plant"), (1_000_000, "National brand plant")]
lakh = lambda v: f"{v / 100_000:,.1f}"
rows, summary = [], []
for hl, name in SIZES:
    s = sav(hl); t = sum(s.values())
    rows.append([f"{hl:,} hL", name] + [lakh(s[k]) for k in ("Beer loss", "Extract", "Energy", "Dumped batches", "Reporting")] + [lakh(t), lakh(t * 2.5), lakh(t * 2.5 / 2)])
    summary.append((hl, name, t))
paper = {
 "slug": "brewery-business-cases",
 "title": "Brewery business cases: what one batch record is worth at four sizes",
 "subtitle": "Modelled savings for a 50,000 to 1,000,000 hL brewery, with every assumption on the page and a conservative case beside the base case.",
 "description": "Modelled brewery business cases at four sizes: beer loss, extract, energy, dumped batches and reporting savings, with assumptions and a conservative case.",
 "keywords": ["brewery business case", "brewery ROI", "beer loss savings", "brewhouse efficiency savings", "brewery data investment"],
 "date": "2026-10-06",
 "kind": "Business cases",
 "summary": [f"A {SIZES[1][0]:,} hL regional brewery models at INR {lakh(summary[1][2])} lakh a year once live." ,
             f"At {SIZES[3][0]:,} hL the model gives INR {lakh(summary[3][2])} lakh a year, even with half the improvement assumed for smaller plants.",
             "Beer loss and extract are most of the value at every size; reporting time is the smallest line.",
             "If only half of each improvement happens, every figure halves, and the three-year value still covers a substantial cost.",
             "These are planning figures from published assumptions, not results from a named brewery."],
 "sections": [
  {"h2": "Read this first", "blocks": [
   {"p": "These are modelled business cases, not customer results. Beer365 has no signed customer saving to publish yet, and we will not dress a model up as one. What a finance director can do with this page is check the arithmetic, replace any assumption with their own and see what the investment has to clear."},
   {"p": "Money is in Indian rupees because the cost assumptions come from Indian brewing costs. One lakh is 100,000. The method works in any currency: swap the three cost figures for your own."}]},
  {"h2": "The assumptions", "blocks": [
   {"table": {"head": ["Input", "Value", "Why"], "rows": [
     ["Brewing cost of beer", "INR 2,000 per hL", "Malt, adjunct, hops, energy and water. Lost beer is valued at cost, not selling price."],
     ["Malt and adjunct cost", "INR 608 per hL", "16 kg of grist per hL at INR 38 per kg."],
     ["Energy cost", "INR 200 per hL", "About 10 kWh of power at INR 8 and 120 MJ of steam at INR 1."],
     ["Beer loss recovered", "1 point (0.75 above 280,000 hL, 0.5 above 600,000 hL)", "Larger plants already run tighter."],
     ["Brewhouse efficiency gained", "1 point on a 95 percent base (scaled the same way)", "Each brew compared with the malt's lab value."],
     ["Energy saved", "5 percent (4 percent above 600,000 hL)", "Power and steam tracked by area against the best day."],
     ["Dumped batches avoided", "0.2 percent of volume (0.15 and 0.1 for larger plants)", "Fermentation drift caught early."],
     ["Reporting time", "INR 5 to 10 lakh a year", "Manual daily, weekly and month-end packs."],
     ["Year one", "Half the annual saving", "The system goes live during the year."]]}}]},
  {"h2": "The four cases", "blocks": [
   {"p": "Annual savings once live, in INR lakh. The three-year figure counts half a year's saving in year one and full savings in years two and three. The conservative column assumes only half of every improvement happens."},
   {"table": {"head": ["Volume a year", "Beer loss", "Extract", "Energy", "Dumped", "Reporting", "Total a year"], "rows": [[r[0]] + r[2:8] for r in rows]}},
   {"p": "And what each is worth over three years, in INR lakh:"},
   {"table": {"head": ["Volume a year", "Brewery", "A year once live", "Three years", "Three years, conservative"], "rows": [[r[0], r[1], r[7], r[8], r[9]] for r in rows]}}]},
  {"h2": "How to read the cases", "blocks": [
   {"ul": ["Beer loss and extract carry most of the value at every size, because they scale with volume and are valued at real cost.",
           "Energy matters more as plants grow, but large plants already meter better, so the assumed share falls.",
           "Reporting time is the smallest line and the most certain one: the reports either build themselves or they do not.",
           "The break-even question is simple: if the full three-year cost of the system, Microsoft bills included, is below the conservative three-year figure, it pays back even if half of what we assume never happens."]}]},
  {"h2": "How a modelled figure becomes a real one", "blocks": [
   {"p": "In the assessment the first month runs on your own records and we sign the starting point off with you. Every month after that, loss, extract and energy are counted against that baseline, in hectolitres and in money, adjusted for volume, and signed by your plant controller. Only those signed figures are ever called savings. When we publish a result, it is a signed saving over a stated period, less 25 percent for risk."},
   {"p": "To run these numbers on your own brewery, use the readiness workbook or the calculator on this site."}]}],
 "sources": ["Savings method and constants: Beer365 savings method (vault Brewforce-Partner/pricing.py), September 2026",
             "Brewing cost basis: Indian brewing input costs as used in the savings method"]}
os.makedirs(os.path.join(HERE, "whitepapers"), exist_ok=True)
json.dump(paper, open(os.path.join(HERE, "whitepapers", "brewery-business-cases.json"), "w"), indent=1, ensure_ascii=False)
for r in rows: print(r)
