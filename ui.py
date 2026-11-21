import html

CSS = """
<style>
#MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 1.2rem; max-width: 1100px;}

.hero {background:#0B2447; border-radius:16px; padding:34px 44px 30px; margin-bottom:24px;}
.brand {font-size:1.45rem; font-weight:800; letter-spacing:-0.5px; color:#fff; margin-bottom:28px;}
.brand span {color:#2DD4BF;}
.hero-title {font-size:2.7rem; line-height:1.12; font-weight:800; color:#fff; margin:0 0 14px;}
.hero-sub {color:#CFE0F1; font-size:1.05rem; max-width:650px; margin:0 0 20px;}
.hero-pts {color:#9FB6CE; font-size:0.92rem;}
.hero-pts span {margin-right:24px;}

.section-title {font-size:1.05rem; font-weight:700; color:#0B2447; margin:6px 0 4px;}

.card {background:#fff; color:#0B2447; border:1px solid #E3EAF2; border-radius:14px;
       padding:22px 24px; box-shadow:0 2px 10px rgba(11,36,71,0.06); margin-bottom:16px;}
.card-title {font-weight:700; font-size:1.05rem; margin-bottom:12px; color:#0B2447;}

.ring {width:156px; height:156px; border-radius:50%; display:flex; align-items:center;
       justify-content:center; margin:6px auto 0;}
.ring-inner {width:120px; height:120px; border-radius:50%; background:#fff; display:flex;
             flex-direction:column; align-items:center; justify-content:center;}
.ring-num {font-size:2.5rem; font-weight:800; line-height:1; color:#0B2447;}
.ring-label {font-size:0.8rem; font-weight:800; letter-spacing:0.06em; margin-top:4px;}
.pill {display:block; width:fit-content; margin:16px auto 0; background:#E6F5F3; color:#0E8A8F;
       font-weight:700; font-size:0.72rem; letter-spacing:0.08em; padding:6px 14px; border-radius:8px;}

.row {display:flex; align-items:center; gap:10px; padding:9px 12px; border-radius:8px;
      font-size:0.95rem; margin-bottom:4px; color:#0B2447;}
.row.bad {background:#FDECEC;}
.ic {width:20px; height:20px; border-radius:50%; display:inline-flex; align-items:center;
     justify-content:center; color:#fff; font-size:0.72rem; font-weight:800; flex:none;}
.row.ok .ic {background:#12A150;}
.row.bad .ic {background:#D92D20;}
.badge {margin-left:auto; background:#D92D20; color:#fff; border-radius:50%; width:20px;
        height:20px; display:inline-flex; align-items:center; justify-content:center;
        font-size:0.72rem; font-weight:700;}

.tiles {display:flex; gap:12px; margin-bottom:16px;}
.tile {flex:1; background:#F2F6FA; border-radius:12px; padding:14px 16px; color:#0B2447;}
.tile b {display:block; font-size:1.6rem; line-height:1.2;}
.tile small {color:#5B6F86; font-weight:600;}

.chip {display:inline-block; padding:5px 12px; border-radius:999px; font-size:0.85rem;
       font-weight:600; margin:0 6px 8px 0;}
.chip.g {background:#E3F6EA; color:#0B7A3E;}
.chip.r {background:#FDECEC; color:#B42318;}
.empty {color:#5B6F86; font-size:0.92rem;}

div.stButton > button, button[data-testid="stBaseButton-primary"] {
  background:#0E8A8F; color:#fff; border:none; border-radius:999px;
  padding:0.65rem 2.4rem; font-weight:700; font-size:1.05rem;}
div.stButton > button:hover, button[data-testid="stBaseButton-primary"]:hover {
  background:#0B7479; color:#fff; border:none;}
section[data-testid="stFileUploaderDropzone"] {
  border:2px dashed #0E8A8F; background:#F2F6FA; border-radius:12px;}
</style>
"""


def hero() -> str:
    return (
        '<div class="hero">'
        '<div class="brand">Resum<span>orix</span></div>'
        '<div class="hero-title">Free ATS Resume Checker<br>&amp; Job Matcher</div>'
        '<div class="hero-sub">Upload your resume, paste a job description, and get an instant '
        'match score, skill gaps, and an ATS readiness checklist.</div>'
        '<div class="hero-pts"><span>✓ Never stores your resume</span>'
        '<span>✓ 8 ATS checks</span><span>✓ Skill gap analysis</span></div>'
        '</div>'
    )


def _grade(total: float):
    if total >= 80:
        return "EXCELLENT", "#12A150"
    if total >= 60:
        return "GOOD", "#0E8A8F"
    if total >= 40:
        return "FAIR", "#F59E0B"
    return "NEEDS WORK", "#D92D20"


def score_card(total: float) -> str:
    label, color = _grade(total)
    pct = max(0, min(100, total))
    return (
        '<div class="card">'
        f'<div class="ring" style="background: conic-gradient({color} 0 {pct}%, #E6ECF2 0);">'
        '<div class="ring-inner">'
        f'<div class="ring-num">{total:.0f}</div>'
        f'<div class="ring-label" style="color:{color};">{label}</div>'
        '</div></div>'
        '<span class="pill">RESUME STRENGTH</span>'
        '</div>'
    )


def tiles(sem: float, skill: float, ats: float) -> str:
    def t(value, name):
        return f'<div class="tile"><b>{value * 100:.0f}%</b><small>{name}</small></div>'

    return (
        '<div class="tiles">'
        + t(sem, "Semantic match")
        + t(skill, "Skill overlap")
        + t(ats, "ATS readiness")
        + '</div>'
    )


def checklist_card(checks, missing) -> str:
    rows = []
    for label, ok in checks:
        cls, icon = ("ok", "✓") if ok else ("bad", "!")
        rows.append(
            f'<div class="row {cls}"><span class="ic">{icon}</span>'
            f'<span>{html.escape(label)}</span></div>'
        )
    if missing:
        rows.append(
            '<div class="row bad"><span class="ic">!</span><span>Job skills match</span>'
            f'<span class="badge">{len(missing)}</span></div>'
        )
    else:
        rows.append('<div class="row ok"><span class="ic">✓</span><span>Job skills match</span></div>')
    return '<div class="card"><div class="card-title">ATS checklist</div>' + "".join(rows) + '</div>'


def chips_card(title: str, skills, kind: str, empty_text: str) -> str:
    if skills:
        body = "".join(f'<span class="chip {kind}">{html.escape(s)}</span>' for s in skills)
    else:
        body = f'<div class="empty">{html.escape(empty_text)}</div>'
    return f'<div class="card"><div class="card-title">{html.escape(title)}</div>{body}</div>'