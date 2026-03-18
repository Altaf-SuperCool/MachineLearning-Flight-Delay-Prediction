from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from .middleware import error_middleware
from .logger import logger
from .config import API_TITLE, API_DESCRIPTION, API_VERSION

from .schemas import (
    FlightRequest,
    FlightResponse,
    BatchFlightRequest,
    BatchFlightResponse,
    CSVStringRequest,
)

from .predict import predict_single_flight
from .batch import (
    batch_predict_json,
    batch_predict_csv_file,
    batch_predict_csv_string,
)

from .health import router as health_router

# Step 9 Monitoring Middleware
from inference.monitoring.middleware import MonitoringMiddleware


# ---------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Step 9 Monitoring Middleware (MUST come before logging)
# ---------------------------------------------------------
app.add_middleware(MonitoringMiddleware)


# ---------------------------------------------------------
# Step 8 Logging Middleware
# ---------------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(
        f"Completed request: {request.method} {request.url} → {response.status_code}"
    )
    return response


# ---------------------------------------------------------
# Global Error Middleware (Step 8)
# ---------------------------------------------------------
app.middleware("http")(error_middleware)


# ---------------------------------------------------------
# Health + Ready + Version Routes
# ---------------------------------------------------------
app.include_router(health_router)


# ---------------------------------------------------------
# Prometheus Metrics Endpoint (Step 9)
# ---------------------------------------------------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ---------------------------------------------------------
# Prediction Endpoints
# ---------------------------------------------------------
@app.post("/predict", response_model=FlightResponse)
def predict(flight: FlightRequest):
    result = predict_single_flight(flight.dict())
    return FlightResponse(**result)


@app.post("/batch_predict", response_model=BatchFlightResponse)
def batch_predict(request: BatchFlightRequest):
    results = batch_predict_json(request.flights)
    return BatchFlightResponse(
        predictions=[FlightResponse(**r) for r in results]
    )


# ---------------------------------------------------------
# CSV Batch Prediction
# ---------------------------------------------------------
@app.post("/batch_predict_csv", response_model=BatchFlightResponse)
async def batch_predict_csv(
    file: UploadFile = File(None),
    csv_string: CSVStringRequest | None = None,
):
    """
    Supports:
    - CSV file upload
    - Raw CSV string
    """
    if file is not None:
        content = await file.read()
        results = batch_predict_csv_file(content)

    elif csv_string is not None:
        results = batch_predict_csv_string(csv_string.csv_string)

    else:
        raise HTTPException(
            status_code=400,
            detail="Either file or csv_string must be provided.",
        )

    return BatchFlightResponse(
        predictions=[FlightResponse(**r) for r in results]
    )
