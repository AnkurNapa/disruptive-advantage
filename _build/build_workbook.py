"""Beer365 Readiness Workbook: what a brewery fills in to be ready for Beer365.

  python3 _build/build_workbook.py   ->  downloads/Beer365-Readiness-Workbook.xlsx

Yellow cells are the brewery's inputs; everything else is a formula. The savings
sheet uses the same five formulas as the website's savings method.
"""
import os
import sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from areas import AREAS, UC, WAVE  # noqa: E402

OUT = os.path.join(SITE, "downloads", "Beer365-Readiness-Workbook.xlsx")
F = "Arial"
INK, YEL, GOLD, CREAM, BAND = "0A0A0A", "F5E003", "E5B611", "FEFBE0", "F6F4EC"
H1 = Font(name=F, size=18, bold=True, color=INK)
H2 = Font(name=F, size=12, bold=True, color=INK)
HEAD = Font(name=F, size=10, bold=True, color="FFFFFF")
BODY = Font(name=F, size=10, color=INK)
MUTED = Font(name=F, size=9, color="6B6A63", italic=True)
INPUT = Font(name=F, size=10, color="0000FF")
EX = Font(name=F, size=10, color="77756C", italic=True)
FILL_HEAD = PatternFill("solid", fgColor=INK)
FILL_IN = PatternFill("solid", fgColor=YEL)
FILL_CREAM = PatternFill("solid", fgColor=CREAM)
FILL_BAND = PatternFill("solid", fgColor=BAND)
THIN = Side(style="thin", color="DEDBD0")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

wb = Workbook()


def sheet(title, widths):
    ws = wb.create_sheet(title)
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws


def header(ws, row, labels):
    for i, t in enumerate(labels, 1):
        c = ws.cell(row, i, t)
        c.font, c.fill, c.alignment, c.border = HEAD, FILL_HEAD, Alignment(wrap_text=True, vertical="center"), BOX
    ws.row_dimensions[row].height = 30


def title(ws, text, sub):
    ws["A1"], ws["A2"] = text, sub
    ws["A1"].font, ws["A2"].font = H1, MUTED
    ws.row_dimensions[1].height = 28


def inp(c, value=None):
    c.fill, c.font, c.border = FILL_IN, INPUT, BOX
    if value is not None:
        c.value = value
    return c


def body(c, value=None, fmt=None):
    c.font, c.border, c.alignment = BODY, BOX, WRAP
    if value is not None:
        c.value = value
    if fmt:
        c.number_format = fmt
    return c


# ---- 1. Start here --------------------------------------------------------------------
ws = wb.active
ws.title = "Start here"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 4
ws.column_dimensions["B"].width = 28
ws.column_dimensions["C"].width = 90
ws["B2"] = "Beer365 Readiness Workbook"
ws["B2"].font = Font(name=F, size=22, bold=True, color=INK)
ws["B3"] = "What to gather before a Beer365 assessment, and a first look at what your brewery could save."
ws["B3"].font = MUTED
rows = [
    ("How to use it", "Fill the yellow cells only. Everything else is a formula and updates as you type. Grey italic rows are examples showing the expected format; overwrite or delete them."),
    ("1 Brewery profile", "Volumes, costs and the assumptions every other sheet uses. Ten minutes."),
    ("2 Records", "Where each record your brewery keeps actually lives, and how much you trust it. This is the biggest single predictor of how fast Beer365 goes live."),
    ("3 Meters", "The measurement points the savings depend on, and when each was last calibrated."),
    ("4 Baseline", "Up to twelve months of plant figures. Loss, brewhouse yield, energy and water ratios are worked out for you."),
    ("5 Savings", "The five savings formulas from beer365 (beer loss, extract, energy, dumped batches, reporting), fed by your own numbers. Planning figures, not a promise: the real starting point is measured and signed in the assessment."),
    ("6 Questions", "All 221 questions Beer365 answers. Score how much each matters and whether you have the data; the priority column ranks them."),
    ("7 Readiness", "One page summary: records, meters, baseline coverage and an overall readiness score."),
    ("When you are done", "Send the workbook to info@disruptive-advantage.com, or bring it to the first call. We read it before we meet."),
    ("Colour legend", "Yellow fill and blue text: your input. Black text: a formula. Do not overwrite formulas."),
    ("Your data", "Nothing in this file leaves your hands unless you send it. It contains no macros and no links."),
]
r = 5
for k, v in rows:
    ws.cell(r, 2, k).font = H2
    c = ws.cell(r, 3, v)
    c.font, c.alignment = BODY, WRAP
    ws.row_dimensions[r].height = 32 if len(v) > 95 else 18
    r += 1
