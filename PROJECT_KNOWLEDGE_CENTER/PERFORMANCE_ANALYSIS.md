# Performance Analysis

## Training Performance
- Training is CPU-bound because each candidate model is wrapped in `GridSearchCV`.
- `n_jobs=-1` uses all available cores, which helps on multicore systems.
- The search space is moderate, but it can still take a while because five models are trained.

## Inference Performance
- Single-email inference is lightweight after the model and vectorizer are loaded.
- `st.cache_resource` helps avoid reloading artifacts on every Streamlit interaction.
- Batch MBOX prediction scales linearly with message count.

## Observed Baseline
- Latest saved SVM model achieved about 0.979 accuracy and 0.979 weighted F1 on the held-out test set.
- The TF-IDF feature space contained 6,847 features in the latest run.

## Bottlenecks
- Grid search and repeated model fitting during training.
- Mailbox parsing and HTML cleaning for large batches.

## Optimization Ideas
- Reduce the parameter grid for fast iteration.
- Cache preprocessed training artifacts for notebook experiments.
- Add incremental or sampled evaluation for rapid prototyping.
