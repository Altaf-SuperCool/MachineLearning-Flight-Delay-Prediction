from pathlib import Path
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import roc_auc_score, classification_report

DATA_DIR = Path("data/processed")
ARTIFACT_DIR = Path("artifacts")
ARTIFACT_DIR.mkdir(exist_ok=True)

MODEL_PATH = ARTIFACT_DIR / "model.pt"

BATCH_SIZE = 4096
EPOCHS = 5
LR = 1e-3
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class FlightDelayDataset(Dataset):
    def __init__(self, X_path, y_path):
        self.X = torch.load(X_path)
        self.y = torch.load(y_path)

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class MLPModel(nn.Module):
    def __init__(self, input_dim):
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


def load_data():
    X_train = DATA_DIR / "X_train.pt"
    X_test = DATA_DIR / "X_test.pt"
    y_train = DATA_DIR / "y_train.pt"
    y_test = DATA_DIR / "y_test.pt"

    train_ds = FlightDelayDataset(X_train, y_train)
    test_ds = FlightDelayDataset(X_test, y_test)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    input_dim = train_ds.X.shape[1]
    return train_loader, test_loader, input_dim


def train_one_epoch(model, loader, criterion, optimizer):
    model.train()
    total_loss = 0.0

    for X_batch, y_batch in loader:
        X_batch = X_batch.to(DEVICE)
        y_batch = y_batch.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * X_batch.size(0)

    return total_loss / len(loader.dataset)


def evaluate(model, loader):
    model.eval()
    all_preds = []
    all_probs = []
    all_targets = []

    with torch.inference_mode():
        for X_batch, y_batch in loader:
            X_batch = X_batch.to(DEVICE)
            y_batch = y_batch.to(DEVICE)

            outputs = model(X_batch)
            probs = outputs.detach().cpu()
            preds = (probs >= 0.5).int()

            all_probs.append(probs)
            all_preds.append(preds)
            all_targets.append(y_batch.cpu())

    all_probs = torch.cat(all_probs).numpy()
    all_preds = torch.cat(all_preds).numpy()
    all_targets = torch.cat(all_targets).numpy()

    try:
        auc = roc_auc_score(all_targets, all_probs)
    except ValueError:
        auc = None

    print("Classification report:")
    print(classification_report(all_targets, all_preds))

    if auc is not None:
        print(f"ROC-AUC: {auc:.4f}")
    else:
        print("ROC-AUC: not defined (only one class present).")


def run_training():
    print(f"Using device: {DEVICE}")

    train_loader, test_loader, input_dim = load_data()
    print(f"Input dimension: {input_dim}")

    model = MLPModel(input_dim=input_dim).to(DEVICE)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer)
        print(f"Epoch {epoch}/{EPOCHS} - Train Loss: {train_loss:.4f}")

    print("Evaluating on test set...")
    evaluate(model, test_loader)

    print(f"Saving model to {MODEL_PATH}...")
    torch.save(model.state_dict(), MODEL_PATH)
    print("Model saved successfully.")


if __name__ == "__main__":
    run_training()
