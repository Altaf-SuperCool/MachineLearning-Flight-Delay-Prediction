import pandas as pd
import torch
from pathlib import Path
from training.preprocessing.transformers import CombinedPreprocessor

ARTIFACT_DIR = Path("artifacts")
ARTIFACT_DIR.mkdir(exist_ok=True)

ENCODER_PATH = ARTIFACT_DIR / "encoder_mapping.pkl"
SCALER_PATH = ARTIFACT_DIR / "scaler.pkl"

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(exist_ok=True)

CATEGORICAL_COLS = ["OP_CARRIER", "ORIGIN", "DEST"]
NUMERIC_COLS = ["CRS_DEP_TIME", "CRS_ARR_TIME", "DISTANCE"]
TARGET_COL = "ARR_DELAY"

def run_preprocessing(train_df, test_df):
    preprocessor = CombinedPreprocessor(
        categorical_cols=CATEGORICAL_COLS,
        numeric_cols=NUMERIC_COLS
    )

    print("Fitting transformers on training data...")
    preprocessor.fit(train_df)

    print("Transforming training data...")
    X_train = preprocessor.transform(train_df)
    y_train = (train_df[TARGET_COL] > 0).astype(float).values

    print("Transforming test data...")
    X_test = preprocessor.transform(test_df)
    y_test = (test_df[TARGET_COL] > 0).astype(float).values

    print("Converting to PyTorch tensors...")
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    print("Saving tensors...")
    torch.save(X_train_tensor, OUTPUT_DIR / "X_train.pt")
    torch.save(X_test_tensor, OUTPUT_DIR / "X_test.pt")
    torch.save(y_train_tensor, OUTPUT_DIR / "y_train.pt")
    torch.save(y_test_tensor, OUTPUT_DIR / "y_test.pt")

    print("Saving preprocessing artifacts...")
    preprocessor.save(ENCODER_PATH, SCALER_PATH)

    print("Preprocessing completed successfully.")
