from __future__ import annotations

import re
from dataclasses import dataclass, field


SKILL_CATALOG = {
    "azure openai": {
        "aliases": {"azure openai", "openai on azure", "azure ai foundry"},
        "category": "llm_platform",
        "weight": 1.25,
    },
    "rag": {
        "aliases": {"rag", "retrieval augmented generation", "grounded generation"},
        "category": "llm_architecture",
        "weight": 1.25,
    },
    "langchain": {"aliases": {"langchain"}, "category": "agentic_ai", "weight": 1.05},
    "langgraph": {"aliases": {"langgraph", "stategraph"}, "category": "agentic_ai", "weight": 1.2},
    "llama": {"aliases": {"llama", "open-source llm", "open source llm"}, "category": "llm_platform", "weight": 1.0},
    "python": {"aliases": {"python", "fastapi"}, "category": "engineering", "weight": 1.0},
    "mlops": {"aliases": {"mlops", "model monitoring", "model governance"}, "category": "production_ml", "weight": 1.0},
    "azure functions": {"aliases": {"azure functions", "serverless functions"}, "category": "cloud", "weight": 0.9},
    "service bus": {"aliases": {"service bus", "azure service bus", "queue"}, "category": "cloud", "weight": 0.85},
    "ocr": {"aliases": {"ocr", "document intelligence", "form recognizer"}, "category": "document_ai", "weight": 0.95},
    "text classification": {"aliases": {"text classification", "behavior scoring"}, "category": "ml", "weight": 0.85},
}

LEADERSHIP_TERMS = {
    "architect",
    "technical lead",
    "solution architect",
    "stakeholder",
    "production",
    "governance",
    "mentoring",
}


@dataclass(frozen=True)
class SkillMatch:
    skill: str
    category: str
    weight: float


@dataclass(frozen=True)
class MatchReport:
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    summary: str
    category_scores: dict[str, float] = field(default_factory=dict)
    leadership_score: float = 0.0
    recommendations: list[str] = field(default_factory=list)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text: str) -> set[str]:
    normalized = normalize(text)
    found: set[str] = set()
    for canonical, metadata in SKILL_CATALOG.items():
        aliases = metadata["aliases"]
        if any(alias in normalized for alias in aliases):
            found.add(canonical)
    return found


def _weighted_matches(skills: set[str]) -> list[SkillMatch]:
    return [
        SkillMatch(
            skill=skill,
            category=str(SKILL_CATALOG[skill]["category"]),
            weight=float(SKILL_CATALOG[skill]["weight"]),
        )
        for skill in sorted(skills)
    ]


def _coverage(matched: set[str], required: set[str]) -> float:
    if not required:
        return 0.0
    matched_weight = sum(float(SKILL_CATALOG[skill]["weight"]) for skill in matched)
    required_weight = sum(float(SKILL_CATALOG[skill]["weight"]) for skill in required)
    return matched_weight / required_weight


def _category_scores(matched: set[str], required: set[str]) -> dict[str, float]:
    categories = {str(SKILL_CATALOG[skill]["category"]) for skill in required}
    scores: dict[str, float] = {}
    for category in sorted(categories):
        required_in_category = {skill for skill in required if SKILL_CATALOG[skill]["category"] == category}
        matched_in_category = matched.intersection(required_in_category)
        scores[category] = round(_coverage(matched_in_category, required_in_category), 2)
    return scores


def _leadership_score(resume: str, job_description: str) -> float:
    resume_text = normalize(resume)
    jd_text = normalize(job_description)
    required_terms = {term for term in LEADERSHIP_TERMS if term in jd_text}
    if not required_terms:
        return 0.0
    matched_terms = {term for term in required_terms if term in resume_text}
    return round(len(matched_terms) / len(required_terms), 2)


def _recommendations(missing_skills: list[str], leadership_score: float) -> list[str]:
    recommendations: list[str] = []
    for skill in missing_skills[:4]:
        recommendations.append(f"Add a concrete project bullet showing hands-on {skill}.")
    if leadership_score and leadership_score < 0.75:
        recommendations.append("Strengthen architecture, stakeholder, and delivery leadership examples.")
    if not recommendations:
        recommendations.append("Resume is strongly aligned; tailor impact bullets to the exact role language.")
    return recommendations


def match_resume_to_job(resume: str, job_description: str) -> MatchReport:
    resume_skills = extract_skills(resume)
    required_skills = extract_skills(job_description)
    matched = resume_skills.intersection(required_skills)
    missing = sorted(required_skills.difference(resume_skills))
    coverage = _coverage(matched, required_skills)
    leadership = _leadership_score(resume, job_description)
    final_score = round((coverage * 0.82) + (leadership * 0.18 if leadership else 0), 2)
    summary = (
        f"Matched {len(matched)} of {len(required_skills)} technical requirements "
        f"with {int(final_score * 100)}% weighted alignment."
    )
    return MatchReport(
        score=final_score,
        matched_skills=[match.skill for match in _weighted_matches(matched)],
        missing_skills=missing,
        summary=summary,
        category_scores=_category_scores(matched, required_skills),
        leadership_score=leadership,
        recommendations=_recommendations(missing, leadership),
    )
