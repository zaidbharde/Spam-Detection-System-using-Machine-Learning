# Recommended Structure

## Current Structure Assessment
```text
Spam-Email-Detection-main/
├── app.py
├── data/
│   └── dataset/
│       └── dataset.csv
├── outputs/ ⚠️ generated artifacts mixed into project root
├── logs/ ⚠️ runtime output in repo tree
├── Notebook Experiments/ ⚠️ legacy exploratory notebook folder
├── src/
│   ├── components/
│   ├── config/
│   ├── pipeline/
│   └── utils/
└── pyproject.toml
```

## Problems Identified
| Issue | Location | Impact | Effort to Fix |
|-------|----------|--------|---------------|
| Hardcoded artifact path | [src/config/config.py](../src/config/config.py) | inference can break when a new training run is produced | Low |
| No tests | repository level | regressions are easy to introduce | Medium |
| Unused dependencies | [pyproject.toml](../pyproject.toml) | packaging noise and larger install surface | Low |
| Generated outputs in repo tree | [outputs/](../outputs/) | source and artifacts are coupled | Low |
| Notebook-only experiment history | [Notebook Experiments/](../Notebook%20Experiments/) | knowledge is less reproducible | Low |

## Recommended Structure
```text
project/
├── src/
│   ├── app/
│   ├── ml/
│   ├── io/
│   └── utils/
├── tests/
├── notebooks/
├── data/
├── models/
├── logs/
├── docs/
└── pyproject.toml
```

## Migration Plan
| Step | Action | Risk | Rollback |
|------|--------|------|----------|
| 1 | Add stable artifact alias | Low | Point alias back to current run |
| 2 | Introduce tests for pipeline pieces | Low | Delete test files |
| 3 | Move notebook experiments under a clearer notebooks folder | Low | Move it back |
| 4 | Prune unused dependencies | Medium | Re-add removed packages |

## What Not to Change
- Keep the core `src/components`, `src/pipeline`, and `src/utils` split unless there is a larger refactor plan.
- Keep `outputs/` if the project still relies on file-based inference.
- Keep the Streamlit entry point simple unless the app gains a true backend layer.
