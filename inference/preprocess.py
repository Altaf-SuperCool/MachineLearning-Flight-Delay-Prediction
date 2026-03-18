import numpy as np
import torch
import joblib

from pathlib import Path
from .config import (
    ENCODER_PATH,
    SCALER_PATH,
    CATEGORICAL_COLS,
    NUMERIC_COLS,
)
from .utils import logger

_encoder = None
_scaler = None


def _load_encoder_and_scaler():
    """
    Loads the encoder and scaler saved during training.
    These were saved using joblib, so we must load them using joblib.
    """
    global _encoder, _scaler

    if _encoder is None:
        logger.info(f"Loading encoder from {ENCODER_PATH} using joblib...")
        _encoder = joblib.load(ENCODER_PATH)
        logger.info(f"Encoder loaded: {type(_encoder)}")

    if _scaler is None:
        logger.info(f"Loading scaler from {SCALER_PATH} using joblib...")
        _scaler = joblib.load(SCALER_PATH)
        logger.info(f"Scaler loaded: {type(_scaler)}")


def preprocess_single(flight: dict) -> torch.Tensor:
    """
    Preprocess a single flight record for inference.
    Applies the SAME transformations used during training.
    """
    _load_encoder_and_scaler()

    # Extract categorical and numeric values
    cat_values = [str(flight[col]) for col in CATEGORICAL_COLS]
    num_values = [float(flight[col]) for col in NUMERIC_COLS]

    # Convert to arrays
    cat_array = np.array(cat_values, dtype=object).reshape(1, -1)
    num_array = np.array(num_values, dtype=float).reshape(1, -1)

    # Apply encoder + scaler
    cat_encoded = _encoder.transform(cat_array)
    num_scaled = _scaler.transform(num_array)

    # Combine features
    features = np.concatenate([cat_encoded, num_scaled], axis=1)

    # Convert to tensor
    tensor = torch.tensor(features, dtype=torch.float32)

    return tensor


def get_input_dim() -> int:
    """
    Returns the number of features after preprocessing.
    """
    _load_encoder_and_scaler()

    num_cat = len(CATEGORICAL_COLS)
    num_num = len(NUMERIC_COLS)

    return num_cat + num_num
