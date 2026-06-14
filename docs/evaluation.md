# Evaluation Strategy

Resume/JD matching should be explainable and advisory. The goal is to help candidates and recruiters discuss fit, not automate hiring decisions.

## What To Evaluate

- Skill extraction coverage.
- Synonym normalization accuracy.
- Weighted scoring stability.
- Missing-skill analysis quality.
- Leadership/architecture signal detection.
- Explanation clarity and responsible-AI wording.

## Local Checks

```bash
python -m unittest discover -s tests
python -m src.demo
```

## Quality Gates

- Scores must include evidence and missing-skill details.
- The tool must not infer protected attributes.
- Sample resumes and JDs must be synthetic or sanitized.
- Output should be treated as advisory and reviewed by a human.

## Future Improvements

- Add embedding-based similarity behind an optional dependency.
- Add Markdown report export.
- Add FastAPI or simple web demo for recruiter-friendly use.
