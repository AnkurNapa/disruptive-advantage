# Brief: Beer365 articles

You are writing practitioner articles for the Beer365 website (beer intelligence for
the whole beer business, built by Disruptive Advantage). Each article answers ONE
question from the brewery use case catalogue. Byline: Ankur Napa, a former R&D brewer
at United Breweries, SABMiller and AB InBev, now a data engineer. Readers: head brewers,
packaging leads, quality heads, plant and finance directors at mid to large breweries.

## Inputs for each use case in your batch file
- The catalogue note: ~/Documents/obsidian/Brewery-Use-Cases/UC-<3-digit id> <title>.md
  It holds the question, the data needed and "Evidence in this vault" links. READ the
  cited vault notes for the real formulas and brewing facts.
- Authoritative brewing maths: ~/Documents/obsidian/MasterBrewers_Export/ (MBAA - CALCULATIONS_REFERENCE.md etc).
  Compute in base units. Numbers must be brewing-correct, not approximate.

## Voice and rules (non-negotiable)
1. Read ~/.claude/skills/humanizer/SKILL.md and ~/.claude/skills/humanizer/references/ankur-voice.md first, and write in that voice. Apply the humanizer silently.
2. Punctuation: NO em dash, NO en dash, NO curly quotes, no double spaces. Use straight quotes. No serial comma before "and"; avoid ", and" joins. British spelling (colour, optimise, litre, analyse, programme).
3. No AI vocabulary (delve, landscape, seamless, leverage, unlock, crucial, robust, game-changer). No "In conclusion". No rule-of-three padding.
4. Never invent statistics, studies, surveys, customers, quotes or named breweries. No client names or sites at all (never Alwar, Carlsberg, Diageo, Pernod, AB InBev as a customer). Worked examples use a clearly hypothetical brewery and say "for example" or "say"; the numbers in them must compute correctly.
5. Do not promise results or percentages. Beer365 may be mentioned once, near the end, plainly: what it does for this question (one record, reads from your systems, answers cite the batch). No hard sell.
6. Each article: 650 to 950 words of body. Practical: why the question matters in money or quality, what to measure and where, the formula if there is one, a short worked example, the traps that make the number lie, what good looks like.

## Output: one JSON file per article
Write to ~/Documents/da-website/_build/articles/<slug>.json (slug: lowercase, hyphens, short, unique, e.g. "coa-versus-reality"). Schema:
{
 "slug": "coa-versus-reality",
 "uc_id": 2,
 "area": "<area key from the batch file>",
 "title": "Headline, sentence case, specific, max 80 chars (may differ from the catalogue title; no colon-reveal tricks)",
 "standfirst": "One or two sentences, max 40 words",
 "read_min": <int, words/220 rounded up>,
 "sections": [
   {"h2": "Section heading, sentence case", "blocks": [
      {"p": "Paragraph text. Use **double asterisks** for bold sparingly."},
      {"ul": ["item", "item"]},
      {"eq": {"label": "What it computes", "code": "formula in plain text, e.g. BHE % = extract in KO wort (kg) / extract charged (kg) x 100", "note": "optional one line"}},
      {"table": {"head": ["Col", "Col"], "rows": [["a", "b"]]}}
   ]}
 ]
}
3 to 5 sections. Valid JSON only (escape inner double quotes). After writing all ten, re-read each file and check: JSON parses (python3 -c "import json,sys;json.load(open(sys.argv[1]))" FILE), no characters U+2013 U+2014 U+2018 U+2019 U+201C U+201D anywhere, arithmetic in examples is right.

Reply at the end with a list of slug, title and word count, and anything you were unsure of.
