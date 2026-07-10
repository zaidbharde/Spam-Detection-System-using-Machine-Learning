# Future Improvements

## Recommended Next Steps
- Add automated tests for ingestion, transformation, and inference.
- Replace hardcoded artifact paths with a stable active-model pointer.
- Introduce a model registry-style manifest for run tracking.
- Add input schema validation before training and prediction.
- Add calibration or clearer wording for confidence estimates.
- Consider a more production-friendly deployment path if the app becomes public.

## ML Improvements
- Compare TF-IDF with embeddings or character n-grams.
- Track minority-class metrics separately from weighted averages.
- Add explainability output for top contributing terms.

## Engineering Improvements
- Convert state bags to dataclasses.
- Split mailbox parsing from prediction orchestration.
- Remove unused dependencies from `pyproject.toml`.
- Add linting and formatting automation.
