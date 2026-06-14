# Security and Governance

## Candidate Data Handling

- Do not commit real resumes or private job descriptions.
- Redact emails, phone numbers, addresses, and identifiers in examples.
- Keep local demo inputs synthetic.
- Apply retention and access controls in any real deployment.

## Responsible AI Controls

- The matcher is an explainable assistant, not a hiring decision engine.
- Do not infer protected attributes or sensitive personal characteristics.
- Present missing skills and evidence transparently.
- Require human review for any recruiting or career decision.

## Operational Governance

- Version scoring rules, synonym maps, and evaluation samples.
- Test for score regressions when changing extraction or matching logic.
- Log only sanitized summaries in production.
- Keep `.env` files out of git and use `.env.example` for configuration shape.
