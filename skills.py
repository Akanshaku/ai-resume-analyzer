"""Skill dictionary + extraction. Add more skills/aliases as you like."""
import re

# canonical skill -> list of aliases
SKILLS = {
    # languages
    "python": [], "java": [], "javascript": ["js"], "typescript": ["ts"],
    "c++": ["cpp"], "c#": ["csharp"], "golang": [], "kotlin": [], "swift": [],
    "php": [], "ruby": [], "scala": [], "r programming": [], "bash": ["shell scripting"],
    # web / backend
    "html": ["html5"], "css": ["css3"], "react": ["reactjs", "react.js"],
    "angular": [], "vue": ["vuejs", "vue.js"], "node.js": ["nodejs", "node"],
    "express": ["expressjs", "express.js"], "django": [], "flask": [],
    "fastapi": [], "spring boot": ["springboot"], "spring": [], "hibernate": [],
    ".net": ["dotnet", "asp.net"], "rest api": ["rest", "restful", "restful api", "rest apis"],
    "graphql": [], "microservices": ["microservice"], "tailwind": ["tailwindcss"],
    "bootstrap": [], "next.js": ["nextjs"],
    # databases
    "sql": [], "mysql": [], "postgresql": ["postgres"], "mongodb": ["mongo"],
    "oracle": [], "sqlite": [], "redis": [], "nosql": [], "elasticsearch": [],
    # cloud / devops
    "aws": ["amazon web services"], "azure": [], "gcp": ["google cloud"],
    "docker": [], "kubernetes": ["k8s"], "jenkins": [], "terraform": [],
    "ci/cd": ["cicd", "ci cd"], "github actions": [], "linux": [], "git": [],
    "github": [], "devops": [],
    # data / AI
    "machine learning": ["ml"], "deep learning": [], "nlp": ["natural language processing"],
    "computer vision": [], "generative ai": ["genai", "gen ai"], "llm": ["llms", "large language models"],
    "rag": ["retrieval augmented generation", "retrieval-augmented generation"],
    "langchain": [], "llamaindex": [], "prompt engineering": [],
    "tensorflow": [], "pytorch": [], "keras": [], "scikit-learn": ["sklearn"],
    "pandas": [], "numpy": [], "matplotlib": [], "seaborn": [], "spacy": [],
    "hugging face": ["huggingface", "transformers"], "mlops": [], "xgboost": [],
    "data analysis": ["data analytics"], "data visualization": [],
    "power bi": ["powerbi"], "tableau": [], "excel": [], "statistics": [],
    "etl": [], "spark": ["pyspark"], "hadoop": [], "kafka": [], "airflow": [],
    # fundamentals
    "data structures": ["dsa", "data structures and algorithms"], "algorithms": [],
    "oop": ["object oriented programming", "object-oriented programming"],
    "operating systems": [], "computer networks": [], "dbms": [],
    "system design": [], "design patterns": [],
    # testing / process
    "unit testing": [], "junit": [], "pytest": [], "selenium": [], "postman": [],
    "agile": [], "scrum": [], "jira": [], "testing": [],
    # security
    "cybersecurity": ["cyber security", "information security"], "owasp": [],
    "penetration testing": [], "networking": [],
    # mobile
    "android": [], "flutter": [], "react native": [],
}


def _pattern(term: str) -> re.Pattern:
    # Not preceded/followed by letters, digits, + or # (so "java" != "javascript")
    return re.compile(rf"(?<![a-z0-9+#]){re.escape(term)}(?![a-z0-9+#])")


_PATTERNS = {
    canon: [_pattern(t) for t in [canon, *aliases]]
    for canon, aliases in SKILLS.items()
}


def extract_skills(text: str) -> list[str]:
    text = text.lower()
    found = [
        canon for canon, patterns in _PATTERNS.items()
        if any(p.search(text) for p in patterns)
    ]
    return sorted(found)
