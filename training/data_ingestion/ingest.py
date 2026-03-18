import os
import json
import pandas as pd
import boto3
from pathlib import Path

from training.data_validation.validate import validate_schema

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

CSV_PATH = RAW_DIR / "airline_delays.csv"
PROCESSED_PATH = PROCESSED_DIR / "processed_data.csv"

SCHEMA_PATH = Path("training/config/schema.json")

# Your S3 bucket + key
S3_BUCKET = "airline-delay-raw-data"
S3_KEY = "airline_delays.csv"


def ensure_directories():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def download_from_s3_if_missing():
    if CSV_PATH.exists():
        print("Local CSV exists. Skipping S3 download.")
        return

    print(f"Downloading from s3://{S3_BUCKET}/{S3_KEY} ...")

    s3 = boto3.client("s3")
    s3.download_file(S3_BUCKET, S3_KEY, str(CSV_PATH))

    print(f"Downloaded CSV to {CSV_PATH}")


def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


def transform_to_schema(df, schema):
    print("Transforming dataset to match schema...")

    column_map = {
        "AIRLINE": "OP_CARRIER",
        "ORIGIN_AIRPORT": "ORIGIN",
        "DESTINATION_AIRPORT": "DEST",
        "SCHEDULED_DEPARTURE": "CRS_DEP_TIME",
        "SCHEDULED_ARRIVAL": "CRS_ARR_TIME",
        "DISTANCE": "DISTANCE",
        "DEPARTURE_DELAY": "DEP_DELAY",
        "ARRIVAL_DELAY": "ARR_DELAY",
    }

    df["FL_DATE"] = (
        df["YEAR"].astype(str)
        + "-"
        + df["MONTH"].astype(str).str.zfill(2)
        + "-"
        + df["DAY"].astype(str).str.zfill(2)
    )

    df = df.rename(columns=column_map)

    required_cols = list(schema["columns"].keys())
    df = df[required_cols]

    for col, dtype in schema["columns"].items():
        if dtype == "string":
            df[col] = df[col].astype(str)
        elif dtype == "integer":
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        elif dtype == "float":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def save_processed(df):
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Processed dataset saved to {PROCESSED_PATH}")


def run_ingestion():
    ensure_directories()

    # NEW: Pull from S3 if local file missing
    download_from_s3_if_missing()

    print("Loading raw CSV...")
    df = pd.read_csv(CSV_PATH)

    schema = load_schema()

    df = transform_to_schema(df, schema)

    print("Validating schema...")
    validate_schema(df, schema)

    save_processed(df)

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    run_ingestion()
