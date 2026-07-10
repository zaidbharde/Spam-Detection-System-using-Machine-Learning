# Pitch Scripts

## 30-Second Pitch (Technical)
This is a Python Streamlit application for binary spam classification. Training uses scikit-learn with TF-IDF features and grid search across five classical models, and the best saved artifact set currently uses an SVM classifier. Inference loads the persisted vectorizer and model to classify either a pasted email or an entire MBOX archive.

## 30-Second Pitch (Non-Technical / Business)
The project saves time by automatically sorting emails into spam or legitimate messages. It turns a manual review task into a quick browser-based tool that can handle one message or many at once.

## 2-Minute Pitch (Investor/Demo)
The product solves a practical productivity problem: email triage. It is lightweight, easy to run locally, and already includes a full training-to-inference loop. A user can paste a message, upload an archive, and get labeled results with confidence values. The strongest current model is an SVM trained on more than 5,500 labeled messages, with high test accuracy and weighted F1 near 0.979. The next growth step is to harden the deployment story with tests, stable artifact management, and cleaner configuration.

## 5-Minute Pitch (Technical Deep Dive)
The repository is organized into a training pipeline and an inference pipeline. Training loads a CSV dataset, normalizes the labels, splits the data, vectorizes the text with TF-IDF, and runs grid search on Logistic Regression, Decision Tree, SVM, KNN, and Random Forest. Each model is evaluated on a held-out set, and the best one is serialized with its vectorizer. The Streamlit front-end then loads those artifacts and supports both single-email classification and batch MBOX processing. The design is small but coherent, with the main tradeoff being that inference depends on timestamped artifact paths.

## 10-Minute Pitch (Complete Walkthrough)
Start with the problem: spam email wastes attention and can hide important messages. Then show the architecture: Streamlit UI at the top, prediction pipeline in the middle, artifacts and file-based persistence underneath. Explain the data flow from CSV ingestion to label encoding to TF-IDF to model search and selection. Show the performance table and point out the current best model. Finally, be honest about the limitations: no database, no API tier, no CI/CD, no tests, and hardcoded artifact paths. That honesty is important because it shows the system is useful now and also ready for the next engineering step.
