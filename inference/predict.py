from typing import Dict
import numpy as np
import torch

from .config import MODEL_VERSION, PREPROCESS_VERSION
from .model_loader import get_model, get_device
from .preprocess import preprocess_single, get_input_dim
from .utils import log_request

# Step 9 imports
from inference.monitoring.logger import logger
from inference.drift.input_drift import calculate_psi
from inference.drift.prediction_drift import kl_divergence


# ---------------------------------------------------------
# Temporary baseline distributions (Step 9 placeholders)
# Replace with real training stats in Step 9.2
# ---------------------------------------------------------
BASELINE_FEATURE_DIST = np.random.normal(0, 1, 5000)   # Example training feature dist
BASELINE_PRED_DIST = np.random.beta(2, 5, 5000)         # Example training prediction dist


@log_request
def predict_single_flight(flight: Dict) -> Dict:
    """
    flight: raw dict with feature values
    returns: dict with delay_probability, delayed, versions
    """

    # ---------------------------------------------------------
    # 1. Preprocess
    # ---------------------------------------------------------
    input_dim = get_input_dim()
    model = get_model(input_dim=input_dim)
    device = get_device()

    tensor = preprocess_single(flight).to(device)

    # ---------------------------------------------------------
    # 2. Model Inference
    # ---------------------------------------------------------
    with torch.inference_mode():
        prob = model(tensor)
        prob_value = float(prob.item())

    delayed = prob_value >= 0.5

    result = {
        "delay_probability": prob_value,
        "delayed": delayed,
        "model_version": MODEL_VERSION,
        "preprocess_version": PREPROCESS_VERSION,
    }

    # ---------------------------------------------------------
    # 3. Drift Detection (Step 9)
    # ---------------------------------------------------------
    try:
        # Extract one numerical feature for drift (example: distance)
        # You can replace this with any feature from your flight dict
        incoming_feature = np.array([flight.get("distance", 0)], dtype=float)

        # Input Drift (PSI)
        psi_score = calculate_psi(
            expected=BASELINE_FEATURE_DIST,
            actual=incoming_feature
        )

        # Prediction Drift (KL Divergence)
        current_pred_array = np.array([prob_value])
        drift_score = kl_divergence(
            p=current_pred_array,
            q=BASELINE_PRED_DIST
        )

        logger.info({
            "event": "drift",
            "input_psi": float(psi_score),
            "pred_kl": float(drift_score),
            "model_version": MODEL_VERSION
        })

    except Exception as ex:
        logger.error({
            "event": "drift_error",
            "error": str(ex)
        })

    # ---------------------------------------------------------
    # 4. Return Response
    # ---------------------------------------------------------
    return result
