# Testing Guide

## Current State
No test suite, test runner config, or CI test job was found.

## What Should Be Tested
- CSV ingestion against the expected schema.
- Label transformation for `spam` and `ham`.
- TF-IDF vectorizer output shape and persistence.
- Model loading from `outputs/`.
- Single-email predictions and confidence formatting.
- MBOX parsing and batch export behavior.

## Suggested Test Layout
- `tests/test_data_ingestion.py`
- `tests/test_data_transformation.py`
- `tests/test_prediction_pipeline.py`
- `tests/test_email_utils.py`

## Manual Validation Steps
1. Run `python -m src.pipeline.training_pipeline` to regenerate artifacts.
2. Launch `streamlit run app.py`.
3. Paste a known spam email and a known ham email.
4. Upload a small MBOX sample and verify the output CSV.

## Risks
- Without tests, changes to the CSV schema or artifact paths can break the app silently.
