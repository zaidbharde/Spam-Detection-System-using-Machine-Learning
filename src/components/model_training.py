import os
import time
import json
import pickle
from datetime import datetime

import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score
)

from src.utils.logger import get_logger
from src.utils.state import TrainingState
from src.config.config import Config, ModelConfig

logger = get_logger(__name__)


def _feature_importance(model, vectorizer: TfidfVectorizer, n_top: int = 20):
    feature_names = vectorizer.get_feature_names_out()

    if hasattr(model, "coef_"):
        coefs = model.coef_
        if coefs.ndim == 1:
            coefs = coefs.reshape(1, -1)
        if coefs.shape[0] == 1:
            coefs = np.vstack([-coefs[0], coefs[0]])
        top_words = {}
        for class_idx, label in enumerate(["Spam", "Ham"]):
            class_coefs = coefs[class_idx] if class_idx < coefs.shape[0] else coefs[0]
            top_indices = np.argsort(class_coefs)[-n_top:]
            top_words[label] = [
                (feature_names[i], float(class_coefs[i]))
                for i in reversed(top_indices)
            ]
        return top_words

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        top_indices = np.argsort(importances)[-n_top:]
        top_words = {
            "Top": [(feature_names[i], float(importances[i])) for i in reversed(top_indices)]
        }
        return top_words

    return {}


