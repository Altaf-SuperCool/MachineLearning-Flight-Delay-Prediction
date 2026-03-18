import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

PROCESSED_PATH = Path("data/processed/processed_data.csv")
TRAIN_PATH = Path("data/processed/train.csv")
TEST_PATH = Path("data/processed/test.csv")

def run_split(test_size=0.2, random_state=42):
    print("Loading processed dataset...")
    df = pd.read_csv(PROCESSED_PATH)

    print("Splitting into train/test...")
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)

    train_df.to_csv(TRAIN_PATH, index=False)
    test_df.to_csv(TEST_PATH, index=False)

    print(f"Train saved to {TRAIN_PATH}")
    print(f"Test saved to {TEST_PATH}")

if __name__ == "__main__":
    run_split()
