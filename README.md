# Resumorix: AI Resume Analyzer & Job Matcher

Upload your resume, paste a job description, and get an instant **match score**, **skill gap analysis** and **ATS readiness checklist**, plus optional AI-written suggestions tailored to the job.

**Live demo:** https://resumorix.streamlit.app/

## Features

- **Match score (0-100)** combining semantic similarity, skill overlap and ATS checks
- **Matched and missing skills**, with missing skills ranked by how often the job description mentions them
- **ATS checklist** covering contact details, key sections (Education, Skills, Projects, Experience), resume length and measurable results
- **AI suggestions (optional):** tailored resume bullets, project ideas to close skill gaps, and quick fixes, with a rule against inventing experience
- **Private by design:** resumes are processed in memory and never stored
- Supports **PDF and DOCX** resumes

## How the score works

| Component | Weight | What it measures |
|---|---|---|
| Semantic similarity | 50% | How close the resume text is to the job description (TF-IDF cosine similarity, or sentence-transformers embeddings if installed) |
| Skill overlap | 35% | Share of the job's required skills that appear in the resume |
| ATS readiness | 15% | Pass rate of 8 structural checks on the resume |

`final score = 100 x (0.50 x semantic + 0.35 x skills + 0.15 x ATS)`

## Tech stack

- **Python**
- **Streamlit** for the web interface
- **pdfplumber** and **python-docx** for reading resumes
- **scikit-learn** for TF-IDF and cosine similarity
- **Regex-based skill extraction** with a skills dictionary and aliases
- **Anthropic API** for optional AI suggestions

## Project structure

```
ai-resume-analyzer/
├── app.py              # Streamlit app (page flow)
├── ui.py               # HTML/CSS components (hero, score ring, checklist)
├── parser.py           # Extract text from PDF / DOCX
├── skills.py           # Skills dictionary and extraction
├── scorer.py           # Semantic, skill and ATS scoring
├── suggestions.py      # Optional LLM suggestions
├── requirements.txt
└── .streamlit/
    ├── config.toml             # Theme
    └── secrets.toml.example    # Template for the optional API key
```

## Limitations

- Scanned or image-based resumes are not supported
- The skills list is finite, so niche skills may be missed (extend `SKILLS` in `skills.py`)
- The score is a guide, not a prediction of any real company's ATS result