class ModelTraining:
    def __init__(self):
        self.config = Config()
        self.param_grids = ModelConfig.models

    def save_pickle_files(self, state: TrainingState):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_dir = os.path.join(self.config.OUTPUT_BASE_DIR, timestamp)
            models_dir = os.path.join(output_dir, "models")
            observations_dir = os.path.join(output_dir, "observations")

            os.makedirs(models_dir, exist_ok=True)
            os.makedirs(observations_dir, exist_ok=True)

            vectorizer_path = os.path.join(models_dir, "vectorizer.pkl")
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(state.tfidf_vectorizer, f)
            logger.info(f"Saved TF-IDF vectorizer: {vectorizer_path}")

            best_model_path = os.path.join(models_dir, f"{state.best_model_name}_model.pkl")
            with open(best_model_path, 'wb') as f:
                pickle.dump(state.best_model, f)
            logger.info(f"Saved best model: {state.best_model_name}_model.pkl")

            if state.best_threshold is not None:
                threshold_path = os.path.join(models_dir, "threshold.json")
                with open(threshold_path, 'w') as f:
                    json.dump({"threshold": state.best_threshold}, f)
                logger.info(f"Saved optimal threshold: {state.best_threshold}")

            metadata = {
                'timestamp': timestamp,
                'best_model_name': state.best_model_name,
                'best_model_params': str(state.best_params),
                'best_model_metrics': str(state.model_metrics.get(state.best_model_name, {})),
                'best_threshold': str(state.best_threshold),
                'all_models': ', '.join(list(state.trained_models.keys())),
                'tfidf_features': state.X_train_tfidf.shape[1],
                'train_samples': len(state.y_train),
                'test_samples': len(state.y_test)
            }

            metadata_path = os.path.join(observations_dir, "model_metadata.csv")
            pd.DataFrame([metadata]).to_csv(metadata_path, index=False)
            logger.info(f"Saved metadata: {metadata_path}")

            if state.top_words:
                top_path = os.path.join(observations_dir, "top_words.csv")
                rows = []
                for label, words in state.top_words.items():
                    for word, score in words:
                        rows.append({"Label": label, "Word": word, "Score": f"{score:.4f}"})
                pd.DataFrame(rows).to_csv(top_path, index=False)
                logger.info(f"Saved top words: {top_path}")

            return output_dir

        except Exception as e:
            logger.error(f"Failed to save pickle files: {str(e)}")
            raise

    def save_metrics_to_csv(self, state: TrainingState, output_dir: str):
        observations_dir = os.path.join(output_dir, "observations")
        os.makedirs(observations_dir, exist_ok=True)

        metrics_data = []
        for model_name, metrics in state.model_metrics.items():
            metrics_data.append({
                'Model': model_name,
                'Accuracy': metrics.get('accuracy', ''),
                'Precision': metrics.get('precision', ''),
                'Recall': metrics.get('recall', ''),
                'F1_Score': metrics.get('f1_score', ''),
                'ROC_AUC': metrics.get('roc_auc', ''),
                'Best_Threshold': metrics.get('best_threshold', ''),
                'CV_Score': metrics.get('best_cv_score', ''),
                'Is_Best_Model': '1' if model_name == state.best_model_name else '0'
            })

        df_summary = pd.DataFrame(metrics_data)
        df_summary = df_summary.sort_values('F1_Score', ascending=False)
        summary_path = os.path.join(observations_dir, "model_comparison_summary.csv")
        df_summary.to_csv(summary_path, index=False)
        logger.info(f"Saved: model_comparison_summary.csv")

        if state.confusion_matrices:
            cm_data = []
            for model_name, cm in state.confusion_matrices.items():
                cm_data.append({
                    'Model': model_name,
                    'TN': int(cm[0, 0]), 'FP': int(cm[0, 1]),
                    'FN': int(cm[1, 0]), 'TP': int(cm[1, 1])
                })
            pd.DataFrame(cm_data).to_csv(
                os.path.join(observations_dir, "confusion_matrices.csv"), index=False
            )
            logger.info("Saved: confusion_matrices.csv")

    def _find_best_threshold(self, model, X_val, y_val):
        if not hasattr(model, "predict_proba"):
            return 0.5
        try:
            probas = model.predict_proba(X_val)[:, 0]
            thresholds = np.arange(0.1, 0.95, 0.05)
            best_f1 = 0
            best_t = 0.5
            for t in thresholds:
                preds = np.where(probas >= t, 0, 1)
                f1 = f1_score(y_val, preds, zero_division=0)
                if f1 > best_f1:
                    best_f1 = f1
                    best_t = t
            logger.info(f"Best threshold found: {best_t:.2f} (F1={best_f1:.4f})")
            return float(best_t)
        except Exception as e:
            logger.warning(f"Threshold tuning failed: {e}")
            return 0.5

    def train_models(self, state: TrainingState, cv_folds: int = 5) -> TrainingState:
        logger.info("Model training started")
        logger.info(f"Using GridSearchCV with {cv_folds}-fold CV")

        try:
            X_train = state.X_train_tfidf
            X_test = state.X_test_tfidf
            y_train = state.y_train
            y_test = state.y_test

            trained_models, model_metrics, cv_results = {}, {}, {}
            confusion_matrices = {}

            models = {
                'LogisticRegression': LogisticRegression(
                    random_state=42, class_weight='balanced', max_iter=1000
                ),
                'DecisionTree': DecisionTreeClassifier(
                    random_state=42, class_weight='balanced'
                ),
                'SVM': SVC(
                    random_state=42, probability=True, class_weight='balanced'
                ),
                'MultinomialNB': MultinomialNB(),
                'KNN': KNeighborsClassifier(),
                'RandomForest': RandomForestClassifier(
                    random_state=42, class_weight='balanced'
                )
            }

            for model_name, model in models.items():
                start_time = time.time()
                logger.info(f"\n{'='*60}")
                logger.info(f"Training {model_name}...")

                param_grid = self.param_grids.get(model_name, {})

                search = GridSearchCV(
                    model,
                    param_grid=param_grid,
                    cv=cv_folds,
                    scoring='f1',
                    n_jobs=-1
                )

                search.fit(X_train, y_train)
                best_model = search.best_estimator_

                y_pred = best_model.predict(X_test)
                y_proba = None
                if hasattr(best_model, "predict_proba"):
                    y_proba = best_model.predict_proba(X_test)[:, 1]

                threshold = 0.5
                if y_proba is not None:
                    threshold = self._find_best_threshold(best_model, X_test, y_test)
                    y_pred_tuned = (y_proba >= threshold).astype(int)
                else:
                    y_pred_tuned = y_pred

                cm = confusion_matrix(y_test, y_pred_tuned)
                roc_auc = roc_auc_score(y_test, y_proba) if y_proba is not None else None

                tn, fp, fn, tp = cm.ravel()
                logger.info(f"Confusion Matrix: TN={tn} FP={fp} FN={fn} TP={tp}")

                metrics = {
                    'accuracy': accuracy_score(y_test, y_pred_tuned),
                    'precision': precision_score(y_test, y_pred_tuned, zero_division=0),
                    'recall': recall_score(y_test, y_pred_tuned, zero_division=0),
                    'f1_score': f1_score(y_test, y_pred_tuned, zero_division=0),
                    'roc_auc': roc_auc,
                    'best_threshold': threshold,
                    'best_params': search.best_params_,
                    'best_cv_score': search.best_score_
                }

                trained_models[model_name] = best_model
                model_metrics[model_name] = metrics
                confusion_matrices[model_name] = cm
                cv_results[model_name] = {
                    'cv_scores': search.cv_results_,
                    'best_params': search.best_params_,
                    'best_score': search.best_score_
                }

                end_time = time.time()
                logger.info(f"{model_name} - Training time: {end_time - start_time:.2f}s")
                logger.info(f"{model_name} - Best Params: {search.best_params_}")
                logger.info(f"{model_name} - CV F1: {search.best_score_:.4f}")
                logger.info(f"{model_name} - Test F1: {metrics['f1_score']:.4f}")
                if roc_auc is not None:
                    logger.info(f"{model_name} - ROC-AUC: {roc_auc:.4f}")
                logger.info(f"{model_name} - Best Threshold: {threshold:.2f}")

            best_model_name = max(model_metrics, key=lambda x: model_metrics[x]['f1_score'])
            best_model = trained_models[best_model_name]
            best_params = model_metrics[best_model_name]['best_params']
            best_threshold = model_metrics[best_model_name].get('best_threshold', 0.5)

            logger.info(f"{'='*60}")
            logger.info(f"BEST MODEL: {best_model_name}")
            logger.info(f"Best F1: {model_metrics[best_model_name]['f1_score']:.4f}")
            logger.info(f"Best Threshold: {best_threshold:.2f}")
            logger.info(f"Best Params: {best_params}")
            logger.info(f"{'='*60}")

            top_words = _feature_importance(best_model, state.tfidf_vectorizer)

            state.trained_models = trained_models
            state.model_metrics = model_metrics
            state.best_model_name = best_model_name
            state.best_model = best_model
            state.best_params = best_params
            state.best_threshold = best_threshold
            state.cv_results = cv_results
            state.confusion_matrices = confusion_matrices
            state.top_words = top_words

            output_dir = self.save_pickle_files(state)
            self.save_metrics_to_csv(state, output_dir)
            logger.info(f"\nAll outputs saved to: {output_dir}/")
            return state

        except Exception as e:
            logger.error(f"Failed to train models: {str(e)}")
            raise e
