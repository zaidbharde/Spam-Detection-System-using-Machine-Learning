# FAQ

## Is this a database-backed app?
No. The project is file-backed and reads from CSV, MBOX, and pickle files.

## Is there an API server?
No API endpoints were found. Streamlit calls the pipeline directly.

## What model is currently used?
The latest saved artifact set shows SVM as the best model.

## Can I retrain it?
Yes. Run the training pipeline after placing the dataset at the configured CSV path.

## Why does inference fail sometimes?
Usually because the configured model artifact path is missing or stale.

## Is the notebook required?
No. It is exploratory documentation and experimentation history.
