"""Optional LLM suggestions. Skipped automatically if no API key is set."""
import os


def get_suggestions(resume_text: str, jd_text: str, missing: list[str]):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=key)
    prompt = f"""You are a career coach reviewing a fresher's resume against a job description.

RESUME:
{resume_text[:6000]}

JOB DESCRIPTION:
{jd_text[:4000]}

SKILLS IN THE JD MISSING FROM THE RESUME: {", ".join(missing) or "none"}

Give:
1. Five improved resume bullet points tailored to this job. Rewrite only what the
   resume already supports. Do NOT invent experience, tools, or numbers; if a metric
   is missing, write [add metric] as a placeholder.
2. Three specific project ideas that would close the biggest skill gaps.
3. Two quick fixes for the resume's wording or structure.
Keep it concise and in plain bullet points."""

    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text
