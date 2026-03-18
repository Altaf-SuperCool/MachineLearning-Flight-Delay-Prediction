
# **🚀 Inference Architecture (Step 8)**
This section documents the production‑grade inference pipeline powering real‑time and batch airline delay predictions.  
It ensures consistent preprocessing, versioned artifacts, and reliable model execution.

---

## **📌 1. Overview**
The inference service exposes multiple endpoints for prediction:

- Real‑time JSON prediction  
- Batch JSON prediction  
- CSV file prediction  
- Raw CSV string prediction  

It uses the **same preprocessing artifacts** generated during training (Step 6) and the **trained PyTorch model** from Step 7.

---

## **📦 2. System Components**
The inference system consists of:

- **FastAPI service** (request handling, validation, routing)  
- **Preprocessing layer** (encoder + scaler)  
- **PyTorch model** (binary classifier)  
- **Postprocessing layer** (probability → label, versioning)  
- **Artifacts** (encoder, scaler, model)  

---

## **🧩 3. Architecture Diagram (Markdown‑Only)**

```
Client / External System
│
├── /predict (JSON)
├── /batch_predict (JSON list)
├── /batch_predict_csv (file upload)
└── /batch_predict_csv_string (raw CSV text)
        │
        ▼
FastAPI Inference Service
│
├── Request Validation (Pydantic)
├── Logging Middleware
├── Error Handling Middleware
│
├── Preprocessing Layer
│     ├── Load encoder_mapping.pkl (OrdinalEncoder via joblib)
│     ├── Load scaler.pkl (StandardScaler via joblib)
│     ├── Encode categorical features
│     ├── Scale numeric features
│     └── Assemble feature vector
│
├── Model Inference Layer
│     ├── Load model.pt (PyTorch)
│     ├── Forward pass
│     ├── Sigmoid → probability
│     └── Threshold → delayed / not delayed
│
└── Postprocessing Layer
      ├── Attach model version
      ├── Attach preprocessing version
      └── Format JSON response
```

---

## **🛠 4. Endpoints**

| Endpoint | Description |
|---------|-------------|
| **`POST /predict`** | Predict delay for a single flight (JSON) |
| **`POST /batch_predict`** | Predict delay for multiple flights (JSON list) |
| **`POST /batch_predict_csv`** | Predict delay from uploaded CSV file |
| **`POST /batch_predict_csv_string`** | Predict delay from raw CSV text |
| **`GET /health`** | Liveness probe |
| **`GET /ready`** | Readiness probe (checks artifacts + model) |
| **`GET /version`** | Returns model + preprocessing versions |

---

## **📁 5. Artifact Dependencies**

| Artifact | Description | Source |
|----------|-------------|--------|
| `encoder_mapping.pkl` | OrdinalEncoder | Step 6 preprocessing |
| `scaler.pkl` | StandardScaler | Step 6 preprocessing |
| `model.pt` | Trained PyTorch model | Step 7 training |

All artifacts must be present for the service to be considered **ready**.

---

## **⚙️ 6. Request Lifecycle**

### **1. Validation**
- Pydantic ensures strict schema compliance  
- CSV inputs are parsed into DataFrames  

### **2. Preprocessing**
- Encoder + scaler loaded via joblib  
- Categorical → ordinal encoding  
- Numeric → standard scaling  
- Combined into a single feature vector  

### **3. Inference**
- PyTorch model loaded once at startup  
- Forward pass → logits  
- Sigmoid → probability  
- Threshold → binary label  

### **4. Postprocessing**
- Attach version metadata  
- Format JSON response  

---

## **📈 7. Operational Characteristics**

### **Performance**
- Low‑latency CPU inference  
- Artifacts loaded once at startup  

### **Reliability**
- Global exception middleware  
- Structured logging  
- Health + readiness endpoints  

### **Scalability**
- Stateless API  
- Horizontal scaling via Kubernetes / Harness  

---

## **🚀 8. Deployment Notes**
- Containerized via Docker (Step 8.13)  
- Deployed via Harness pipelines  
- Supports canary + rolling deployments  
- Versioned artifacts ensure reproducibility  

---

