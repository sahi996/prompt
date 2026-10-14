"""
AI service wrapper.
Uses OpenAI API when key is available; falls back to rule engine transparently.
"""
import json
import logging
from flask import current_app

logger = logging.getLogger(__name__)


def get_career_recommendations(assessment) -> tuple[list[dict], bool]:
    """
    Returns (recommendations_list, used_ai).
    recommendations_list: [{slug, score, reason, ai_explanation}]
    used_ai: True if the OpenAI API was used, False if rule engine was used.
    """
    from app.ai_services.rule_engine import rule_based_score
    base = rule_based_score(assessment)

    api_key = current_app.config.get("OPENAI_API_KEY", "")
    if not api_key:
        return base, False

    try:
        return _openai_enrich(assessment, base, api_key), True
    except Exception as exc:
        logger.warning("OpenAI enrichment failed, using rule engine: %s", exc)
        return base, False


def _openai_enrich(assessment, base: list[dict], api_key: str) -> list[dict]:
    import httpx

    slugs = [r["slug"] for r in base]
    interests = json.loads(assessment.interests or "[]")
    activities = json.loads(assessment.preferred_activities or "[]")

    prompt = (
        "You are a career counsellor. Based on the student profile below, "
        "write a short, warm, personalised explanation (2-3 sentences) for why "
        f"each of these career options may suit them: {', '.join(slugs)}.\n\n"
        f"Profile:\n"
        f"- Education: {assessment.education_level}\n"
        f"- Field of study: {assessment.field_of_study}\n"
        f"- Interests: {', '.join(interests)}\n"
        f"- Technical skills: {assessment.technical_skills}\n"
        f"- Preferred activities: {', '.join(activities)}\n"
        f"- Career goals: {assessment.career_goals}\n\n"
        "Respond as a JSON object where each key is a career slug and the value is the explanation string. "
        "Do not add any text outside the JSON."
    )

    model = current_app.config.get("OPENAI_MODEL", "gpt-3.5-turbo")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 600,
        "temperature": 0.7,
    }

    with httpx.Client(timeout=20) as client:
        resp = client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=body,
        )
        resp.raise_for_status()

    raw = resp.json()["choices"][0]["message"]["content"].strip()
    explanations: dict = json.loads(raw)

    for item in base:
        item["ai_explanation"] = explanations.get(item["slug"], "")

    return base


def generate_interview_feedback(question: str, answer: str, career_title: str) -> str:
    """
    Returns brief feedback on an interview answer.
    Falls back to a generic tip when AI is unavailable.
    """
    api_key = current_app.config.get("OPENAI_API_KEY", "")
    if not api_key:
        return _fallback_feedback(answer)

    try:
        import httpx
        prompt = (
            f"Career: {career_title}\n"
            f"Interview question: {question}\n"
            f"Candidate answer: {answer}\n\n"
            "Provide brief, constructive feedback in 2-3 sentences: what was done well, "
            "and one specific suggestion for improvement. Be encouraging and professional."
        )
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        body = {
            "model": current_app.config.get("OPENAI_MODEL", "gpt-3.5-turbo"),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
            "temperature": 0.6,
        }
        with httpx.Client(timeout=15) as client:
            resp = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
            resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        logger.warning("Interview feedback AI failed: %s", exc)
        return _fallback_feedback(answer)


def _fallback_feedback(answer: str) -> str:
    length = len(answer.split())
    if length < 20:
        return (
            "Your answer is quite brief. Try to expand with a specific example using the STAR method "
            "(Situation, Task, Action, Result) to make your response more compelling."
        )
    return (
        "Good start! Make sure to include a concrete example that demonstrates your skills. "
        "Quantify your results where possible (e.g. 'improved performance by 30%')."
    )


def generate_resume_objective(profile_data: dict) -> str:
    """Generate a resume objective/summary. Falls back to a template."""
    api_key = current_app.config.get("OPENAI_API_KEY", "")
    if not api_key:
        return _fallback_objective(profile_data)

    try:
        import httpx
        prompt = (
            "Write a professional 2-sentence resume objective for a job seeker with the following profile. "
            "Do not invent qualifications or experience not mentioned.\n\n"
            f"Name: {profile_data.get('full_name', 'the candidate')}\n"
            f"Education: {profile_data.get('education_level', '')}\n"
            f"Field: {profile_data.get('field_of_study', '')}\n"
            f"Target career: {profile_data.get('target_career', '')}\n"
            f"Skills: {profile_data.get('skills', '')}\n"
            f"Goal: {profile_data.get('career_goal', '')}"
        )
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        body = {
            "model": current_app.config.get("OPENAI_MODEL", "gpt-3.5-turbo"),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150,
            "temperature": 0.7,
        }
        with httpx.Client(timeout=15) as client:
            resp = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
            resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        logger.warning("Resume objective AI failed: %s", exc)
        return _fallback_objective(profile_data)


def _fallback_objective(profile_data: dict) -> str:
    name = profile_data.get("full_name", "I")
    target = profile_data.get("target_career", "a relevant role")
    field = profile_data.get("field_of_study", "")
    field_part = f" in {field}" if field else ""
    return (
        f"A motivated {field_part.strip()} graduate seeking an entry-level position as a {target}. "
        "Eager to apply academic knowledge and practical skills to contribute to a dynamic team."
    )
