from typing import Optional, List, Dict, Any, Tuple
import pandas as pd
import numpy as np

class TrainingState:
    training_data_path: Optional[str] = None
    training_data: Optional[pd.DataFrame] = None
    transformed_data: Optional[pd.DataFrame] = None
    X_train: Optional[pd.Series] = None
    X_test: Optional[pd.Series] = None
    y_train: Optional[np.ndarray] = None
    y_test: Optional[np.ndarray] = None
    X_train_tfidf: Optional[Any] = None
    X_test_tfidf: Optional[Any] = None
    tfidf_vectorizer: Optional[Any] = None
    trained_models: Optional[Dict[str, Any]] = None
    model_metrics: Optional[Dict[str, Dict]] = None
    best_model_name: Optional[str] = None
    best_model: Optional[Any] = None
    best_params: Optional[Dict[str, Any]] = None
    best_threshold: float = 0.5
    cv_results: Optional[Dict[str, Any]] = None
    confusion_matrices: Optional[Dict[str, np.ndarray]] = None
    top_words: Optional[Dict[str, List[Tuple[str, float]]]] = None

class PredictionState:
    mailbox_path: Optional[str] = None
    mail_data: Optional[List[Dict[str, str]]] = None
