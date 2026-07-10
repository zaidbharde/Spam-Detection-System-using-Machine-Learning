# File-Level Deep Analysis

## app.py
**Path**: [app.py](../app.py)
**Type**: UI / Application
**Criticality**: High
**Last Known Change Indicator**: Imports the prediction pipeline and depends on saved artifacts in `outputs/`.

### Purpose
Provides the Streamlit user interface for single-email spam classification and batch MBOX processing.

### Responsibility
Single responsibility is interactive inference presentation. It mostly keeps that boundary, although it also handles some temporary-file lifecycle work for uploads.

### Key Functions / Classes
| Name | Type | Inputs | Outputs | Side Effects | Complexity |
|------|------|--------|---------|--------------|------------|
| get_pipeline() | function | none | PredictionPipeline | caches model loading | O(1) on warm runs |

### Dependencies (Imports)
- `streamlit` → UI framework.
- `pandas` → DataFrame display and CSV export.
- `tempfile`, `os`, `time` → upload handling and output naming.
- `src.pipeline.prediction_pipeline.PredictionPipeline` → core inference engine.

### Dependents (Who Imports This)
- None in source; this is a top-level entry point.

### Data Flow
User input -> Streamlit widget -> prediction pipeline -> displayed label and confidence.

### Risks & Code Smells
- Runtime fails if the saved model artifacts are missing or stale.
- Upload handling uses a temporary file and manual cleanup, which is fine but should be tested.

### Improvement Opportunities
- Add a health status block for missing artifacts.
- Surface the model version being loaded.

## src/config/config.py
**Path**: [src/config/config.py](../src/config/config.py)
**Type**: Config
**Criticality**: High
**Last Known Change Indicator**: Centralized artifact paths and model grids.

### Purpose
Holds training paths, output directory settings, and the hyperparameter grids used by `GridSearchCV`.

### Responsibility
Centralize configuration. It is doing that cleanly, but the artifact paths are hardcoded to one timestamped output directory.

### Key Functions / Classes
| Name | Type | Inputs | Outputs | Side Effects | Complexity |
|------|------|--------|---------|--------------|------------|
| Config | dataclass | none | config object | none | O(1) |
| ModelConfig | class | none | dict of grids | none | O(1) |

### Dependencies (Imports)
- `dataclasses.dataclass` → simple configuration container.

### Dependents (Who Imports This)
- `DataIngestion`, `DataTransformation`, `ModelTraining`, and `PredictionPipeline`.

### Risks & Code Smells
- Hardcoded model and vectorizer paths couple inference to one specific training run.
- The validation path references an MBOX file that may not exist in every checkout.

### Improvement Opportunities
- Replace timestamped artifact paths with a stable alias or environment override.
- Validate paths at startup.

## src/pipeline/training_pipeline.py
**Path**: [src/pipeline/training_pipeline.py](../src/pipeline/training_pipeline.py)
**Type**: Pipeline
**Criticality**: Critical
**Last Known Change Indicator**: Orchestrates data ingestion, transformation, and model training.

### Purpose
Coordinates the full training workflow from CSV ingestion through model selection and artifact persistence.

### Responsibility
The orchestration boundary is appropriate. It does not perform model logic itself; it delegates to the component layer.

### Key Functions / Classes
| Name | Type | Inputs | Outputs | Side Effects | Complexity |
|------|------|--------|---------|--------------|------------|
| run_pipeline() | method | cv_folds | TrainingState | reads CSV, writes artifacts, logs progress | O(models × folds × search space) |

### Dependencies (Imports)
- `src.components.data_ingestion.DataIngestion`
- `src.components.data_transformation.DataTransformation`
- `src.components.model_training.ModelTraining`
- `src.utils.state.TrainingState`
- `src.utils.logger.get_logger`

### Dependents (Who Imports This)
- Notebook experiments and direct CLI execution via the module main block.

### Risks & Code Smells
- Exception handling re-raises raw exceptions without typed context.
- Logging says outputs are saved to `results/`, but the code actually writes to `outputs/`.

### Improvement Opportunities
- Fix the stale log message.
- Return richer run metadata.

## src/pipeline/prediction_pipeline.py
**Path**: [src/pipeline/prediction_pipeline.py](../src/pipeline/prediction_pipeline.py)
**Type**: Pipeline
**Criticality**: Critical
**Last Known Change Indicator**: Loads pickled artifacts and performs single-email or mailbox inference.

### Purpose
Implements inference for pasted email text and for MBOX archives.

