"""
Turns a PredictionRequest into the exact one-row pandas.DataFrame shape the
trained pipeline expects.

Column names below MUST match the training columns from the notebook
(FinalPrj.ipynb), where:

    numeric_features = ["area_sqft", "floor_num", "bathroom_num",
                         "balcony_num", "car_parking_num"]
    categorical_features = ["location", "Status", "Transaction",
                             "Furnishing", "facing", "overlooking",
                             "Ownership", "society_grouped"]

The frontend form (src/components/PredictionForm.tsx) only collects a
subset of these: location, carpet_area_sqft, floor_num, bathroom, balcony,
furnishing, transaction, ownership, facing. Four training columns are never
sent by the client: Status, overlooking, society_grouped, car_parking_num.

Rather than guessing hardcoded defaults for those four, we leave them as
None/NaN. The exported pipeline already embeds a SimpleImputer
(median for numeric, most_frequent for categorical) fitted on the training
data, so missing values are filled in exactly the way the model was trained
to expect -- this is more faithful than inventing our own default values.

Unknown/unseen `location` values are handled by the pipeline's
OneHotEncoder(handle_unknown="ignore"), so no special-casing is needed here.
"""
import pandas as pd

from app.schemas.prediction import PredictionRequest

NUMERIC_FEATURES = ["area_sqft", "floor_num", "bathroom_num", "balcony_num", "car_parking_num"]
CATEGORICAL_FEATURES = [
    "location",
    "Status",
    "Transaction",
    "Furnishing",
    "facing",
    "overlooking",
    "Ownership",
    "society_grouped",
]
MODEL_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def request_to_dataframe(request: PredictionRequest) -> pd.DataFrame:
    """Build the one-row DataFrame the trained pipeline expects."""
    row = {
        "area_sqft": request.carpet_area_sqft,
        "floor_num": request.floor_num,
        "bathroom_num": request.bathroom,
        "balcony_num": request.balcony,
        "car_parking_num": None,  # not collected by the frontend -> imputed
        "location": request.location.strip().lower(),
        "Status": None,  # not collected by the frontend -> imputed
        "Transaction": request.transaction,
        "Furnishing": request.furnishing,
        "facing": request.facing,
        "overlooking": None,  # not collected by the frontend -> imputed
        "Ownership": request.ownership,
        "society_grouped": None,  # not collected by the frontend -> imputed
    }
    return pd.DataFrame([row], columns=MODEL_COLUMNS)