ws.cell(r + 1, 2, "Beer365, built by Disruptive Advantage. ankurnapa.github.io/disruptive-advantage").font = MUTED

# ---- 2. Brewery profile -------------------------------------------------------------------
pf = sheet("1 Profile", [44, 18, 18, 60, 18])
title(pf, "Brewery profile", "Yellow cells are yours. The example column shows the expected format.")
header(pf, 4, ["Item", "Your brewery", "Example", "Why we ask", "Used in the sheets"])
PROFILE = [
    ("Brewery name", None, "Example Brewing Co", "", "@"),
    ("Currency used below", None, "INR", "Every money figure in this workbook is in this currency.", "@"),
    ("Beer packaged a year (hL)", None, 120000, "Drives every saving.", "#,##0"),
    ("Brews a week", None, 18, "", "#,##0"),
    ("Number of fermenters and unitanks", None, 15, "", "#,##0"),
    ("Packaging lines (bottle, can, keg)", None, 3, "", "#,##0"),
    ("Malt and adjunct charged a year (kg)", None, 2100000, "Base for extract and brewhouse yield.", "#,##0"),
    ("Malt and adjunct cost per kg", None, 45, "Hypothetical example price.", "#,##0.00"),
    ("Average extract of the grist, as-is (%)", None, 0.78, "From the malt certificates; fine grind, as-is basis.", "0.0%"),
    ("Brewing cost per hL (malt, hops, energy, water)", None, 2000, "Lost beer is valued at cost to make, not selling price.", "#,##0"),
    ("Energy cost per hL (power plus steam)", None, 200, "Or leave blank and use the Baseline sheet.", "#,##0"),
    ("Brewhouse efficiency today (%)", None, 0.92, "If you know it. The Baseline sheet also works it out.", "0.0%"),
    ("Hours a week spent compiling reports by hand", None, 20, "All people, all reports.", "#,##0"),
    ("Cost of an hour of that time", None, 600, "Loaded cost.", "#,##0"),
    ("Main ERP or accounting system", None, "Excel", "", "@"),
    ("Process historian or SCADA", None, "None", "", "@"),
    ("Laboratory system (LIMS) or lab sheets", None, "Excel lab sheets", "", "@"),
    ("Cloud you already use (Azure, AWS, Google, none)", None, "Microsoft 365 only", "Beer365 runs in your own Azure tenant; it can read data held on AWS or Google.", "@"),
]
PROF = {}
for i, (k, _, ex, why, fmt) in enumerate(PROFILE):
    rr = 5 + i
    body(pf.cell(rr, 1), k)
    inp(pf.cell(rr, 2)).number_format = fmt
    e = pf.cell(rr, 3, ex)
    e.font, e.border, e.number_format = EX, BOX, fmt
    body(pf.cell(rr, 4), why)
    u = body(pf.cell(rr, 5), f'=IF(B{rr}="",C{rr},B{rr})', fmt)
    u.fill = FILL_BAND
    PROF[k] = f"'1 Profile'!$E${rr}"
pf.cell(5 + len(PROFILE) + 1, 1, "Until you fill a yellow cell, the sheets use the example value beside it, so the savings page shows a worked example from the start.").font = MUTED

