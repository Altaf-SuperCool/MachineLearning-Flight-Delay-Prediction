from typing import Optional
import torch
from torch import nn

from .config import MODEL_PATH
from .utils import logger


class MLPModel(nn.Module):
    def __init__(self, input_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Dropout(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


_model: Optional[MLPModel] = None
_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_model(input_dim: int) -> MLPModel:
    global _model
    if _model is None:
        logger.info(f"Loading model from {MODEL_PATH} on device {_DEVICE}...")
        model = MLPModel(input_dim=input_dim)
        state_dict = torch.load(MODEL_PATH, map_location=_DEVICE)
        model.load_state_dict(state_dict)
        model.to(_DEVICE)
        model.eval()
        _model = model
        logger.info("Model loaded successfully.")
    return _model


def get_device():
    return _DEVICE
