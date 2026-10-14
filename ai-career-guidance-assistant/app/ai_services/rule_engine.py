"""
AI Career Guidance — rule-based recommendation engine.
Used when no OpenAI API key is configured or when the API call fails.
"""

# Scoring weights: interest keyword → career slug → score contribution
INTEREST_WEIGHTS = {
    "programming": {
        "python-developer": 10,
        "web-developer": 8,
        "software-tester": 6,
        "ai-ml-engineer": 7,
        "cloud-engineer": 5,
    },
    "data": {
        "data-analyst": 10,
        "ai-ml-engineer": 9,
        "business-analyst": 7,
        "python-developer": 6,
    },
    "design": {
        "ui-ux-designer": 10,
        "web-developer": 6,
        "digital-marketing-specialist": 5,
    },
    "business": {
        "business-analyst": 10,
        "digital-marketing-specialist": 8,
        "cybersecurity-analyst": 4,
    },
    "security": {
        "cybersecurity-analyst": 10,
        "cloud-engineer": 6,
        "software-tester": 5,
    },
    "ai_ml": {
        "ai-ml-engineer": 10,
        "data-analyst": 8,
        "python-developer": 6,
    },
    "cloud": {
        "cloud-engineer": 10,
        "cybersecurity-analyst": 6,
        "software-tester": 5,
    },
    "writing": {
        "digital-marketing-specialist": 9,
        "business-analyst": 7,
        "ui-ux-designer": 5,
    },
    "teaching": {
        "python-developer": 4,
        "web-developer": 4,
        "data-analyst": 4,
    },
    "problem_solving": {
        "python-developer": 8,
        "data-analyst": 8,
        "cybersecurity-analyst": 8,
        "ai-ml-engineer": 8,
        "business-analyst": 7,
    },
}

ACTIVITY_WEIGHTS = {
    "coding": {"python-developer": 10, "web-developer": 9, "ai-ml-engineer": 8, "software-tester": 6},
    "analysing": {"data-analyst": 10, "business-analyst": 9, "ai-ml-engineer": 7},
    "designing": {"ui-ux-designer": 10, "web-developer": 7, "digital-marketing-specialist": 6},
    "communicating": {"digital-marketing-specialist": 9, "business-analyst": 8, "ui-ux-designer": 6},
    "researching": {"data-analyst": 9, "ai-ml-engineer": 8, "cybersecurity-analyst": 7},
    "building": {"web-developer": 9, "python-developer": 8, "cloud-engineer": 8},
    "helping": {"ui-ux-designer": 7, "business-analyst": 7, "digital-marketing-specialist": 6},
    "strategising": {"business-analyst": 10, "digital-marketing-specialist": 8, "cloud-engineer": 6},
}

MATCH_REASONS = {
    "python-developer": "You show interest in programming and problem-solving — Python development is a great fit.",
    "web-developer": "Your enthusiasm for building things and coding aligns well with web development.",
    "data-analyst": "You enjoy working with data and finding patterns — data analysis matches your profile.",
    "ai-ml-engineer": "Your interest in AI, data, and research maps directly to machine learning engineering.",
    "cybersecurity-analyst": "Your security interests and problem-solving skills suit a career in cybersecurity.",
    "ui-ux-designer": "Your creativity and interest in design point toward a strong UX design career.",
    "cloud-engineer": "Your interest in cloud infrastructure and building scalable systems fits cloud engineering.",
    "software-tester": "Your systematic approach and programming interest align with software quality assurance.",
    "digital-marketing-specialist": "Your communication and writing skills pair well with digital marketing.",
    "business-analyst": "Your strategic thinking and business interests are a strong match for business analysis.",
}


def rule_based_score(assessment) -> list[dict]:
    """
    Returns a sorted list of {slug, score, reason} dicts.
    `assessment` is an Assessment ORM object.
    """
    import json
    scores: dict[str, float] = {}

    def add(slug, points):
        scores[slug] = scores.get(slug, 0) + points

    interests = json.loads(assessment.interests or "[]")
    for interest in interests:
        for slug, pts in INTEREST_WEIGHTS.get(interest, {}).items():
            add(slug, pts)

    activities = json.loads(assessment.preferred_activities or "[]")
    for activity in activities:
        for slug, pts in ACTIVITY_WEIGHTS.get(activity, {}).items():
            add(slug, pts)

    # Boost for technical keywords in free-text fields
    tech_text = (assessment.technical_skills or "").lower()
    if any(kw in tech_text for kw in ["python", "django", "flask"]):
        add("python-developer", 8)
    if any(kw in tech_text for kw in ["html", "css", "javascript", "react"]):
        add("web-developer", 8)
    if any(kw in tech_text for kw in ["sql", "excel", "tableau", "pandas"]):
        add("data-analyst", 8)
    if any(kw in tech_text for kw in ["machine learning", "tensorflow", "pytorch", "scikit"]):
        add("ai-ml-engineer", 8)
    if any(kw in tech_text for kw in ["aws", "azure", "gcp", "docker", "kubernetes"]):
        add("cloud-engineer", 8)
    if any(kw in tech_text for kw in ["figma", "adobe", "sketch", "ux"]):
        add("ui-ux-designer", 8)
    if any(kw in tech_text for kw in ["network", "kali", "wireshark", "security"]):
        add("cybersecurity-analyst", 8)

    results = sorted(
        [{"slug": slug, "score": score, "reason": MATCH_REASONS.get(slug, "")}
         for slug, score in scores.items()],
        key=lambda x: x["score"],
        reverse=True,
    )
    return results[:5]  # top 5
