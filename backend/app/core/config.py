"""
Application settings, loaded from environment variables / a .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Path to the exported scikit-learn pipeline (relative to the backend/ folder,
    # or an absolute path). Must match the file produced by the notebook
    # (joblib.dump(model_rf, "house_price.pkl")).
    MODEL_PATH: str = "models/house_price.pkl"

    # Origins allowed to call this API (Vite dev server runs on 5173 by default).
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    APP_NAME: str = "House Price Prediction API"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
