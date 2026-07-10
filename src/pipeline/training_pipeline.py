from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTraining
from src.utils.state import TrainingState
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TrainingPipeline:
    def __init__(self):
        self.state = TrainingState()

    def run_pipeline(self, cv_folds: int = 5):
        try:
            logger.info("Initiating training pipeline")
            ingestion = DataIngestion()
            self.state = ingestion.load_data(self.state)
            logger.info(f"Data loaded: {self.state.training_data.shape}")
            logger.info(f"Columns: {self.state.training_data.columns.tolist()}")
            logger.info(f"Samples: {len(self.state.training_data)}")

            transformation = DataTransformation()
            self.state = transformation.transform_data(self.state)
            logger.info(f"Train: {len(self.state.X_train)}, Test: {len(self.state.X_test)}")
            logger.info(f"TF-IDF features: {self.state.X_train_tfidf.shape[1]}")

            trainer = ModelTraining()
            self.state = trainer.train_models(self.state, cv_folds=cv_folds)

            logger.info(f"\n{'='*70}")
            logger.info("Training pipeline completed successfully")
            logger.info(f"Best model: {self.state.best_model_name}")
            logger.info(f"Best F1: {self.state.model_metrics[self.state.best_model_name]['f1_score']:.4f}")
            best_metrics = self.state.model_metrics[self.state.best_model_name]
            logger.info(f"Threshold: {best_metrics.get('best_threshold', 'N/A')}")
            if best_metrics.get('roc_auc') is not None:
                logger.info(f"ROC-AUC: {best_metrics['roc_auc']:.4f}")

            return self.state

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise e

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline(cv_folds=5)
