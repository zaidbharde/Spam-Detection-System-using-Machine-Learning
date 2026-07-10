# Tech Stack

## Language and Runtime
- Python 3.13 is declared in [pyproject.toml](../pyproject.toml).
- The source uses the Python standard library plus common data-science packages.

## Frontend
- Streamlit powers the UI in [app.py](../app.py).

## Backend / Application Layer
- There is no separate web API layer.
- The pipeline logic lives in [src/pipeline/](../src/pipeline/) and [src/components/](../src/components/).

## Data and ML
- pandas for CSV and DataFrame handling.
- NumPy for array handling and confidence calculations.
- scikit-learn for train/test split, TF-IDF, grid search, classifiers, and metrics.
- BeautifulSoup4 for HTML stripping during email parsing.

## Infrastructure
- Local filesystem for dataset, logs, artifacts, and outputs.
- Timestamped model and log directories.

## DevOps
- No CI/CD, Docker, or deployment manifests were found.
- `uv.lock` is present, so dependency locking is supported at the workspace level.

## Monitoring
- Logging is file-based through [src/utils/logger.py](../src/utils/logger.py).
- There is no metrics backend or observability platform integration.

## Testing
- No test directory or pytest configuration was found.

## External Services
- None detected.

## Dependency Notes
- `fastapi`, `flask`, and `uvicorn` are declared but not used by the current source.
- `mailbox` is listed in `pyproject.toml`, but it is part of the Python standard library.
