# Disruptive Advantage

Marketing site for Disruptive Advantage, a data and applied AI team building
process intelligence for beer, whisky and wine producers.

Live at <https://ankurnapa.github.io/disruptive-advantage/>

## What this is

Ten static pages, one stylesheet, one script. No framework and no build step is
needed to serve it: everything in this repository is what gets deployed.

| Page | File |
|---|---|
| Home | `index.html` |
| About | `about.html` |
| Features | `features.html` |
| Solutions, beer whisky wine | `solutions.html` |
| Case studies | `case-studies.html` |
| Case study detail | `case-study-spirit-account.html` |
| Contact | `contact.html` |
| Careers | `careers.html` |
| Articles | `articles.html` |
| Article | `article-brewhouse-efficiency.html` |

## Design system

Palette, typography and spacing are ported from the approved Disruptive
Advantage profile deck rather than reinvented.

| Token | Value | Use |
|---|---|---|
| `--blue` | `#386FB9` | The single brand accent |
| `--navy` | `#1D4354` | Hero, section breaks, footer |
| `--ink` | `#1E1E1E` | Body and headings |
| `--beer` | `#916700` | Brewery category mark |
| `--whisky` | `#AA531E` | Distillery category mark |
| `--wine` | `#AE4A52` | Winery category mark |

The three industry marks are the brand blue converted to OKLCH, holding its
lightness (0.541) and chroma (0.130) exactly and rotating hue only, so no
category reads as louder than another.

Typeface is Neue June, self hosted, subset to Latin and served as woff2.

## CSS structure

`assets/site.css` is generated and uses three cascade layers:

```
@layer base, page, responsive;
```

Page rules are scoped per page (`.p-index`, `.p-contact`) so ten pages cannot
collide. That scoping out-specifies the shared media queries, so the responsive
rules live in a later layer and win by layer order rather than by specificity.
Edit the sources, not `site.css`.

## Editing

Content lives in the page sources used by the generator. To change a page,
edit its source and rebuild, rather than hand editing the generated HTML.

## Notes

- Case studies are anonymised representative engagements. No client is named
  and no outcome percentage is invented. `[REGION]` and `[DATE]` on the detail
  page are deliberate placeholders.
- The contact and newsletter forms compose a `mailto:` message, so the site
  needs no backend. Swap in a form endpoint when one exists.
- Every link resolves. There are no `href="#"` placeholders.
