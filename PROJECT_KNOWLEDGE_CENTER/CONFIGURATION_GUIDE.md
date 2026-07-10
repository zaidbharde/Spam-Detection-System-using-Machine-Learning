# Configuration Guide

## Config Sources
- [src/config/config.py](../src/config/config.py): runtime paths and model grids.
- [pyproject.toml](../pyproject.toml): declared package metadata and dependencies.
- [requirements.txt](../requirements.txt): minimal install list.
- [.python-version](../.python-version): local Python pin.

## Current Runtime Settings
- Training data path: `data/dataset/dataset.csv`
- Validation mailbox path: `data/dataset/All_mail_Including_Spam_and_Trash.mbox`
- Output base directory: `outputs`
- Active model path: `outputs/2025-12-25_14-02-05/models/SVM_model.pkl`
- Active vectorizer path: `outputs/2025-12-25_14-02-05/models/vectorizer.pkl`

## Important Notes
- The active artifact paths are hardcoded.
- The validation mailbox path may not exist in every checkout.
- The README claims Python 3.10+, but the project metadata requires Python 3.13.

## Recommended Overrides
- Expose model artifact paths through environment variables.
- Keep a single stable `current_model` alias rather than a timestamped path.

## Configuration Troubleshooting
- If `app.py` fails at startup, verify the model pickle files exist at the configured paths.
- If training fails, verify `data/dataset/dataset.csv` exists and contains `Category` and `Message` columns.
