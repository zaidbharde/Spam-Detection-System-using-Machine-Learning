# Project Summary

## Project Identity
- Name: Spam Email Classification System
- Version: 0.1.0 from [pyproject.toml](../pyproject.toml)
- Tagline: A Streamlit-based machine learning app for classifying email text as spam or ham.
- Primary entry point: [app.py](../app.py)
- Training entry point: [src/pipeline/training_pipeline.py](../src/pipeline/training_pipeline.py)

## Problem Statement
The project addresses a common email triage problem: separating unwanted spam from legitimate mail quickly and with reasonable accuracy. The repository is aimed at reducing manual review time for both individual messages and batches of archived emails.

## Solution Summary
The implementation uses a file-backed, scikit-learn text classification pipeline. Training ingests a CSV dataset, normalizes labels, builds TF-IDF features, evaluates several candidate models with grid search, and persists the best model and vectorizer. The Streamlit UI then loads those artifacts and predicts either a pasted email or each message in an MBOX archive.

## Intended Users
- Primary: people who want to classify email text interactively.
- Secondary: developers or analysts experimenting with binary text classification.
- Technical level: moderate Python familiarity for training, low technical friction for inference because the UI is browser-based.

## Core Value Proposition
One-sentence value: turn raw email text into a spam or ham decision, with the selected model and confidence exposed in a simple UI.

## Major Features
- Single-email classification: paste text and get a spam/ham result with a confidence value when the model supports it.
- Batch MBOX processing: parse an MBOX archive, extract message metadata and bodies, and generate a CSV of predictions.
- Model comparison: train Logistic Regression, Decision Tree, SVM, KNN, and Random Forest with grid search and cross-validation.
- Artifact persistence: save the TF-IDF vectorizer, best model, and summary metrics under `outputs/`.
- Logging: write pipeline logs under `logs/` with timestamped filenames.

## Technology Stack
- Frontend: Streamlit.
- Backend/runtime: Python 3.13 per [pyproject.toml](../pyproject.toml) and scikit-learn pipelines.
- Database: none detected; the project is file-backed.
- Infrastructure: local filesystem for dataset, logs, and serialized artifacts.
- DevOps: none detected; no CI/CD or Docker files were found.
- AI/ML: pandas, NumPy, BeautifulSoup4, scikit-learn.
- Testing: no automated test suite detected.
- Monitoring: basic file logging only.

## External Services
No third-party hosted APIs or SaaS integrations were found in the source. The only external packages are local Python dependencies.

## Runtime Environment
- Operating system: works on macOS in the current workspace; nothing in the source is OS-specific beyond local file paths and Python.
- Python: `>=3.13` in [pyproject.toml](../pyproject.toml); the README still claims Python 3.10+, which appears stale.
- Memory/CPU: modest local machine is sufficient for inference; training benefits from multiple CPU cores because `GridSearchCV` uses `n_jobs=-1`.
- Storage: enough space for serialized models, logs, and the `outputs/` tree.

## Licensing & Compliance Notes
- The README says MIT, but no `LICENSE` file was present in the workspace. ⚠️ ASSUMPTION: treat the license as unconfirmed until a license file is added.
- The project uses standard OSS dependencies from PyPI; downstream redistribution should preserve their notices and terms.
