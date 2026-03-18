from io import StringIO
from typing import List, Dict

import pandas as pd

from .schemas import FlightRequest
from .predict import predict_single_flight
from .utils import log_request


@log_request
def batch_predict_json(flights: List[FlightRequest]) -> List[Dict]:
    results = []
    for flight in flights:
        result = predict_single_flight(flight.dict())
        results.append(result)
    return results


@log_request
def batch_predict_csv_string(csv_data: str) -> List[Dict]:
    df = pd.read_csv(StringIO(csv_data))
    return _batch_predict_from_dataframe(df)


@log_request
def batch_predict_csv_file(file_bytes: bytes) -> List[Dict]:
    df = pd.read_csv(StringIO(file_bytes.decode("utf-8")))
    return _batch_predict_from_dataframe(df)


def _batch_predict_from_dataframe(df: pd.DataFrame) -> List[Dict]:
    required_cols = [
        "OP_CARRIER",
        "ORIGIN",
        "DEST",
        "CRS_DEP_TIME",
        "CRS_ARR_TIME",
        "DISTANCE",
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")

    results = []
    for _, row in df.iterrows():
        flight = {
            "OP_CARRIER": row["OP_CARRIER"],
            "ORIGIN": row["ORIGIN"],
            "DEST": row["DEST"],
            "CRS_DEP_TIME": row["CRS_DEP_TIME"],
            "CRS_ARR_TIME": row["CRS_ARR_TIME"],
            "DISTANCE": row["DISTANCE"],
        }
        result = predict_single_flight(flight)
        results.append(result)
    return results
