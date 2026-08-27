import logging

from fastapi import APIRouter, HTTPException

from app.schemas.prediction import HealthResponse, PredictionRequest, PredictionResponse
from app.services.inference import ModelNotLoadedError, predictor
from app.services.preprocessing import request_to_dataframe

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    if not predictor.is_loaded:
        # Server is up but the model failed to load -- still respond 200 with
        # a clear status so the caller/monitor can tell what's wrong, rather
        # than a bare connection error.
        return HealthResponse(status="model_not_loaded")
    return HealthResponse(status="ok")


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    try:
        X = request_to_dataframe(request)
        predicted_price = predictor.predict(X)
    except ModelNotLoadedError as exc:
        logger.error("Prediction requested before model was loaded: %s", exc)
        raise HTTPException(status_code=503, detail="Model is not ready yet.") from exc
    except Exception as exc:  # noqa: BLE001 - surface a clean 500 to the client
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed.") from exc

    return PredictionResponse(predicted_price=predicted_price)