### Responsibility
This file is the runtime inference brain. It includes mailbox parsing, feature generation, prediction, and confidence estimation.

### Key Functions / Classes
| Name | Type | Inputs | Outputs | Side Effects | Complexity |
|------|------|--------|---------|--------------|------------|
| _load_models() | method | none | loads model/vectorizer | reads pickle files | O(1) |
| predict_single_email() | method | email_body | dict | model inference | O(n_features) |
| process_mailbox() | method | mailbox_path | list[dict] | reads mailbox, closes handle | O(messages) |
| run_prediction() | method | mail_data | list[dict] | adds predictions to records | O(messages) |
| predict_mbox_file() | method | mailbox_path | DataFrame | orchestrates full batch flow | O(messages) |

### Dependencies (Imports)
- `mailbox`, `pickle`, `time`, `pathlib.Path`.
- `numpy`, `pandas`.
- `src.utils.email_utils.extract_body`, `all_recipients`, `clean_text`.
- `src.config.config.Config`.
- `src.utils.state.PredictionState` for the legacy helper.

### Dependents (Who Imports This)
- `app.py` and the legacy pipeline helper.

### Risks & Code Smells
- Untrusted pickle loading is a supply-chain risk if artifact files are replaced.
- Batch prediction assumes `Body` exists in each record and that `clean_text` is sufficient for all message variants.

### Improvement Opportunities
- Add artifact integrity checks.
- Split mailbox parsing from model inference for easier testing.

## src/components/data_ingestion.py
**Path**: [src/components/data_ingestion.py](../src/components/data_ingestion.py)
**Type**: Service
**Criticality**: High
**Last Known Change Indicator**: Reads the training CSV into state.

### Purpose
Loads the training dataset into the shared training state.

### Responsibility
Very narrow: read CSV from disk and attach it to the state object.

### Dependencies (Imports)
- `pandas`
- `src.utils.logger.get_logger`
- `src.config.config.Config`
- `src.utils.state.TrainingState`

### Dependents (Who Imports This)
- `TrainingPipeline`

### Risks & Code Smells
- No schema validation for the CSV.
- The code assumes the configured path exists and contains the expected columns.

## src/components/data_transformation.py
**Path**: [src/components/data_transformation.py](../src/components/data_transformation.py)
**Type**: Service
**Criticality**: Critical
**Last Known Change Indicator**: Encodes labels and creates TF-IDF features.

### Purpose
Transforms raw text data into model-ready training and test sets.

### Responsibility
Handles label encoding, train/test split, and TF-IDF vectorization. This is appropriately focused, though it depends on the dataset having exactly `Message` and `Category` columns.

### Key Functions / Classes
| Name | Type | Inputs | Outputs | Side Effects | Complexity |
|------|------|--------|---------|--------------|------------|
| transform_data() | method | TrainingState | TrainingState | mutates state with split data and vectorizer | O(n) plus vectorization |

### Dependencies (Imports)
- `train_test_split`, `TfidfVectorizer`
- `numpy`

### Dependents (Who Imports This)
- `TrainingPipeline`

### Risks & Code Smells
- Hardcoded label mapping is case-sensitive and only works if labels are exactly `spam` and `ham` in lowercase after prior ingestion.
- The conversion to `int` will fail if unexpected categories appear.

## src/components/model_training.py
**Path**: [src/components/model_training.py](../src/components/model_training.py)
**Type**: Service
**Criticality**: Critical
**Last Known Change Indicator**: Trains and serializes model candidates.

### Purpose
Trains multiple classical ML classifiers, evaluates them, and saves the winning model plus metrics.

### Responsibility
This file owns model search, evaluation, selection, and artifact writing. It is the heart of the training workflow.

### Key Functions / Classes
| Name | Type | Inputs | Outputs | Side Effects | Complexity |
|------|------|--------|---------|--------------|------------|
| train_models() | method | TrainingState, cv_folds | TrainingState | grid search, model persistence, CSV exports | O(models × folds × params) |
| save_pickle_files() | method | TrainingState | output_dir | writes pickle and metadata files | O(1) |
| save_metrics_to_csv() | method | TrainingState, output_dir | none | writes summary CSVs | O(models) |

### Dependencies (Imports)
- scikit-learn model classes and metrics.
- `GridSearchCV`, `cross_val_score` import exists, although `cross_val_score` is not used.
- `pandas`, `numpy`, `pickle`, `os`, `json`, `datetime`.

### Dependents (Who Imports This)
- `TrainingPipeline`

