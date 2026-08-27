"""
Loads the exported scikit-learn Pipeline (house_price.pkl) and runs
predictions. The pipeline bundles preprocessing (imputation, scaling,
one-hot encoding) AND the RandomForestRegressor together, so calling
.predict() on the raw one-row DataFrame is enough -- no manual encoding
needed here.
"""
import logging
from pathlib import Path

import joblib
import pandas as pd

logger = logging.getLogger(__name__)


class ModelNotLoadedError(RuntimeError):
    """Raised when a prediction is requested before the model has loaded."""


class PricePredictor:
    def __init__(self) -> None:
        self._model = None

    def load(self, model_path: str) -> None:
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Model file not found at '{path}'. Copy house_price.pkl "
                f"(exported from the notebook via joblib.dump) into this path "
                f"before starting the server."
            )
        logger.info("Loading model from %s ...", path)
        self._model = joblib.load(path)
        logger.info("Model loaded successfully.")

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def predict(self, X: pd.DataFrame) -> float:
        if self._model is None:
            raise ModelNotLoadedError("Model has not been loaded yet.")
        prediction = self._model.predict(X)
        return float(prediction[0])


# Single shared instance, loaded once at app startup (see app/main.py lifespan).
predictor = PricePredictor()
