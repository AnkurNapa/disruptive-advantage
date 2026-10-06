"""The 221 use cases from the vault catalogue (Brewery-Use-Cases), grouped into the
areas of a beer business a brewer would recognise. Shared by build_beer.py and
build_usecases.py so the counts on both pages always agree."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UC = json.load(open(os.path.join(HERE, "use_cases.json")))

AREAS = [
    ("raw", "Raw materials and recipe", "Malt, hops, water and the recipe, from the supplier's certificate to the pilot brew.", "ABR"),
    ("brewhouse", "Brewhouse", "Milling to wort cooling, and every point of extract along the way.", "C"),
    ("cellar", "Fermentation and cellar", "Yeast, fermentation, maturation, filtration and the beer's physical stability.", "DES"),
    ("packaging", "Packaging", "Bottle, can and keg lines, from fill level to dissolved oxygen.", "FW"),
    ("quality", "Quality, safety and traceability", "Laboratory, sensory, food safety, complaints and recall.", "IJV"),
    ("plant", "Energy, utilities and plant", "Power, steam, refrigeration, CO2, water, effluent and the kit itself.", "GHTU"),
    ("market", "Supply chain, sales and marketing", "Warehouse, freshness, distributors, outlets, demand and brand.", "KLM"),
    ("business", "Finance, duty, ESG and people", "True cost per hectolitre, excise, carbon, compliance and the shift.", "NOP"),
    ("layer", "Across the whole brewery", "The questions that cut across every department at once.", "Q"),
]
WAVE = {"NOW": "First wave", "NEXT": "Second wave", "LATER": "Later"}


def cases(area):
    letters = area[3]
    return [u for u in UC if u["section"] and u["section"][0] in letters]


def examples(area, n=3):
    """Lead with first-wave, strong-evidence questions."""
    rank = {"NOW": 0, "NEXT": 1, "LATER": 2}
    pool = sorted(cases(area), key=lambda u: (rank[u["when"]], u["conf"] != "strong", u["id"]))
    return pool[:n]


assert sum(len(cases(a)) for a in AREAS) == len(UC), "an area mapping dropped a section"
