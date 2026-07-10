from src.utils.logger import get_logger
from src.config.config import Config
from src.utils.state import TrainingState
from src.utils.preprocessor import preprocess_text
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

logger = get_logger(__name__)

class DataTransformation:
    def __init__(self):
        self.config = Config()

    def transform_data(self, state: TrainingState) -> TrainingState:
        logger.info("Data transformation started")
        try:
            data = state.training_data.copy()

            data['Category'] = data['Category'].astype(str).str.lower().str.strip()
            data.loc[data['Category'] == 'spam', 'Category'] = '0'
            data.loc[data['Category'] == 'ham', 'Category'] = '1'
            data['Category'] = data['Category'].astype(int)

            logger.info(f"Label encoding completed. Data shape: {data.shape}")

            logger.info("Applying text preprocessing...")
            data['Message'] = data['Message'].apply(preprocess_text)

            X = data['Message']
            y = data['Category'].values

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42, stratify=y
            )

            logger.info(f"Train/test split completed. Train size: {len(X_train)}, Test size: {len(X_test)}")

            tfidf_vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words='english',
                max_features=5000,
                ngram_range=(1, 2),
                sublinear_tf=True
            )
            X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
            X_test_tfidf = tfidf_vectorizer.transform(X_test)

            logger.info(f"TF-IDF transformation completed. Feature shape: {X_train_tfidf.shape}")

            state.transformed_data = data
            state.X_train = X_train
            state.X_test = X_test
            state.y_train = y_train
            state.y_test = y_test
            state.X_train_tfidf = X_train_tfidf
            state.X_test_tfidf = X_test_tfidf
            state.tfidf_vectorizer = tfidf_vectorizer

            logger.info("Data transformation completed")
            return state
        except Exception as e:
            logger.error(f"Failed to transform data: {str(e)}")
            raise e
