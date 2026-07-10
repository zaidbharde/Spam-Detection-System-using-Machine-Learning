# Project Structure Analysis

## Annotated Tree
```text
Spam-Email-Detection-main/
├── app.py                        → Streamlit entry point for inference UI
├── pyproject.toml                → Project metadata and declared dependencies
├── requirements.txt              → Short dependency list for pip-based installs
├── README.md                     → High-level user-facing documentation
├── uv.lock                       → Lockfile for reproducible dependency resolution
├── data/
│   └── dataset/
│       ├── dataset.csv           → Training dataset used by the pipeline
│       └── All_mail_Including_Spam_and_Trash.mbox → Validation mailbox path referenced in config
├── logs/
│   └── 2026-06-12/               → Timestamped runtime logs from past runs
├── Notebook Experiments/
│   └── Spam Email Detection.ipynb → Exploratory notebook and prior experiments
├── outputs/
│   ├── 2025-12-25_10-01-23/      → Generated model artifacts and metrics from one training run
│   └── 2025-12-25_14-02-05/      → Generated model artifacts and metrics from the latest saved run
├── src/
│   ├── __init__.py               → Package marker
│   ├── components/               → Training-stage building blocks
│   ├── config/                   → Central configuration values and model grids
│   ├── pipeline/                 → Training and inference orchestration
│   └── utils/                    → Logging, state, and email parsing helpers
├── .gitignore                    → Ignore rules for logs, env files, caches, and virtualenvs
├── .python-version               → Local Python version pin
├── .idea/                        → IDE metadata; generated/local-only
└── .venv/                        → Local virtual environment; generated/local-only
```

## Folder-by-Folder Analysis

### Root
- Purpose: project coordination and entry points.
- Contents: source, docs, data, outputs, and workspace metadata.
- Criticality: Core.
- Who owns it: maintainers / technical lead.
- Dependencies: everything depends on the root layout being stable.
- Dependents: app launch, training scripts, docs, and artifact paths.
- Risk if deleted: complete project loss.

### data/
- Purpose: hold input datasets and mailbox fixtures.
- Contents: CSV training data and referenced MBOX archive.
- Criticality: Core for training, supporting for inference.
- Who owns it: data/ML engineer.
- Dependencies: training pipeline and notebook experiments.
- Dependents: `DataIngestion` and the notebook.
- Risk if deleted: training and validation paths break immediately.

### logs/
- Purpose: store runtime logs.
- Contents: dated log folders with timestamped `.log` files.
- Criticality: Supporting.
- Who owns it: DevOps / maintainers.
- Dependencies: `src/utils/logger.py`.
- Dependents: troubleshooting and audit review.
- Risk if deleted: no loss of source behavior, but reduced observability.

### Notebook Experiments/
- Purpose: exploratory analysis and ad hoc experimentation.
- Contents: a single Jupyter notebook.
- Criticality: Supporting / legacy.
- Who owns it: data scientist / ML engineer.
- Dependencies: dataset, library environment, and source logic.
- Dependents: none in runtime code.
- Risk if deleted: loss of experiment history and exploratory notes.

### outputs/
- Purpose: persist generated models and evaluation artifacts.
- Contents: model pickle files plus observation CSVs.
- Criticality: Generated.
- Who owns it: training pipeline.
- Dependencies: `ModelTraining`.
- Dependents: Streamlit inference via `Config.model_path` and `Config.feature_path`.
- Risk if deleted: inference breaks unless artifacts are regenerated.

### src/
- Purpose: application logic.
- Contents: pipeline orchestration, feature processing, config, utilities.
- Criticality: Core.
- Who owns it: engineering team.
- Dependencies: pandas, scikit-learn, BeautifulSoup4, mailbox, logging.
- Dependents: `app.py`, notebook experiments, training run entry points.
- Risk if deleted: the project ceases to function.

### src/components/
- Purpose: reusable training pipeline stages.
- Contents: data ingestion, transformation, model training.
- Criticality: Core.
- Who owns it: ML engineer.
- Dependencies: config and utility modules.
- Dependents: `TrainingPipeline`.
- Risk if deleted: training pipeline collapses.

### src/config/
- Purpose: centralized paths and model hyperparameter grids.
- Contents: `Config` and `ModelConfig`.
- Criticality: Configuration.
- Who owns it: maintainers / ML engineer.
- Dependencies: path layout and saved artifact names.
- Dependents: training and prediction pipelines.
- Risk if deleted: hardcoded behavior spreads elsewhere.

### src/pipeline/
- Purpose: end-to-end orchestration.
- Contents: training and prediction pipelines.
- Criticality: Core.
- Who owns it: ML engineer / application engineer.
- Dependencies: components, utils, config.
- Dependents: app.py and direct CLI training execution.
- Risk if deleted: no coordinated training or inference.

### src/utils/
- Purpose: supporting helpers.
- Contents: email parsing, logging, state objects, placeholder utility module.
- Criticality: Supporting.
- Who owns it: engineering team.
- Dependencies: standard library and BeautifulSoup.
- Dependents: almost every other module.
- Risk if deleted: pipeline code must duplicate helper logic.

### Hidden workspace folders
- `.gitignore`: protects local-only files and generated artifacts.
- `.python-version`: keeps local Python selection consistent.
- `.idea/`: IDE metadata, safe to delete but noisy in repos.
- `.venv/`: local environment, generated and machine-specific.

## Key Observations
- The repo is source-light and artifact-heavy.
- `outputs/` is effectively part of the runtime contract because inference loads files from it.
- The notebook is not required for production behavior.
- The current structure is intentionally simple, but training artifacts and source logic are somewhat interleaved through hardcoded paths.
