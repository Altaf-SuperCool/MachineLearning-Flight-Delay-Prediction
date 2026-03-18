# 📘 **Airline Delay MLOps — Project Setup (Step 1 to Step 3)**  
*Consolidated Technical Reference*

---

# #️⃣ **Step 1 — Project Creation (Root Setup)**

## **1. Create project root folder**
```powershell
mkdir airline-delay-mlops
cd airline-delay-mlops
git init
```

## **2. Create core root files**
```powershell
New-Item -ItemType File -Path "README.md"
New-Item -ItemType File -Path ".gitignore"
New-Item -ItemType File -Path "requirements.txt"
New-Item -ItemType File -Path "pyproject.toml"
```

## **3. Create top‑level module folders**
```powershell
mkdir training
mkdir inference
mkdir mcp-server
mkdir helm
mkdir terraform
mkdir harness
mkdir monitoring
mkdir scripts
mkdir data
```

## **4. Add Python package initializers**
```powershell
New-Item -ItemType File -Path "training\__init__.py"
New-Item -ItemType File -Path "inference\__init__.py"
New-Item -ItemType File -Path "mcp-server\__init__.py"
```

## **5. Recommended root `.gitignore`**
```gitignore
__pycache__/
*.pyc
.env
.venv
.idea/
.vscode/
dist/
build/
*.egg-info/
.ipynb_checkpoints/
.terraform/
terraform.tfstate*
```

## **6. Recommended root `requirements.txt` (dev tools only)**
```
black
isort
flake8
pre-commit
```
## **7. Recommended `pyproject.toml`**
```toml
[tool.black]
line-length = 100

[tool.isort]
profile = "black"
line_length = 100
```

---

# #️⃣ **Step 2 — Training Module Structure**

## **Create training subfolders**
```powershell
New-Item -ItemType Directory -Path "training\config"
New-Item -ItemType Directory -Path "training\data_ingestion"
New-Item -ItemType Directory -Path "training\data_validation"
New-Item -ItemType Directory -Path "training\feature_engineering"
New-Item -ItemType Directory -Path "training\model"
New-Item -ItemType Directory -Path "training\mlflow_utils"
New-Item -ItemType Directory -Path "training\scripts"
New-Item -ItemType Directory -Path "data" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "data\raw" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "data\processed" -ErrorAction SilentlyContinue

```

## **Create all training files**

### **config/**
```powershell
New-Item -ItemType File -Path "training\config\config.yaml"
New-Item -ItemType File -Path "training\config\params.yaml"
New-Item -ItemType File -Path "training\config\schema.json"
```

### **data_ingestion/**
```powershell
New-Item -ItemType File -Path "training\data_ingestion\__init__.py"
New-Item -ItemType File -Path "training\data_ingestion\ingest.py"
New-Item -ItemType File -Path "training\data_ingestion\s3_loader.py"
```

### **data_validation/**
```powershell
New-Item -ItemType File -Path "training\data_validation\__init__.py"
New-Item -ItemType File -Path "training\data_validation\validate.py"
New-Item -ItemType File -Path "training\data_validation\expectations.json"
```

### **feature_engineering/**
```powershell
New-Item -ItemType File -Path "training\feature_engineering\__init__.py"
New-Item -ItemType File -Path "training\feature_engineering\preprocess.py"
New-Item -ItemType File -Path "training\feature_engineering\transformers.py"
```

### **model/**
```powershell
New-Item -ItemType File -Path "training\model\__init__.py"
New-Item -ItemType File -Path "training\model\model_def.py"
New-Item -ItemType File -Path "training\model\train.py"
New-Item -ItemType File -Path "training\model\evaluate.py"
New-Item -ItemType File -Path "training\model\callbacks.py"
New-Item -ItemType File -Path "training\model\save_model.py"
```

### **mlflow_utils/**
```powershell
New-Item -ItemType File -Path "training\mlflow_utils\__init__.py"
New-Item -ItemType File -Path "training\mlflow_utils\mlflow_client.py"
New-Item -ItemType File -Path "training\mlflow_utils\registry.py"
```

### **scripts/**
```powershell
New-Item -ItemType File -Path "training\scripts\run_training.sh"
New-Item -ItemType File -Path "training\scripts\run_evaluation.sh"
New-Item -ItemType File -Path "training\scripts\export_artifacts.sh"
```

### **requirements.txt**
```powershell
New-Item -ItemType File -Path "training\requirements.txt"
```

---

# #️⃣ **Step 3 — Training Environment Setup**

## **3.1 Create virtual environment**
```powershell
python -m venv training\.venv
training\.venv\Scripts\activate
```

## **3.2 Populate `training/requirements.txt` (Python 3.11 + Windows compatible)**

```powershell
Set-Content -Path "training\requirements.txt" -Value @"
torch==2.2.0
torchvision==0.17.0
torchaudio==2.2.0

mlflow==2.12.1
pandas==2.2.1
numpy==1.26.4
scikit-learn==1.3.2
pyyaml==6.0.1
boto3==1.34.34
great_expectations==0.18.12
matplotlib==3.8.2
seaborn==0.13.2
joblib==1.3.2
"@
```

## **3.3 Install dependencies**
```powershell
pip install -r training\requirements.txt 
python -m pip install -r training/requirements.txt

```

---
### **data/raw/airline_delays.csv**
```powershell
New-Item -ItemType Directory -Path "data\raw"
```

# 🎉 **Steps 1–3 Completed Successfully**

You now have:

- A clean, professional project root  
- A fully scaffolded training module  
- A working Python 3.11 training environment  
- TensorFlow + MLflow + data stack installed  
- Windows‑compatible dependency versions  

This is the perfect foundation for the next steps.

---

# ✈️ ** Kaggle: Airline Delay Dataset (CSV Ready)**  
If you want **CSV directly**, Kaggle is the easiest.

### Popular dataset:
**“Airline Delay and Cancellation Data”**

Download from Kaggle → extract → rename to:
https://www.kaggle.com/datasets/usdot/flight-delays/flights.csv
```
data/raw/airline_delays.csv
```

This dataset includes:
- FL_DATE  
- OP_CARRIER  
- ORIGIN  
- DEST  
- CRS_DEP_TIME  
- CRS_ARR_TIME  
- DISTANCE  
- DEP_DELAY  
- ARR_DELAY  

Exactly matching your schema.

---

data/raw/airline_delays.csv

Your training pipeline will read from this path.
```
## **Generate Helm Folder + Files**
```powershell
# Create folder structure
New-Item -ItemType Directory -Force -Path "deploy"
New-Item -ItemType Directory -Force -Path "deploy/helm"
New-Item -ItemType Directory -Force -Path "deploy/helm/inference-api"
New-Item -ItemType Directory -Force -Path "deploy/helm/inference-api/templates"

# Create empty files
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/Chart.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/values.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/templates/deployment.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/templates/service.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/templates/hpa.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/templates/configmap.yaml"
```