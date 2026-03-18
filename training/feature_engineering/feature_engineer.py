import pandas as pd
from pathlib import Path
from training.preprocessing.preprocess import run_preprocessing

TRAIN_PATH = Path("data/processed/train.csv")
TEST_PATH = Path("data/processed/test.csv")

def run_feature_engineering():
    print("Loading train/test datasets...")
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    print("Running preprocessing pipeline...")
    run_preprocessing(train_df, test_df)

    print("Feature engineering completed successfully.")

if __name__ == "__main__":
    run_feature_engineering()