### Risks & Code Smells
- Pickle serialization is convenient but unsafe for untrusted artifacts.
- One unused import (`cross_val_score`) indicates cleanup debt.
- Artifact paths are timestamped, so inference depends on config pointing at a specific run.

### Improvement Opportunities
- Add artifact naming indirection.
- Save a model manifest for runtime selection.

## src/utils/email_utils.py
**Path**: [src/utils/email_utils.py](../src/utils/email_utils.py)
**Type**: Utility
**Criticality**: High
**Last Known Change Indicator**: Handles message body extraction and Excel-safe text cleaning.

### Purpose
Parses MBOX messages into readable text and cleans strings for export or downstream processing.

### Responsibility
Utility extraction. It combines message parsing, HTML stripping, and Excel-safety cleanup, which are related but could be split if the file grows.

### Key Functions / Classes
| Name | Type | Inputs | Outputs | Side Effects | Complexity |
|------|------|--------|---------|--------------|------------|
| extract_body() | function | mailbox message | string | parses email payloads | O(parts) |
| all_recipients() | function | mailbox message | string | none | O(headers) |
| clean_text() | function | text | cleaned text | none | O(length) |

### Dependencies (Imports)
- `re`, `html.unescape`, `email.utils.getaddresses`, `BeautifulSoup`

### Dependents (Who Imports This)
- `PredictionPipeline`

### Risks & Code Smells
- HTML parsing is permissive and may flatten formatting aggressively.
- The cleaning logic truncates output to Excel’s cell limit, which is correct for export but lossy.

## src/utils/logger.py
**Path**: [src/utils/logger.py](../src/utils/logger.py)
**Type**: Utility
**Criticality**: Medium
**Last Known Change Indicator**: Creates timestamped file logs.

### Purpose
Provides a shared logger with a single file destination per process run.

### Responsibility
Centralized logging setup. This is clean and lightweight.

### Dependencies (Imports)
- `logging`, `pathlib.Path`, `datetime`

### Dependents (Who Imports This)
- Most runtime modules.

### Risks & Code Smells
- The module-level `_LOG_FILE` keeps state across logger calls, which is intended but should be understood during tests.

## src/utils/state.py
**Path**: [src/utils/state.py](../src/utils/state.py)
**Type**: Model / State
**Criticality**: Medium
**Last Known Change Indicator**: Mutable container for pipeline state.

### Purpose
Defines lightweight containers for training and prediction state.

### Responsibility
State transport only. There is no validation or behavior here.

### Risks & Code Smells
- The classes are plain attribute bags rather than typed dataclasses, so they are easy to mutate incorrectly.

## README.md
**Path**: [README.md](../README.md)
**Type**: Documentation
**Criticality**: Medium
**Last Known Change Indicator**: Describes the project as a Streamlit ML system.

### Purpose
Gives a broad user-facing overview, install steps, and run commands.

### Responsibility
High-level onboarding. It currently overstates some implementation details and has a stale Python version claim.

### Risks & Code Smells
- The README mentions `main.py`, but no `main.py` exists in the workspace.
- It says the system is production-grade, but the repository lacks tests, CI/CD, and deployment artifacts.

## pyproject.toml
**Path**: [pyproject.toml](../pyproject.toml)
**Type**: Config
**Criticality**: High
**Last Known Change Indicator**: Declares the runtime dependency set.

### Purpose
Defines project metadata and the currently declared Python dependencies.

### Risks & Code Smells
- `fastapi`, `flask`, and `uvicorn` are declared but not used by the current source tree.
- `mailbox` is declared even though it is part of the Python standard library.

## requirements.txt
**Path**: [requirements.txt](../requirements.txt)
**Type**: Config
**Criticality**: Medium
**Last Known Change Indicator**: Minimal pip dependency list.

### Purpose
Provides a simpler installation list than `pyproject.toml`.

### Risks & Code Smells
- It is incomplete relative to `pyproject.toml`.
- It may not reproduce the exact environment used for training or inference.

## Notebook Experiments/Spam Email Detection.ipynb
**Path**: [Notebook Experiments/Spam Email Detection.ipynb](../Notebook%20Experiments/Spam%20Email%20Detection.ipynb)
**Type**: Notebook
**Criticality**: Supporting / Legacy
**Last Known Change Indicator**: Contains exploratory ML work and generated outputs.

### Purpose
Preserves exploratory steps, charts, and experiment history.

### Responsibility
Not production logic. It is a learning and experiment surface.

### Risks & Code Smells
- Notebook state is harder to reproduce than the scripted pipeline.
- It should be treated as auxiliary documentation, not a deployment source.
