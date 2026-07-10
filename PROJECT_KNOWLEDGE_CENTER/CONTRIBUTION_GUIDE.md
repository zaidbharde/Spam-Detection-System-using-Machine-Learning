# Contribution Guide

## How to Contribute
1. Fork or branch the repository.
2. Create a focused change in the relevant layer: UI, pipeline, config, or docs.
3. Run the training or inference path that your change affects.
4. Update documentation if behavior or paths change.
5. Keep model artifacts and generated outputs out of source control unless intentionally versioned.

## Repo Conventions
- Prefer small, single-purpose modules.
- Keep config values centralized.
- Use the existing logger instead of ad hoc print statements.
- Treat `outputs/` as generated artifacts, not hand-edited source.

## Review Checklist
- Does the change preserve the current artifact paths or update them consistently?
- Does the code still work with the saved model/vectorizer contract?
- Are edge cases handled for missing files and malformed inputs?
