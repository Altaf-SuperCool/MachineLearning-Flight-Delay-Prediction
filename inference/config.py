from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = BASE_DIR / "artifacts"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

MODEL_PATH = ARTIFACT_DIR / "model.pt"
ENCODER_PATH = ARTIFACT_DIR / "encoder_mapping.pkl"
SCALER_PATH = ARTIFACT_DIR / "scaler.pkl"

# Model / preprocessing versions
MODEL_VERSION = "1.0.0"
PREPROCESS_VERSION = "1.0.0"

# API metadata
API_TITLE = "Airline Delay Prediction API"
API_DESCRIPTION = "Enterprise-grade inference API for flight delay prediction."
API_VERSION = "1.0.0"

# Feature configuration
CATEGORICAL_COLS = ["OP_CARRIER", "ORIGIN", "DEST"]
NUMERIC_COLS = ["CRS_DEP_TIME", "CRS_ARR_TIME", "DISTANCE"]