# ---- 3. Records -------------------------------------------------------------------------
RECORDS = {
    "raw": ["Malt certificates of analysis by lot", "Hop certificates and alpha acid by lot", "Water analysis", "Goods received and lot numbers", "Recipes and specifications"],
    "brewhouse": ["Brew sheets (grist, volumes, gravities, times)", "Mash and kettle temperature logs", "Wort volumes at kettle and knockout"],
    "cellar": ["Fermentation gravity and temperature readings", "Yeast pitch, generation and viability", "Tank transfers and losses", "Filtration and bright beer tank records"],
    "packaging": ["Line counts, rejects and downtime", "Fill level and dissolved oxygen checks", "Packaging material lots", "Date codes against tank and batch"],
    "quality": ["Laboratory results by batch", "Sensory panel results", "Complaints log", "Micro results by sample point", "CIP records"],
    "plant": ["Power meter readings by area", "Steam or fuel use", "Water meter readings", "Refrigeration and compressor logs", "Maintenance work orders"],
    "market": ["Stock and warehouse movements", "Sales by SKU, channel and outlet", "Distributor depletions", "Keg fleet and returns"],
    "business": ["Excise or duty register", "Cost of goods by brand and pack", "Shift logs and handovers", "Monthly management reports"],
}
WHERE = ["Paper", "Excel or Google Sheets", "ERP", "SCADA or historian", "LIMS or lab system", "Other software", "Not kept"]
rc = sheet("2 Records", [30, 46, 22, 16, 16, 12, 14, 36])
title(rc, "Where your records live", "One row per record. Choose where it is kept, how often it is updated, and how much you trust it (1 low to 5 high).")
header(rc, 4, ["Area", "Record", "Where it is kept", "How often", "Owner", "Trust 1 to 5", "Ready score", "Notes"])
dv_where = DataValidation(type="list", formula1='"' + ",".join(WHERE) + '"', allow_blank=True)
dv_freq = DataValidation(type="list", formula1='"Live,Each batch,Daily,Weekly,Monthly,Rarely"', allow_blank=True)
dv_trust = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True)
for d in (dv_where, dv_freq, dv_trust):
    rc.add_data_validation(d)
r = 5
names = {k: n for k, n, _, _ in AREAS}
first = True
for area, recs in RECORDS.items():
    for rec in recs:
        body(rc.cell(r, 1), names[area])
        body(rc.cell(r, 2), rec)
        for col, dv in ((3, dv_where), (4, dv_freq), (5, None), (6, dv_trust)):
            inp(rc.cell(r, col))
            if dv:
                dv.add(rc.cell(r, col))
        if first:  # one example row, as the legend says
            for col, v in ((3, "Excel or Google Sheets"), (4, "Each batch"), (5, "Quality manager"), (6, 4)):
                rc.cell(r, col).value = v
            rc.cell(r, 8).value = "Example row: overwrite with your own"
            rc.cell(r, 8).font = EX
            first = False
        body(rc.cell(r, 7), f'=IF(C{r}="","",IF(C{r}="Not kept",0,IF(F{r}="",0.5,F{r}/5)*IF(C{r}="Paper",0.5,1)))', "0%")
        inp(rc.cell(r, 8)) if rc.cell(r, 8).value is None else None
        r += 1
REC_LAST = r - 1
rc.cell(r + 1, 1, "Ready score: 0 if not kept; trust out of 5, halved for paper records because they have to be keyed in first.").font = MUTED
rc.freeze_panes = "C5"

# ---- 4. Meters -------------------------------------------------------------------------
METERS = ["Malt intake weigher or silo load cells", "Hot liquor and sparge water flow", "Wort flow or volume at knockout", "Wort gravity at knockout (density meter or lab)",
          "Fermenter level or volume", "Fermenter temperature probes", "Inline gravity in fermentation (if fitted)", "Bright beer tank level",
          "Dissolved oxygen meter (packaging)", "Filler counters and rejects", "Keg fill weight scale", "Main power meter", "Power meters by area",
          "Steam or boiler fuel meter", "Main water meter", "Water meters by area", "CO2 recovery and purchase meter", "Refrigeration plant power"]
mt = sheet("3 Meters", [46, 14, 18, 16, 40])
title(mt, "Meters and instruments", "Is it fitted, and when was it last calibrated? Savings are only as good as the meter behind them.")
header(mt, 4, ["Measurement point", "Fitted?", "Last calibrated", "Within 12 months", "Notes"])
dv_yn = DataValidation(type="list", formula1='"Yes,No,Partly"', allow_blank=True)
mt.add_data_validation(dv_yn)
for i, m in enumerate(METERS):
    rr = 5 + i
    body(mt.cell(rr, 1), m)
    dv_yn.add(inp(mt.cell(rr, 2)))
    inp(mt.cell(rr, 3)).number_format = "dd mmm yyyy"
    body(mt.cell(rr, 4), f'=IF(C{rr}="",IF(B{rr}="No","Not fitted",""),IF(TODAY()-C{rr}<=365,"Yes","Overdue"))')
    inp(mt.cell(rr, 5))
