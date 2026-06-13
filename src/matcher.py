from __future__ import annotations

import re
from dataclasses import dataclass


SKILL_ALIASES = {
    "azure openai": {"azure openai", "openai on azure"},
    "rag": {"rag", "retrieval augmented generation"},
    "langchain": {"langchain"},
    "langgraph": {"langgraph"},
    "python": {"python"},
    "mlops": {"mlops", "model monitoring"},
}


@dataclass(frozen=True)
class MatchReport:
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    summary: str


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text: str) -> set[str]:
    normalized = normalize(text)
    found: set[str] = set()
    for canonical, aliases in SKILL_ALIASES.items():
        if any(alias in normalized for alias in aliases):
            found.add(canonical)
    return found


def match_resume_to_job(resume: str, job_description: str) -> MatchReport:
    resume_skills = extract_skills(resume)
    required_skills = extract_skills(job_description)
    matched = sorted(resume_skills.intersection(required_skills))
    missing = sorted(required_skills.difference(resume_skills))
    score = len(matched) / len(required_skills) if required_skills else 0.0
    summary = f"Matched {len(matched)} of {len(required_skills)} required skills."
    return MatchReport(score=score, matched_skills=matched, missing_skills=missing, summary=summary)
