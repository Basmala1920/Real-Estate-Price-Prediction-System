import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.prediction import router as prediction_router
from app.core.config import settings
from app.services.inference import predictor
from app.utils.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model once at startup, not on every request.
    try:
        predictor.load(settings.MODEL_PATH)
    except FileNotFoundError as exc:
        # Don't crash the whole server -- /health will report the problem
        # clearly instead of the app failing to boot with a stack trace.
        logger.error(str(exc))
    yield
    logger.info("Shutting down.")


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)
