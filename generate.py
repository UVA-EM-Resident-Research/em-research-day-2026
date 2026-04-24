#!/usr/bin/env python3
"""Generate research overview pages from data.json manifest."""
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

# ── Method-specific section templates ──
def method_sections(methodology):
    templates = {
        "prospective-observational": [
            ("Research Question", None),
            ("Study Design & Methods", None),
            ("Key Findings", None),
            ("Clinical Significance", None),
        ],
        "clinical-innovation": [
            ("Problem Statement", None),
            ("Innovation Description", None),
            ("Implementation & Impact", None),
            ("Lessons Learned", None),
        ],
        "case-report": [
            ("Clinical Scenario", None),
            ("Key Findings", None),
            ("Teaching Points", None),
        ],
        "retrospective-database": [
            ("Research Question", None),
            ("Data Source & Methods", None),
            ("Key Findings", None),
            ("Implications", None),
        ],
        "educational-chapter": [
            ("Scope & Topic", None),
            ("Key Contributions", None),
            ("Publication Status", None),
        ],
    }
    return templates.get(methodology, [("Abstract", None)])


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
        notes = entry.get("notes", "")
        category = ""
        authors_str = ""
    elif entry_type == "saem":
        name = entry["piClean"]
        title = entry["title"]
        slug = entry["slug"]
        mentors = []
        methodology = "retrospective-database"  # default for SAEM
        fmt = "saem-gallery"
        block_time = "On display all morning"
        saem = True
        notes = ""
        category = entry.get("category", "")
        authors_str = entry.get("authors", "") or ""
        # Parse mentors from pi field
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
        notes = ""
        category = ""
        authors_str = ""

    method = METHOD_META.get(methodology, {"label": methodology, "color": "#6b7280", "bg": "#f3f4f6"})
    sections = method_sections(methodology)

    # Build tags
    tags_html = ""
    if saem:
        tags_html += '<span class="tag tag-saem">SAEM 2026</span>'
    if entry_type == "pgy3":
        tags_html += '<span class="tag tag-pgy3">PGY-3</span>'
    elif entry_type == "saem":
        pi_full = entry.get("pi", "")
        if "(R" in pi_full or "Dr." in pi_full:
            tags_html += '<span class="tag tag-pgy3">Resident</span>'
        elif "student" in pi_full.lower() or "(M" in pi_full:
            tags_html += '<span class="tag tag-student">Med Student</span>'
        else:
            tags_html += '<span class="tag tag-faculty">Faculty</span>'
    if category:
        tags_html += f'<span class="tag tag-category">{esc(category)}</span>'

    # Mentors HTML
    mentors_html = ""
    if mentors and mentors != ["TBD"]:
        chips = "".join(f'<span class="mentor-chip">Dr. {esc(m)}</span>' for m in mentors)
        mentors_html = f'''
    <div class="section">
      <div class="section-title">Mentors &amp; Collaborators</div>
      <div class="mentor-list">{chips}</div>
    </div>'''

    # Authors line
    if authors_str:
        authors_line = f'<div class="authors">with {esc(authors_str)}</div>'
    elif mentors and mentors != ["TBD"]:
        authors_line = f'<div class="authors"><strong>{esc(name)}</strong> · Faculty: {", ".join(esc(m) for m in mentors)}</div>'
    else:
        authors_line = f'<div class="authors"><strong>{esc(name)}</strong></div>'

    # Sections HTML
    sections_html = ""
    for sec_title, sec_content in sections:
        if sec_content:
            sections_html += f'''
    <div class="section">
      <div class="section-title">{esc(sec_title)}</div>
      <div class="section-content">{esc(sec_content)}</div>
    </div>'''
        else:
            sections_html += f'''
    <div class="section">
      <div class="section-title">{esc(sec_title)}</div>
      <div class="section-content placeholder">Details will be available soon — check back as presenters finalize their materials.</div>
    </div>'''

    # Notes (planning only)
    notes_html = ""
    if notes:
        notes_html = f'''
    <div class="section" style="background:#FFFBEB; padding:12px 16px; border-radius:6px; border-left:3px solid #F59E0B;">
      <div class="section-title" style="color:#92400E; border:none; padding:0; margin-bottom:4px;">Planning Note</div>
      <div class="section-content" style="font-size:13px; color:#78350F;">{esc(notes)}</div>
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
    <a href="../index.html">← Schedule</a>
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
{sections_html}
{mentors_html}
{notes_html}
  </div>

  <footer class="abstract-footer">
    UVA EM Research Day 2026 · <a href="../index.html">Back to Schedule</a> · <a href="../gallery.html">Browse All Research</a>
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
    generated.append({"slug": p["slug"], "name": p["name"], "title": p["project"], "type": "pgy3", "format": p["format"], "methodology": p.get("methodology","")})
    print(f"  ✓ PGY-3: {p['slug']}.html")

# SAEM gallery (skip those already generated as PGY-3)
pgy3_slugs = {p["slug"] for p in data["pgy3Presenters"]}
for s in data["saemGallery"]:
    if s["alsoOnPgy3Schedule"]:
        print(f"  ○ SAEM skip (already PGY-3): {s['piClean']}")
        continue
    html_content = build_abstract_page(s, "saem")
    path = os.path.join(OUT_DIR, f"{s['slug']}.html")
    with open(path, "w") as f:
        f.write(html_content)
    generated.append({"slug": s["slug"], "name": s["piClean"], "title": s["title"], "type": "saem", "format": "saem-gallery", "methodology": "retrospective-database"})
    print(f"  ✓ SAEM: {s['slug']}.html")

# Dry-run presenters
for d in data["dryRunPresenters"]:
    html_content = build_abstract_page(d, "dryrun")
    path = os.path.join(OUT_DIR, f"{d['slug']}.html")
    with open(path, "w") as f:
        f.write(html_content)
    generated.append({"slug": d["slug"], "name": d["name"], "title": d["project"], "type": "dryrun", "format": "saem-dryrun", "methodology": "prospective-observational"})
    print(f"  ✓ Dry-run: {d['slug']}.html")

# Write generated index for use by gallery page
with open(os.path.join(OUT_DIR, "index.json"), "w") as f:
    json.dump(generated, f, indent=2)

print(f"\n✅ Generated {len(generated)} research overview pages")
