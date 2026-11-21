"""Extract clean text from an uploaded PDF or DOCX resume."""
import io
import re

import docx
import pdfplumber


def clean_text(text: str) -> str:
    text = text.replace("\u2022", "- ").replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    data = uploaded_file.read()

    if name.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            text = "\n".join((page.extract_text() or "") for page in pdf.pages)
    elif name.endswith(".docx"):
        document = docx.Document(io.BytesIO(data))
        text = "\n".join(p.text for p in document.paragraphs)
    else:
        raise ValueError("Please upload a PDF or DOCX file.")

    return clean_text(text)
