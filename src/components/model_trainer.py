import os
import sys
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from src.exception import CustomException
from src.logger import get_logger
from src.utils import save_object

logging = get_logger(__name__)

@dataclass
class ModelTrainerConfig:
    model_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def train_model(self, X_train, X_test, y_train, y_test, transformer):
        try:
            logging.info("Starting model training process...")

            # Define individual models with pipelines
            logistic_pipeline = Pipeline([
                ('scaler', StandardScaler()),
                ('lr', LogisticRegression(solver='liblinear', max_iter=1000, random_state=42))
            ])

            rf_pipeline = Pipeline([
                ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
            ])

            # Ensemble voting classifier
            voting_model = VotingClassifier(
                estimators=[
                    ('lr', logistic_pipeline),
                    ('rf', rf_pipeline)
                ],
                voting='soft'
            )
            logging.info("Voting classifier created.")
            # Final pipeline with preprocessor
            pipe = Pipeline([
                ('transform', transformer),
                ('voting_model', voting_model)
            ])

            # Grid search parameters
            param_grid = {
                'voting_model__lr__lr__C': [0.1, 1.0, 10],
                'voting_model__rf__rf__n_estimators': [50, 100],
                'voting_model__rf__rf__max_depth': [None, 10, 20]
            }
            logging.info("Starting grid search for hyperparameter tuning...")
            grid = GridSearchCV(pipe, param_grid, cv=3, verbose=1, n_jobs=-1)
            grid.fit(X_train, y_train)
            logging.info("Grid search completed.")
            # Best model
            best_model = grid.best_estimator_

            # Evaluate
            y_pred = best_model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            logging.info(f"Model accuracy on test set: {acc:.4f}")

            # Save model
            save_object(
                file_path=self.model_trainer_config.model_path,
                obj=best_model
            )
            logging.info(f"Trained model saved at {self.model_trainer_config.model_path}")

            return acc

        except Exception as e:
            logging.error("Exception occurred during model training.")
            raise CustomException(e, sys)
