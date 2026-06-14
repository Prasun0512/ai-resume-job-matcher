import unittest

from src.matcher import extract_skills, match_resume_to_job


class MatcherTests(unittest.TestCase):
    def test_extract_skills_finds_aliases(self) -> None:
        skills = extract_skills("Retrieval Augmented Generation with OpenAI on Azure")
        self.assertIn("rag", skills)
        self.assertIn("azure openai", skills)

    def test_match_report_identifies_missing_skills(self) -> None:
        report = match_resume_to_job("Python and RAG", "Python RAG LangGraph")
        self.assertIn("langgraph", report.missing_skills)
        self.assertGreater(report.score, 0)
        self.assertIn("agentic_ai", report.category_scores)

    def test_leadership_alignment_is_scored(self) -> None:
        report = match_resume_to_job(
            "Technical Lead and solution architect delivering production RAG on Azure OpenAI.",
            "Need a solution architect for production Azure OpenAI RAG systems.",
        )
        self.assertGreaterEqual(report.leadership_score, 0.5)
        self.assertGreater(report.score, 0.5)


if __name__ == "__main__":
    unittest.main()
