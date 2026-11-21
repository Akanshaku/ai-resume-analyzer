import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import streamlit as st

import ui
from parser import extract_text
from scorer import ats_check, final_score, semantic_score, skill_score
from skills import extract_skills
from suggestions import get_suggestions

st.set_page_config(page_title="Resumorix | ATS Resume Checker")

# Load optional API key from Streamlit secrets
try:
    if "ANTHROPIC_API_KEY" in st.secrets:
        os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    pass

st.markdown(ui.CSS, unsafe_allow_html=True)
st.markdown(ui.hero(), unsafe_allow_html=True)

left, right = st.columns(2, gap="large")
with left:
    st.markdown('<div class="section-title">1. Upload your resume</div>', unsafe_allow_html=True)
    file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")
with right:
    st.markdown('<div class="section-title">2. Paste the job description</div>', unsafe_allow_html=True)
    jd = st.text_area("Job description", height=140, label_visibility="collapsed",
                      placeholder="Paste the full job description here...")

clicked = st.button("Check Your Score", type="primary")

if clicked:
    if not file or not jd.strip():
        st.warning("Please upload a resume and paste a job description.")
        st.stop()

    try:
        resume = extract_text(file)
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        st.stop()

    if len(resume) < 100:
        st.error("Couldn't extract text. Scanned/image PDFs aren't supported; upload a text-based PDF or DOCX.")
        st.stop()

    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(jd)
    matched = sorted(set(resume_skills) & set(jd_skills))
    missing = sorted(set(jd_skills) - set(resume_skills), key=lambda s: -jd.lower().count(s))

    sem = semantic_score(resume, jd)
    sk = skill_score(resume_skills, jd_skills)
    ats, checks = ats_check(resume)
    total = final_score(sem, sk, ats)

    st.markdown("&nbsp;", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1.5], gap="large")
    with col_a:
        st.markdown(ui.score_card(total), unsafe_allow_html=True)
        st.markdown(ui.tiles(sem, sk, ats), unsafe_allow_html=True)
    with col_b:
        st.markdown(ui.checklist_card(checks, missing), unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(ui.chips_card("Matched skills", matched, "g", "No matching skills found."),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(ui.chips_card("Missing skills (in the JD, not in your resume)", missing, "r",
                                  "None. Great coverage!"), unsafe_allow_html=True)

    st.markdown('<div class="section-title">💡 AI suggestions</div>', unsafe_allow_html=True)
    with st.spinner("Generating tailored suggestions..."):
        try:
            tips = get_suggestions(resume, jd, missing)
        except Exception as e:
            tips = None
            st.error(f"Suggestion service failed: {e}")
    if tips:
        st.markdown(tips)
    else:
        st.info("Add an ANTHROPIC_API_KEY in Streamlit secrets to enable AI-written suggestions.")

st.caption("Your resume is processed in memory and is never stored.")