MET_LAST = 5 + len(METERS) - 1
mt["B5"], mt["C5"], mt["E5"] = "Yes", 46023, "Example row: overwrite with your own"
mt["E5"].font = EX
mt.conditional_formatting.add(f"D5:D{MET_LAST}", CellIsRule(operator="equal", formula=['"Overdue"'], font=Font(name=F, color="B00020", bold=True)))

# ---- 5. Baseline -----------------------------------------------------------------------
bl = sheet("4 Baseline", [12, 11, 14, 14, 11, 14, 14, 12, 14, 14, 12, 13, 13, 13, 13, 13])
title(bl, "Baseline months", "Up to twelve months of plant figures. Yellow columns are yours; the grey columns are worked out. One example month is filled in.")
cols = ["Month", "Brews", "Grist charged (kg)", "Knockout wort (hL)", "Knockout gravity (°P)", "Beer to bright tank (hL)", "Beer packaged (hL)",
        "Dumped (hL)", "Power (kWh)", "Steam or fuel (MJ)", "Water (hL)",
        "Brewhouse yield", "Wort to pack loss", "kWh per hL", "MJ per hL", "Water to beer (hL/hL)"]
header(bl, 4, cols)
ext = PROF["Average extract of the grist, as-is (%)"]
for i in range(12):
    rr = 5 + i
    for col in range(1, 12):
        inp(bl.cell(rr, col)).number_format = "mmm yyyy" if col == 1 else ("0.0" if col == 5 else "#,##0")
    # SG from Plato (ASBC approximation), extract kg = litres x SG x P / 100
    body(bl.cell(rr, 12), f'=IF(OR(C{rr}="",D{rr}="",E{rr}=""),"",IFERROR((D{rr}*100*(1+E{rr}/(258.6-E{rr}/258.2*227.1))*E{rr}/100)/(C{rr}*{ext}),""))', "0.0%")
    body(bl.cell(rr, 13), f'=IF(OR(D{rr}="",G{rr}=""),"",1-G{rr}/D{rr})', "0.0%")
    body(bl.cell(rr, 14), f'=IF(OR(I{rr}="",G{rr}="",G{rr}=0),"",I{rr}/G{rr})', "0.0")
    body(bl.cell(rr, 15), f'=IF(OR(J{rr}="",G{rr}="",G{rr}=0),"",J{rr}/G{rr})', "0")
    body(bl.cell(rr, 16), f'=IF(OR(K{rr}="",G{rr}="",G{rr}=0),"",K{rr}/G{rr})', "0.00")
    for col in range(12, 17):
        bl.cell(rr, col).fill = FILL_BAND
ex_month = [46143, 78, 191000, 10900, 12.0, 10400, 10000, 20, 95000, 1200000, 42000]  # consistent with the example profile: 120,000 hL a year
for col, v in enumerate(ex_month, 1):
    bl.cell(5, col).value = v
bl.cell(17, 1, "Average").font = H2
for col in range(2, 17):
    L = get_column_letter(col)
    fmt = bl.cell(5, col).number_format
    body(bl.cell(17, col), f'=IFERROR(AVERAGE({L}5:{L}16),"")', fmt).font = Font(name=F, size=10, bold=True)
bl.cell(19, 1, "Brewhouse yield = extract in knockout wort (kg) / extract charged (kg). Extract in wort = litres x SG x °P / 100, with SG from °P by the ASBC "
               "approximation SG = 1 + P / (258.6 - (P / 258.2) x 227.1). Charged extract = grist kg x average extract as-is from the Profile sheet. "
               "Wort to pack loss compares packaged beer with knockout wort volume; it includes trub, yeast, filtration and packaging losses.").font = MUTED
bl.merge_cells("A19:P21")
bl["A19"].alignment = WRAP
bl.freeze_panes = "B5"

# ---- 6. Savings ------------------------------------------------------------------------
sv = sheet("5 Savings", [38, 18, 62])
title(sv, "What it could be worth", "The five formulas Beer365 uses, fed by your figures. Change any yellow assumption to your own view.")
header(sv, 4, ["Assumption", "Value", "Basis"])
ASSUME = [("Points of beer loss recovered", 0.01, "0.0%", "Breweries without a stage view commonly lose several percent between brewhouse and pack; we assume one point."),
          ("Points of brewhouse efficiency gained", 0.01, "0.0%", "Comparing every brew with the malt's lab value typically moves efficiency by a point or more."),
          ("Share of energy saved", 0.05, "0%", "Tracking power and steam by area against your best day typically trims a few percent."),
          ("Share of volume no longer dumped", 0.002, "0.0%", "Catching fermentation drift early saves the occasional batch."),
          ("Share of manual reporting time automated", 0.75, "0%", "Daily, weekly and month-end packs built from the record instead of by hand.")]
