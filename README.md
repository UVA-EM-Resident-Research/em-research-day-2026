# UVA EM Research Day 2026 — Event Site

Static site for the [UVA Department of Emergency Medicine](https://med.virginia.edu/emergency-medicine/) Annual Research Day, held Wednesday, April 29, 2026.

**Live site:** https://uva-em-resident-research.github.io/em-research-day-2026/ *(after Pages is enabled — see below)*

---

## Quick start

This is a plain static HTML site. No build step, no dependencies, no framework. Open `index.html` in a browser to view locally.

```bash
git clone https://github.com/UVA-EM-Resident-Research/em-research-day-2026.git
cd em-research-day-2026
open index.html          # macOS — opens in default browser
```

## Pages

| Page | Purpose |
|---|---|
| `index.html` | **Landing page** — the front door. Event framing, format pillars, schedule preview, resident roster, mentorship note. |
| `schedule.html` | **Full program** with a planning/public view toggle. Planning view shows TBDs and working-drafts; public view shows finals only. |
| `gallery.html` | **SAEM abstract browser** — filter and browse all accepted abstracts from the department. |
| `abstracts/*.html` | One detail page per project. Generated from `abstracts/data.json` via `generate.py`. |

## Design system

Jefferson Blue (`#232D4B`) · Rotunda Orange (`#E57200`) · UVA Cream (`#F4EAD5`). Source Serif 4 for display, Inter for body. Full spec and copy bank in the parent planning folder's `05_Day_Of/Design_Brief.md`.

## Deployment

The site is deployed to GitHub Pages via the workflow in `.github/workflows/deploy-pages.yml`. Every push to `main` triggers a rebuild.

### First-time setup

1. **Enable GitHub Pages** for this repo:
   `Settings → Pages → Source: "GitHub Actions"` — select this instead of "Deploy from a branch."
2. **If the repo is private:** GitHub Pages on a private repo requires **GitHub Team** ($4/user/mo for orgs) or **GitHub Enterprise**. If the organization is on the free tier, either (a) make this repo public — it only contains a public event site, or (b) upgrade the org. Making public is the recommended path.
3. **Push to `main`** — the workflow runs automatically and the site appears at the URL above within ~60 seconds.

### Updating

```bash
git pull                           # start from latest main
# edit files
git add .
git commit -m "Describe the change"
git push                           # Pages rebuilds automatically
```

## Regenerating abstract pages

Abstract pages in `abstracts/` are generated from `abstracts/data.json` by `generate.py`.

```bash
python3 generate.py                # regenerates all abstracts/*.html from data.json
```

After regenerating, review the diff with `git diff abstracts/` and commit.

## Repository conventions

- **One concern per commit.** Easier to revert.
- **Concise commit messages** — verb-led, present tense. "Add resident to lightning round" not "added residents."
- **No secrets, no PII beyond publicly shareable names + project titles.** This is a public-facing site.
- **Issues** — file in the GitHub Issues tab for schedule changes, bug fixes, and design requests.

## Claude assistance

This repo is set up for use with Claude Code. See `CLAUDE.md` at the repo root for session context, voice conventions, and editing guidelines.

## Credits

**Host & MC:** Matt Trowbridge, MD ([`trowbridge.business@gmail.com`](mailto:trowbridge.business@gmail.com))
**Vice-Chair Research & sponsor:** Andrew Taylor, MD
**Education co-lead:** Heather Lounsbury
**Department Chair:** Andrew Muck, MD

Built with Claude AI assistance.

## License

See [LICENSE](LICENSE). Content owned by the University of Virginia School of Medicine.
