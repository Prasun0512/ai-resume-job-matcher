# Production Readiness

## Deployment

- Expose matching as an API or batch scoring job.
- Keep resume/JD text transient unless explicit storage is required.
- Version skill catalogs and scoring weights.

## Security

- Treat resumes as sensitive personal data.
- Mask or avoid logging names, contact details, and private employment details.
- Do not send candidate data to external LLMs without policy approval.

## Monitoring

- Track match-score distribution, missing-skill patterns, and user feedback.
- Review false positives and false negatives by role family.

## Cost Optimization

- Use deterministic matching before invoking embedding or LLM calls.
- Cache parsed skills for repeated resumes and JDs.

## Scalability

- Batch parse resumes asynchronously.
- Store normalized skill profiles separately from raw documents.
- Add embedding search only after deterministic baselines are measured.