A = {}
for i, (k, v, fmt, why) in enumerate(ASSUME):
    rr = 5 + i
    body(sv.cell(rr, 1), k)
    inp(sv.cell(rr, 2), v).number_format = fmt
    body(sv.cell(rr, 3), why)
    A[k] = f"$B${rr}"
hl = PROF["Beer packaged a year (hL)"]
bc = PROF["Brewing cost per hL (malt, hops, energy, water)"]
en = PROF["Energy cost per hL (power plus steam)"]
grist_cost = f"({PROF['Malt and adjunct charged a year (kg)']}*{PROF['Malt and adjunct cost per kg']})"
bhe = f"IF({PROF['Brewhouse efficiency today (%)']}=\"\",IFERROR('4 Baseline'!L17,0.9),{PROF['Brewhouse efficiency today (%)']})"
rep = f"({PROF['Hours a week spent compiling reports by hand']}*52*{PROF['Cost of an hour of that time']})"
header(sv, 11, ["Saving", "A year", "Formula"])
SAV = [("Beer loss", f"={hl}*{A['Points of beer loss recovered']}*{bc}", "hL a year x points of loss recovered x brewing cost per hL"),
       ("Extract", f"={grist_cost}*{A['Points of brewhouse efficiency gained']}/{bhe}", "malt spend a year x points gained / efficiency today"),
       ("Energy", f"={hl}*{en}*{A['Share of energy saved']}", "hL a year x energy cost per hL x share saved"),
       ("Dumped batches", f"={hl}*{A['Share of volume no longer dumped']}*{bc}", "hL a year x share no longer dumped x brewing cost per hL"),
       ("Reporting", f"={rep}*{A['Share of manual reporting time automated']}", "hours a week x 52 x cost per hour x share automated")]
for i, (k, f_, why) in enumerate(SAV):
    rr = 12 + i
    body(sv.cell(rr, 1), k)
    body(sv.cell(rr, 2), f"=IFERROR({f_[1:]},0)", "#,##0")
    body(sv.cell(rr, 3), why)
body(sv.cell(17, 1), "Total a year").font = Font(name=F, size=11, bold=True)
c = body(sv.cell(17, 2), "=SUM(B12:B16)", "#,##0")
c.font, c.fill = Font(name=F, size=11, bold=True), FILL_IN
body(sv.cell(18, 1), "Year one (half, while the system goes live)")
body(sv.cell(18, 2), "=B17/2", "#,##0")
body(sv.cell(19, 1), "Three years")
body(sv.cell(19, 2), "=B17*2.5", "#,##0")
sv["A21"] = ("A planning figure from your own inputs, not a promise. We do not count lost sales in sold-out months, faster complaint answers, smaller recalls, "
             "water, or packaging on beer no longer lost. In the assessment the real starting point is measured from your records and signed by your plant controller; "
             "only savings counted against that baseline are ever claimed.")
sv["A21"].font, sv["A21"].alignment = MUTED, WRAP
sv.merge_cells("A21:C24")
sv["B12"].comment = Comment("Currency: as set on the Profile sheet.", "Ankur Napa")

# ---- 7. Questions -----------------------------------------------------------------------
qs = sheet("6 Questions", [8, 30, 56, 34, 13, 14, 14, 10])
title(qs, "The 221 questions", "Score each: how much it matters to you (0 to 3) and whether you have the data today (0 to 3). Priority = matters x data.")
header(qs, 4, ["ID", "Area", "Question", "Use case", "Build wave", "Matters 0 to 3", "Data 0 to 3", "Priority"])
dv_03 = DataValidation(type="whole", operator="between", formula1="0", formula2="3", allow_blank=True)
qs.add_data_validation(dv_03)
area_of = {}
for k, n, _, letters in AREAS:
    for u in UC:
        if u["section"] and u["section"][0] in letters:
            area_of[u["id"]] = n
