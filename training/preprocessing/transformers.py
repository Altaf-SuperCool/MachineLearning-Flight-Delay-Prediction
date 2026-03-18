import joblib
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
import numpy as np

class CombinedPreprocessor:
    def __init__(self, categorical_cols, numeric_cols):
        self.categorical_cols = categorical_cols
        self.numeric_cols = numeric_cols

        # Integer encoding for PyTorch embeddings
        self.encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value",
            unknown_value=-1
        )

        # Numeric scaling
        self.scaler = StandardScaler()

    def fit(self, df):
        self.encoder.fit(df[self.categorical_cols])
        self.scaler.fit(df[self.numeric_cols])

    def transform(self, df):
        # Integer encoded categorical features
        X_cat = self.encoder.transform(df[self.categorical_cols])

        # Scaled numeric features
        X_num = self.scaler.transform(df[self.numeric_cols])

        # Combine into a single dense matrix
        X = np.hstack([X_cat, X_num])

        return X

    def save(self, encoder_path, scaler_path):
        joblib.dump(self.encoder, encoder_path)
        joblib.dump(self.scaler, scaler_path)

    def load(self, encoder_path, scaler_path):
        self.encoder = joblib.load(encoder_path)
        self.scaler = joblib.load(scaler_path)
