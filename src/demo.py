from .matcher import match_resume_to_job


def main() -> None:
    resume = "AI architect with Python, Azure OpenAI, RAG, LangChain and MLOps experience."
    jd = "Looking for Python, Azure OpenAI, RAG, LangGraph, LangChain and MLOps."
    print(match_resume_to_job(resume, jd))


if __name__ == "__main__":
    main()