for i, u in enumerate(sorted(UC, key=lambda u: u["id"])):
    rr = 5 + i
    body(qs.cell(rr, 1), u["id"])
    body(qs.cell(rr, 2), area_of[u["id"]])
    body(qs.cell(rr, 3), u["q"])
    body(qs.cell(rr, 4), u["title"])
    body(qs.cell(rr, 5), WAVE[u["when"]])
    dv_03.add(inp(qs.cell(rr, 6)))
    dv_03.add(inp(qs.cell(rr, 7)))
    body(qs.cell(rr, 8), f'=IF(OR(F{rr}="",G{rr}=""),"",F{rr}*G{rr})')
Q_LAST = 4 + len(UC)
qs["F5"], qs["G5"] = 3, 2
qs.auto_filter.ref = f"A4:H{Q_LAST}"
qs.freeze_panes = "C5"
qs.conditional_formatting.add(f"H5:H{Q_LAST}", CellIsRule(operator="greaterThanOrEqual", formula=["6"], fill=FILL_IN, font=Font(name=F, bold=True)))

# ---- 8. Readiness -----------------------------------------------------------------------
rd = sheet("7 Readiness", [44, 16, 60])
title(rd, "Readiness summary", "Worked out from the other sheets. Nothing to fill in here.")
header(rd, 4, ["Measure", "Result", "What it means"])
R = [("Records listed", f"=COUNTA('2 Records'!B5:B{REC_LAST})", "0", ""),
     ("Records you have answered", f"=COUNTA('2 Records'!C5:C{REC_LAST})", "0", ""),
     ("Records kept somewhere", f"=COUNTA('2 Records'!C5:C{REC_LAST})-COUNTIF('2 Records'!C5:C{REC_LAST},\"Not kept\")", "0", ""),
     ("Records on paper", f"=COUNTIF('2 Records'!C5:C{REC_LAST},\"Paper\")", "0", "Paper records are fine; they are keyed in during the first two weeks."),
     ("Records score", f"=IFERROR(AVERAGE('2 Records'!G5:G{REC_LAST}),0)", "0%", "Average ready score of the records you answered."),
     ("Meters fitted", f"=COUNTIF('3 Meters'!B5:B{MET_LAST},\"Yes\")", "0", ""),
     ("Meters calibrated in the last 12 months", f"=COUNTIF('3 Meters'!D5:D{MET_LAST},\"Yes\")", "0", ""),
     ("Meters score", f"=IFERROR(B11/B10,0)", "0%", "Share of fitted meters that are in calibration."),
     ("Baseline months entered", "=COUNT('4 Baseline'!G5:G16)", "0", "Three months is enough to start; twelve shows seasonality."),
     ("Baseline score", "=MIN(1,B13/3)", "0%", ""),
     ("Questions scored", f"=COUNT('6 Questions'!H5:H{Q_LAST})", "0", ""),
     ("Questions with priority 6 or more", f"=COUNTIF('6 Questions'!H5:H{Q_LAST},\">=6\")", "0", "These are where the first modules should start."),
     ("Planning saving a year", "='5 Savings'!B17", "#,##0", "In the currency on the Profile sheet."),
     ("Overall readiness", "=ROUND(0.5*B9+0.2*B12+0.3*B14,2)", "0%", "Half records, a fifth meters, the rest baseline.")]
for i, (k, f_, fmt, why) in enumerate(R):
    rr = 5 + i
    body(rd.cell(rr, 1), k)
    body(rd.cell(rr, 2), f_, fmt)
    body(rd.cell(rr, 3), why)
rr = 5 + len(R)
body(rd.cell(rr, 1), "Verdict").font = Font(name=F, size=11, bold=True)
v = body(rd.cell(rr, 2), f'=IF(B18>=0.7,"Ready to start",IF(B18>=0.4,"Ready with a two-week data tidy-up","Start with the records"))')
v.font, v.fill = Font(name=F, size=11, bold=True), FILL_IN
rd.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=3)

for s in wb.worksheets:
    s.sheet_properties.tabColor = YEL if s.title in ("1 Profile", "2 Records", "3 Meters", "4 Baseline", "6 Questions") else INK
wb.properties.creator = "Ankur Napa"
wb.properties.lastModifiedBy = "Ankur Napa"
wb.properties.title = "Beer365 Readiness Workbook"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print(OUT)
