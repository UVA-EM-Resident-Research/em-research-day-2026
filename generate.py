#!/usr/bin/env python3
"""Generate research overview pages from data.json manifest.

Each page:
  - Title, authors, method badge, tags
  - Presentation Details card (time, format, date)
  - Presentation Materials: inline-embedded slides and/or poster PDFs (if available)
  - Mentors & Collaborators

Run from repo root: `python3 generate.py`
"""
import json, os, html as html_mod

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SITE_DIR, "abstracts", "data.json")
OUT_DIR = os.path.join(SITE_DIR, "abstracts")

with open(DATA_PATH) as f:
    data = json.load(f)

METHOD_META = data["methodologyTypes"]

def esc(s):
    return html_mod.escape(str(s)) if s else ""

def format_label(fmt):
    labels = {
        "podium": "Podium Presentation",
        "poster-lightning": "Poster + Lightning Talk",
        "saem-dryrun": "SAEM Dress Rehearsal",
        "saem-gallery": "SAEM Gallery Wall",
    }
    return labels.get(fmt, fmt)

def format_icon(fmt):
    icons = {
        "podium": "🎤",
        "poster-lightning": "📋",
        "saem-dryrun": "🎯",
        "saem-gallery": "🖼️",
    }
    return icons.get(fmt, "📄")


def materials_section(entry):
    """Render embedded slides / poster PDF viewers when available."""
    slides = entry.get("slidesUrl")
    poster = entry.get("posterUrl")
    if not slides and not poster:
        return ""

    status = entry.get("materialStatus", "draft")
    # Label suffix: "(draft)" for AI prototypes, nothing for presenter-provided
    label_suffix = " (draft)" if status == "draft" else ""

    # Also offer editable PPTX download when the source file exists alongside the PDF
    def pptx_links(rel_pdf):
        pptx_rel = rel_pdf[:-4] + ".pptx"  # same slug, .pptx extension
        pptx_path = os.path.join(SITE_DIR, pptx_rel.replace("../", "", 1))
        if os.path.exists(pptx_path):
            return f'<span class="sep">·</span><a href="{esc(pptx_rel)}" download>Download PPTX</a>'
        return ""

    blocks = []
    if slides:
        slides_rel = "../" + slides
        blocks.append(f'''
      <div class="material-block">
        <div class="material-label">🎤 Slides{label_suffix}</div>
        <div class="material-frame">
          <embed src="{esc(slides_rel)}#toolbar=0&navpanes=0" type="application/pdf" width="100%" height="560" />
        </div>
        <div class="material-links">
          <a href="{esc(slides_rel)}" target="_blank" rel="noopener">Open in new tab</a>
          <span class="sep">·</span>
          <a href="{esc(slides_rel)}" download>Download PDF</a>{pptx_links(slides_rel)}
        </div>
      </div>''')
    if poster:
        poster_rel = "../" + poster
        blocks.append(f'''
      <div class="material-block">
        <div class="material-label">🖼️ Poster{label_suffix}</div>
        <div class="material-frame">
          <embed src="{esc(poster_rel)}#toolbar=0&navpanes=0" type="application/pdf" width="100%" height="560" />
        </div>
        <div class="material-links">
          <a href="{esc(poster_rel)}" target="_blank" rel="noopener">Open in new tab</a>
          <span class="sep">·</span>
          <a href="{esc(poster_rel)}" download>Download PDF</a>{pptx_links(poster_rel)}
        </div>
      </div>''')

    if status == "presenter":
        note = 'Presenter-provided materials. PDFs open in your browser; use the links to open in a new tab or download.'
    else:
        note = 'Working drafts — presenters may refine before April 29. PDFs open in your browser; use the links to open in a new tab or download.'

    return f'''
    <div class="section">
      <div class="section-title">Presentation Materials</div>
      <div class="materials-note">{note}</div>
      {"".join(blocks)}
    </div>'''


