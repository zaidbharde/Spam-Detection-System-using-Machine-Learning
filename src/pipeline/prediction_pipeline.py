import mailbox
import pickle
import json
import time
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from src.utils.state import PredictionState
from src.utils.logger import get_logger
from src.config.config import Config
from src.utils.email_utils import extract_body, all_recipients, clean_text
from src.utils.preprocessor import preprocess_text

logger = get_logger(__name__)

class PredictionPipeline:
    def __init__(self, load_models: bool = True):
        self.config = Config()
        self.mailbox = None
        self.feature_transformer = None
        self.model = None
        self.threshold = 0.5

        if load_models:
            self._load_models()

    def _load_models(self) -> None:
        logger.info("Loading models...")
        feature_path = Path(self.config.feature_path)
        model_path = Path(self.config.model_path)
        missing_paths = [
            str(path) for path in (feature_path, model_path) if not path.exists()
        ]
        if missing_paths:
            raise FileNotFoundError(
                "Required model artifact(s) not found: "
                + ", ".join(missing_paths)
                + ". Run `python -m src.pipeline.training_pipeline` or update "
                + "`src/config/config.py` with valid artifact paths."
            )

        with feature_path.open("rb") as feature_file:
            self.feature_transformer = pickle.load(feature_file)
        with model_path.open("rb") as model_file:
            self.model = pickle.load(model_file)

        threshold_path = model_path.parent / "threshold.json"
        if threshold_path.exists():
            with open(threshold_path) as f:
                self.threshold = json.load(f).get("threshold", 0.5)
        logger.info(f"Models loaded. Threshold: {self.threshold}")

    @staticmethod
    def _prediction_to_label(prediction) -> str:
        normalized = str(prediction).strip().lower()
        if normalized in {"0", "spam"}:
            return "Spam"
        if normalized in {"1", "ham"}:
            return "Ham"
        raise ValueError(f"Unsupported prediction label: {prediction!r}")

    def _get_probabilities(self, features) -> Tuple[float, float]:
        if not hasattr(self.model, "predict_proba"):
            return None, None
        try:
            probs = self.model.predict_proba(features)[0]
            classes = self.model.classes_
            prob_spam = float(probs[list(classes).index(0)]) if 0 in classes else float(probs[0])
            prob_ham = float(probs[list(classes).index(1)]) if 1 in classes else float(probs[1])
            return prob_spam, prob_ham
        except Exception:
            return None, None

    def _top_features(self, features) -> List[Tuple[str, float]]:
        try:
            feature_names = self.feature_transformer.get_feature_names_out()
            feature_array = features.toarray()[0]

            if hasattr(self.model, "coef_"):
                coefs = self.model.coef_
                if coefs.ndim == 1:
                    coefs = coefs.reshape(1, -1)
                spam_coefs = -coefs[0] if coefs.shape[0] == 1 else coefs[0]
                scores = feature_array * spam_coefs
            elif hasattr(self.model, "feature_importances_"):
                scores = feature_array * self.model.feature_importances_
            else:
                return []

            nonzero = np.where(feature_array > 0)[0]
            if len(nonzero) == 0:
                return []

            word_scores = [(feature_names[i], float(scores[i])) for i in nonzero]
            word_scores.sort(key=lambda x: abs(x[1]), reverse=True)
            return word_scores[:10]
        except Exception:
            return []

    def predict_single_email(self, email_body: str) -> Dict:
        if self.model is None or self.feature_transformer is None:
            self._load_models()

        processed = preprocess_text(email_body)
        features = self.feature_transformer.transform([processed])

        if hasattr(self.model, "predict_proba"):
            prob_spam, prob_ham = self._get_probabilities(features)
            if prob_spam is not None:
                spam_prob_pct = prob_spam * 100
                ham_prob_pct = prob_ham * 100
                if prob_spam >= self.threshold:
                    prediction_label = "Spam"
                    confidence = spam_prob_pct
                else:
                    prediction_label = "Ham"
                    confidence = ham_prob_pct
                confidence_source = "probability"
                raw_prediction = 0 if prediction_label == "Spam" else 1
            else:
                raw_prediction = self.model.predict(features)[0]
                prediction_label = self._prediction_to_label(raw_prediction)
                confidence = None
                confidence_source = None
        else:
            raw_prediction = self.model.predict(features)[0]
            prediction_label = self._prediction_to_label(raw_prediction)
            prob_spam = prob_ham = None
            confidence = None
            confidence_source = None

        top_words = self._top_features(features)

        return {
            'prediction': prediction_label,
            'confidence': confidence,
            'confidence_source': confidence_source,
            'raw_prediction': int(raw_prediction),
            'prob_spam_pct': round(prob_spam * 100, 2) if prob_spam is not None else None,
            'prob_ham_pct': round(prob_ham * 100, 2) if prob_ham is not None else None,
            'top_words': top_words,
            'threshold': self.threshold
        }

    def load_mailbox(self, mailbox_path: str) -> None:
        logger.info(f"Loading mailbox from {mailbox_path}")
        self.mailbox = mailbox.mbox(mailbox_path)
        logger.info(f"Loaded mailbox from {mailbox_path}")

    def process_mailbox(self, mailbox_path: Optional[str] = None) -> List[Dict]:
        if mailbox_path:
            self.load_mailbox(mailbox_path)
        if self.mailbox is None:
            raise ValueError("No mailbox loaded. Call load_mailbox() first.")
        logger.info("Processing mailbox")
        data = []
        for message in self.mailbox:
            labels = (message.get("X-Gmail-Labels") or "").lower()
            category = (
                "Spam" if "spam" in labels else
                "Promotions" if "category_promotions" in labels else
                "Social" if "category_social" in labels else
                "Updates" if "category_updates" in labels else
                "Inbox"
            )
            time_str = message.get("Date", "")
            recipients = clean_text(all_recipients(message))
            subject = clean_text(message.get("Subject", ""))
            body = clean_text(extract_body(message))
            direction = "Sent" if "Sent" in (message.get("X-Gmail-Labels") or "") else "Received"
            data.append({
                "Time": time_str,
                "Recipients": recipients,
                "Subject": subject,
                "Body": body,
                "Category": category,
                "Direction": direction
            })
        logger.info(f"Processed {len(data)} emails from mailbox")
        self.mailbox.close()
        self.mailbox = None
        return data

    def run_prediction(self, mail_data: List[Dict]) -> List[Dict]:
        if self.model is None or self.feature_transformer is None:
            self._load_models()
        start_time = time.time()
        logger.info("Running predictions")
        for mail in mail_data:
            body_text = mail.get('Body', '')
            processed = preprocess_text(body_text)
            features = self.feature_transformer.transform([processed])
            if hasattr(self.model, "predict_proba"):
                prob_spam, prob_ham = self._get_probabilities(features)
                if prob_spam is not None:
                    if prob_spam >= self.threshold:
                        mail["Prediction"] = "Spam"
                        mail["Confidence"] = prob_spam * 100
                    else:
                        mail["Prediction"] = "Ham"
                        mail["Confidence"] = prob_ham * 100
                    mail["Confidence Source"] = "probability"
                    mail["Spam Prob"] = round(prob_spam * 100, 2)
                    mail["Ham Prob"] = round(prob_ham * 100, 2)
                else:
                    raw = self.model.predict(features)[0]
                    mail["Prediction"] = self._prediction_to_label(raw)
                    mail["Confidence"] = None
                    mail["Confidence Source"] = None
            else:
                raw = self.model.predict(features)[0]
                mail["Prediction"] = self._prediction_to_label(raw)
                mail["Confidence"] = None
                mail["Confidence Source"] = None
        end_time = time.time()
        logger.info(f"Prediction completed in {end_time - start_time:.2f} seconds")
        return mail_data

    def predict_mbox_file(self, mailbox_path: str, output_path: Optional[str] = None) -> pd.DataFrame:
        mail_data = self.process_mailbox(mailbox_path)
        mail_data = self.run_prediction(mail_data)
        df = pd.DataFrame(mail_data)
        if output_path:
            df.to_csv(output_path, index=False)
            logger.info(f"Predictions saved to {output_path}")
        return df


def run_legacy_pipeline(state: PredictionState) -> None:
    pipeline = PredictionPipeline(load_models=False)
    pipeline.load_mailbox(state.mailbox_path)
    mail_data = pipeline.process_mailbox()
    state.mail_data = mail_data
    state.mail_data = pipeline.run_prediction(state.mail_data)
    df = pd.DataFrame(state.mail_data)
    df.to_csv("data/predictions.csv", index=False)
