from fastapi import APIRouter

from .config import MODEL_VERSION, PREPROCESS_VERSION
from .preprocess import get_input_dim
from .model_loader import get_model

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/ready")
def ready():
    # Try to load model + artifacts
    input_dim = get_input_dim()
    _ = get_model(input_dim=input_dim)
    return {"status": "ready"}


@router.get("/version")
def version():
    return {
        "model_version": MODEL_VERSION,
        "preprocess_version": PREPROCESS_VERSION,
    }