def build_abstract_page(entry, entry_type="pgy3"):
    """Generate HTML for one research overview page."""
    if entry_type == "pgy3":
        name = entry["name"]
        title = entry["project"]
        slug = entry["slug"]
        mentors = entry.get("mentors", [])
        methodology = entry.get("methodology", "")
        fmt = entry.get("format", "podium")
        block_time = entry.get("blockTime", "")
        saem = entry.get("saemAccepted", False)
        category = ""
        authors_str = ""
    elif entry_type == "saem":
        name = entry["piClean"]
        title = entry["title"]
        slug = entry["slug"]
        mentors = []
        methodology = "retrospective-database"
        fmt = "saem-gallery"
        block_time = "On display all morning"
        saem = True
        category = entry.get("category", "")
        authors_str = entry.get("authors", "") or ""
        pi_full = entry.get("pi", "")
        if "(" in pi_full:
            mentor_part = pi_full.split("(")[1].rstrip(")")
            mentors = [m.strip() for m in mentor_part.split(",")]
    elif entry_type == "dryrun":
        name = entry["name"]
        title = entry["project"]
        slug = entry["slug"]
        mentors = entry.get("mentors", [])
        methodology = "prospective-observational"
        fmt = entry.get("format", "saem-dryrun")
        block_time = entry.get("blockTime", "")
        saem = True
        category = ""
        authors_str = ""

    method = METHOD_META.get(methodology, {"label": methodology, "color": "#6b7280", "bg": "#f3f4f6"})

    # Build tags
    tags_html = ""
    if saem:
        tags_html += '<span class="tag tag-saem">SAEM 2026</span>'
    if entry_type == "pgy3":
        tags_html += '<span class="tag tag-pgy3">PGY-3</span>'
    elif entry_type == "saem":
        pi_full = entry.get("pi", "")
        role = entry.get("role", "")
        if role == "scribe":
            tags_html += '<span class="tag tag-scribe">Medical Scribe</span>'
        elif role == "student" or "student" in pi_full.lower() or "(M" in pi_full:
            tags_html += '<span class="tag tag-student">Med Student</span>'
        elif role == "resident" or "(R" in pi_full or "Dr." in pi_full:
            tags_html += '<span class="tag tag-pgy3">Resident</span>'
        else:
            tags_html += '<span class="tag tag-faculty">Faculty</span>'
    if category:
        tags_html += f'<span class="tag tag-category">{esc(category)}</span>'

    # Mentors HTML (skip TBD placeholders)
    clean_mentors = [m for m in mentors if m and m != "TBD"]
    mentors_html = ""
    if clean_mentors:
        chips = "".join(f'<span class="mentor-chip">Dr. {esc(m)}</span>' for m in clean_mentors)
        mentors_html = f'''
    <div class="section">
      <div class="section-title">Mentors &amp; Collaborators</div>
      <div class="mentor-list">{chips}</div>
    </div>'''

    # Authors line
    role_display = entry.get("roleDisplay", "")
    if authors_str:
        authors_line = f'<div class="authors">with {esc(authors_str)}</div>'
    elif clean_mentors:
        mentor_str = ", ".join(esc(m) for m in clean_mentors)
        if role_display:
            authors_line = f'<div class="authors"><strong>{esc(name)}</strong>, {esc(role_display)} · Faculty: {mentor_str}</div>'
        else:
            authors_line = f'<div class="authors"><strong>{esc(name)}</strong> · Faculty: {mentor_str}</div>'
    else:
        if role_display:
            authors_line = f'<div class="authors"><strong>{esc(name)}</strong> · {esc(role_display)}</div>'
        else:
            authors_line = f'<div class="authors"><strong>{esc(name)}</strong></div>'

    # Presentation materials
    materials_html = materials_section(entry)

    # Abstract placeholder — light framing, no heavy boilerplate
    if materials_html:
        abstract_copy = "The full abstract will appear here once the presenter finalizes their summary. The slides and poster above reflect the current draft."
    else:
        abstract_copy = "The full abstract will appear here once the presenter finalizes their summary — check back as April 29 approaches."
    abstract_placeholder = f'''
    <div class="section">
      <div class="section-title">Abstract</div>
      <div class="section-content placeholder">{esc(abstract_copy)}</div>
    </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(name)} — {esc(title)} | EM Research Day 2026</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<div class="abstract-page">

  <nav class="back-nav">
    <a href="../index.html">← Event Home</a>
    <span class="sep">|</span>
    <a href="../schedule.html">Schedule</a>
    <span class="sep">|</span>
    <a href="../gallery.html">All Research</a>
  </nav>

  <div class="abstract-header">
    <div class="method-badge" style="background:{method['bg']}; color:{method['color']};">{method['label']}</div>
    <h1>{esc(title)}</h1>
    {authors_line}
    <div class="tag-row">{tags_html}</div>
  </div>

  <div class="abstract-body">

    <div class="section">
      <div class="section-title">Presentation Details</div>
      <div class="schedule-card">
        <div>
          <div class="time">{format_icon(fmt)} {esc(block_time)}</div>
          <div class="format-label">{format_label(fmt)}</div>
        </div>
        <div class="divider"></div>
        <div>
          <div style="font-size:13px; color:var(--gray-700);">Wednesday, April 29, 2026</div>
          <div style="font-size:12px; color:var(--gray-400);">UVA Department of Emergency Medicine</div>
        </div>
      </div>
    </div>
{materials_html}
{abstract_placeholder}
{mentors_html}
  </div>

  <footer class="abstract-footer">
    UVA EM Research Day 2026 · <a href="../index.html">Event Home</a> · <a href="../schedule.html">Schedule</a> · <a href="../gallery.html">Browse All Research</a>
  </footer>

</div>
</body>
</html>'''


