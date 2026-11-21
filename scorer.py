"""Scoring: semantic similarity + skill overlap + ATS checks."""
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_st_model = None


def semantic_score(resume: str, jd: str) -> float:
    """0-1 similarity. Uses sentence-transformers if installed, else TF-IDF."""
    try:
        global _st_model
        from sentence_transformers import SentenceTransformer, util

        if _st_model is None:
            _st_model = SentenceTransformer("all-MiniLM-L6-v2")
        emb = _st_model.encode([resume, jd], convert_to_tensor=True)
        return max(0.0, min(1.0, float(util.cos_sim(emb[0], emb[1]))))
    except ImportError:
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vec.fit_transform([resume, jd])
        raw = float(cosine_similarity(matrix[0], matrix[1])[0][0])
        # TF-IDF scores run low; scale so typical good matches land ~0.5-0.8.
        # Tune this factor after testing on your own resume/JD pairs.
        return max(0.0, min(1.0, raw * 2.5))


def skill_score(resume_skills: list[str], jd_skills: list[str]) -> float:
    if not jd_skills:
        return 0.0
    return len(set(resume_skills) & set(jd_skills)) / len(set(jd_skills))


def ats_check(resume: str):
    """Returns (score 0-1, list of (label, passed))."""
    text = resume.lower()
    words = len(resume.split())
    checks = [
        ("Email address present", bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", resume))),
        ("Phone number present", bool(re.search(r"(\+?\d[\d\s-]{8,}\d)", resume))),
        ("Education section", "education" in text),
        ("Skills section", "skills" in text),
        ("Projects section", "project" in text),
        ("Experience / internship section", "experience" in text or "internship" in text),
        ("Reasonable length (250-1000 words)", 250 <= words <= 1000),
        ("Has numbers/metrics (%, counts)", bool(re.search(r"\d+\s?%|\d{2,}", resume))),
    ]
    score = sum(1 for _, ok in checks if ok) / len(checks)
    return score, checks


def final_score(sem: float, skill: float, ats: float) -> float:
    return round(100 * (0.50 * sem + 0.35 * skill + 0.15 * ats), 1)
