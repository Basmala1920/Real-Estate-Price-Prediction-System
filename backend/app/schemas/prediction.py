"""
Request/response schemas.

IMPORTANT: PredictionRequest's field names intentionally match the frontend's
`PredictionFormData` interface (src/types/prediction.ts) exactly, field for
field. The frontend is not being modified, so the API contract has to meet
it where it is. The mapping from these field names to the model's actual
training column names (e.g. carpet_area_sqft -> area_sqft, bathroom ->
bathroom_num) happens in services/preprocessing.py, not here.
"""
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    location: str = Field(..., min_length=1)
    carpet_area_sqft: float = Field(..., gt=0, description="Must be > 0")
    floor_num: int
    bathroom: int = Field(..., ge=0)
    balcony: int = Field(..., ge=0)
    furnishing: str
    transaction: str
    ownership: str
    facing: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "location": "mumbai",
                "carpet_area_sqft": 1000,
                "floor_num": 3,
                "bathroom": 2,
                "balcony": 1,
                "furnishing": "Semi-Furnished",
                "transaction": "Resale",
                "ownership": "Freehold",
                "facing": "East",
            }
        }
    }


class PredictionResponse(BaseModel):
    predicted_price: float


class HealthResponse(BaseModel):
    status: str
