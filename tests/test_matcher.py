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


if __name__ == "__main__":
    unittest.main()
