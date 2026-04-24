# CLAUDE.md — UVA EM Research Day 2026 Event Site

This file gives Claude persistent context for any session working in this repository.

## What this repo is

The public event site for **UVA Emergency Medicine Research Day 2026**, a department-wide morning of research on **Wednesday, April 29, 2026**, 8:30 AM – 12:30 PM, Pinn Hall. Hosted on GitHub Pages under the `UVA-EM-Resident-Research` organization.

This repo is narrowly scoped to the **live event site**. Planning materials (resident trackers, logistics checklists, email drafts, decision logs) live in the private working folder at `~/Documents/Work (iCloud)/Academic/UVA EM/2026.04 UVA EM Research Day/`.

## Structure

```
.
├── index.html              Event landing page (front door for faculty + residents)
├── schedule.html           Full program with planning/public view toggle
├── gallery.html            SAEM-accepted abstract browser with filters
├── abstracts/
│   ├── *.html              One page per project (33 total)
│   ├── data.json           Structured data backing the gallery
│   └── index.json          Lightweight index for the filter bar
├── assets/
│   └── style.css           Shared styles for gallery + abstract pages
├── generate.py             Regenerates abstracts/ pages from data.json
├── .github/workflows/
│   └── deploy-pages.yml    Auto-deploys the site on push to main
├── .nojekyll               Tells GitHub Pages to serve files as-is
└── README.md               Human onboarding + deploy notes
```

## Design system

Jefferson Blue `#232D4B` · Rotunda Orange `#E57200` · UVA Cream `#F4EAD5`. Source Serif 4 for display, Inter for body. Full spec in the parent planning folder at `05_Day_Of/Design_Brief.md`. Rules:

- Navy is the default field for 70%+ of a composition.
- Orange is accent-only. Never a whole-slide background.
- Cream-on-navy is the primary type treatment for dark compositions.
- No other palette colors. Photography muted/desaturated only.

## Working principles

- **Speed > polish.** The site went from idea to live in the same week as the event. Iterate, ship, revise.
- **Every graduating PGY-3 presents something.** Seven podium talks + five posters/lightning + dress rehearsals — every resident is visible.
- **Faculty mentorship is a named value.** The site should read as a celebration of mentor + resident pairs, not of individuals.
- **Forwardable standard** (from the `uva-em-voice` skill): any copy on the site should read fine if printed and slid across a table to the Department Chair.

## Voice & copy conventions

Follow the `uva-em-voice` skill in Matt's local Claude setup when editing site copy. Short version:

- Full names with credentials on first mention: "Andrew Taylor, MD" not "Andy T."
- Formal event names: "UVA Emergency Medicine Research Day 2026" on first mention, "Research Day 2026" or "Research Day" thereafter.
- No "gang," "folks," casual group-address, or exclamation-point pile-ups.
- Gentle warmth, not aggressive marketing. "A morning of research from our department" is the canonical tagline — it is deliberately understated.

## Editing the site

### Schedule or presenter changes

Most content updates happen in `index.html` (landing) and `schedule.html` (full program). Both are self-contained HTML files with inline CSS — no build step.

### Adding or updating an abstract page

Pages in `abstracts/` are generated from `abstracts/data.json` by `generate.py`. To add or update an abstract:

1. Edit `abstracts/data.json`
2. Run `python3 generate.py`
3. Verify the new/updated page in `abstracts/`
4. Commit and push

### Deploying

Push to `main`. The GitHub Actions workflow in `.github/workflows/deploy-pages.yml` deploys automatically. Live URL: `https://uva-em-resident-research.github.io/em-research-day-2026/`.

## People

- **Matt Trowbridge, MD** — Lead organizer, MC, site maintainer (`trowbridge.business@gmail.com`)
- **Andrew Taylor, MD** — Vice-Chair for Research, sponsor
- **Andrew Muck, MD** — Department Chair
- **Heather Lounsbury** — Education co-lead, resident coordination
- **Bill Brady, MD** — Keynote (invited)
- **Tom Hartka, MD** — 2025 Research Day lead, advising this year

Full contact registry in the parent planning folder's `CLAUDE.md`.

## When editing this site, Claude should

- Preserve the design system exactly. Don't introduce new colors or fonts.
- Preserve the Rotunda / Monticello aesthetic — warm, academic, considered. Not startup-pitch-deck.
- Maintain navigation consistency: every page should have a way back to `index.html` (Home), `schedule.html` (Schedule), and `gallery.html` (Gallery).
- Update `README.md` if the file structure changes.
- Use `git commit -m "<concise verb-led message>"` for every change; small commits beat large ones.
- Flag anything that affects the live event (e.g., a schedule change within 7 days of April 29) back to Matt before committing.
