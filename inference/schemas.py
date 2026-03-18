from typing import List, Optional
from pydantic import BaseModel, Field


class FlightRequest(BaseModel):
    OP_CARRIER: str = Field(..., description="Operating carrier code")
    ORIGIN: str = Field(..., description="Origin airport code")
    DEST: str = Field(..., description="Destination airport code")
    CRS_DEP_TIME: float = Field(..., description="Scheduled departure time (HHMM)")
    CRS_ARR_TIME: float = Field(..., description="Scheduled arrival time (HHMM)")
    DISTANCE: float = Field(..., description="Flight distance in miles")


class FlightResponse(BaseModel):
    delay_probability: float
    delayed: bool
    model_version: str
    preprocess_version: str


class BatchFlightRequest(BaseModel):
    flights: List[FlightRequest]


class BatchFlightResponse(BaseModel):
    predictions: List[FlightResponse]


class CSVStringRequest(BaseModel):
    csv_data: str = Field(..., description="CSV content as string")
