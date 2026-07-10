# Executive Summary

This repository is a compact machine learning application for spam detection. It is not a distributed system, database service, or multi-tier web platform; it is a local Python project that combines a Streamlit front-end with a scikit-learn training and inference pipeline.

The training workflow loads `data/dataset/dataset.csv`, converts email labels into numeric classes, builds TF-IDF features, and runs grid search across five classical models. The best model from the latest saved run is SVM with a linear kernel, `C=10`, and CV score around 0.989.

The inference workflow is simpler: the Streamlit app loads the saved TF-IDF vectorizer and model from `outputs/2025-12-25_14-02-05/models/`, classifies pasted text or MBOX messages, and shows a spam/ham label plus a confidence estimate when available.

Operationally, the project is lightweight. There is no database, no Docker file, no CI/CD configuration, and no dedicated API layer. That makes it easy to run locally, but it also means deployment, monitoring, and testing maturity are limited.