# ── Generate all pages ──
generated = []

# PGY-3 presenters
for p in data["pgy3Presenters"]:
    html_content = build_abstract_page(p, "pgy3")
    path = os.path.join(OUT_DIR, f"{p['slug']}.html")
    with open(path, "w") as f:
        f.write(html_content)
    generated.append({
        "slug": p["slug"], "name": p["name"], "title": p["project"],
        "type": "pgy3", "format": p["format"], "methodology": p.get("methodology",""),
        "hasSlides": "slidesUrl" in p, "hasPoster": "posterUrl" in p,
    })
    print(f"  ✓ PGY-3: {p['slug']}.html")

# SAEM gallery
for s in data["saemGallery"]:
    if s.get("alsoOnPgy3Schedule"):
        print(f"  ○ SAEM skip (already PGY-3): {s['piClean']}")
        continue
    html_content = build_abstract_page(s, "saem")
    path = os.path.join(OUT_DIR, f"{s['slug']}.html")
    with open(path, "w") as f:
        f.write(html_content)
    generated.append({
        "slug": s["slug"], "name": s["piClean"], "title": s["title"],
        "type": "saem", "format": "saem-gallery", "methodology": "retrospective-database",
        "hasSlides": "slidesUrl" in s, "hasPoster": "posterUrl" in s,
    })
    print(f"  ✓ SAEM: {s['slug']}.html")

# Dry-run presenters
for d in data["dryRunPresenters"]:
    html_content = build_abstract_page(d, "dryrun")
    path = os.path.join(OUT_DIR, f"{d['slug']}.html")
    with open(path, "w") as f:
        f.write(html_content)
    generated.append({
        "slug": d["slug"], "name": d["name"], "title": d["project"],
        "type": "dryrun", "format": "saem-dryrun", "methodology": "prospective-observational",
        "hasSlides": "slidesUrl" in d, "hasPoster": "posterUrl" in d,
    })
    print(f"  ✓ Dry-run: {d['slug']}.html")

# Write generated index for use by gallery page
with open(os.path.join(OUT_DIR, "index.json"), "w") as f:
    json.dump(generated, f, indent=2)

print(f"\n✅ Generated {len(generated)} research overview pages")
