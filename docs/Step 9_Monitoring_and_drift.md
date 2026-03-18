# **📘 Step 9 — Monitoring, Metrics & Drift Detection (Consolidated Summary)**

Step 9 adds **observability** and **model drift detection** to the inference service.  
This includes:

- Monitoring middleware  
- Prometheus metrics  
- Structured JSON logs  
- Input drift (PSI)  
- Prediction drift (KL Divergence)  
- Drift logging inside `predict_single_flight()`  
- Validation via PowerShell commands  

---

## **9.1 — Files & Folders Created (PowerShell Commands)**

```powershell
# Monitoring folder
New-Item -ItemType Directory -Force -Path "inference/monitoring"

# Drift folder
New-Item -ItemType Directory -Force -Path "inference/drift"

# Monitoring files
New-Item -ItemType File -Force -Path "inference/monitoring/logger.py"
New-Item -ItemType File -Force -Path "inference/monitoring/middleware.py"
New-Item -ItemType File -Force -Path "inference/monitoring/metrics.py"

# Drift detection files
New-Item -ItemType File -Force -Path "inference/drift/input_drift.py"
New-Item -ItemType File -Force -Path "inference/drift/prediction_drift.py"
```

---

## **9.2 — Step 9 Code Added**

### **Monitoring Middleware**
- Tracks request count  
- Tracks errors  
- Measures latency  
- Emits structured JSON logs  

### **Prometheus Metrics**
- `/metrics` endpoint added  
- Counters + histograms exposed  

### **Drift Detection**
- PSI for input drift  
- KL Divergence for prediction drift  
- Logged inside `predict_single_flight()`  

### **Updated `api.py`**
- Added monitoring middleware  
- Added `/metrics` endpoint  
- Kept Step 8 logging + error middleware  

### **Updated `predict_single_flight()`**
- Added drift detection  
- Added drift logging  
- Added baseline placeholder distributions  

---

## **9.3 — Commands Executed to Test Step 9 (PowerShell)**

### **Start API**
```powershell
uvicorn inference.api:app --reload --host 0.0.0.0 --port 8000
```

### **Health & Ready**
```powershell
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/version
```

### **Metrics**
```powershell
curl http://localhost:8000/metrics
```

### **Single Prediction (JSON)**
```powershell
curl -Method POST `
     -Uri "http://localhost:8000/predict" `
     -ContentType "application/json" `
     -Body '{
        "OP_CARRIER": "AA",
        "ORIGIN": "ORD",
        "DEST": "DFW",
        "CRS_DEP_TIME": 1430,
        "CRS_ARR_TIME": 1700,
        "DISTANCE": 802
     }'
```

### **Batch Prediction (JSON)**
```powershell
curl -Method POST `
     -Uri "http://localhost:8000/batch_predict" `
     -ContentType "application/json" `
     -Body '{
        "flights": [
          {
            "OP_CARRIER": "AA",
            "ORIGIN": "ORD",
            "DEST": "DFW",
            "CRS_DEP_TIME": 1430,
            "CRS_ARR_TIME": 1700,
            "DISTANCE": 802
          }
        ]
     }'
```

### **CSV Prediction (File Upload)**
```powershell
curl -Method POST `
     -Uri "http://localhost:8000/batch_predict_csv" `
     -Form @{ file = Get-Item ".\flights.csv" }
```

### **CSV Prediction (Raw String)**
```powershell
curl -Method POST `
     -Uri "http://localhost:8000/batch_predict_csv" `
     -ContentType "application/json" `
     -Body '{ "csv_string": "OP_CARRIER,ORIGIN,DEST,CRS_DEP_TIME,CRS_ARR_TIME,DISTANCE\nAA,ORD,DFW,1430,1700,802" }'
```

---

## **9.4 — Observed Outcomes (Logs & Metrics)**

### **Monitoring Middleware Logs**
```
"event": "request_completed",
"path": "/predict",
"method": "POST",
"status_code": 200,
"latency_ms": 14.59
```

### **Drift Logs**
```
"event": "drift",
"input_psi": 0.9679,
"pred_kl": 0.2004,
"model_version": "1.0.0"
```

### **Metrics Endpoint Output**
```
# HELP inference_requests_total Total inference requests
inference_requests_total 3
```

### **Error Handling Verified**
Invalid payload → structured error logs emitted.

---

## **9.5 — Simple Drift Example (Human‑Friendly)**

### **Training Data (Summer)**
```
Weather Score:
0.8, 0.9, 0.7, 0.85, 0.95
```

### **Incoming Data (Stormy Day)**
```
0.1, 0.2, 0.15, 0.05, 0.12
```

### **Drift Detection Says**
- PSI ≈ **1.0** → big change in input data  
- KL ≈ **0.2** → predictions shifting  

### **Meaning**
> “The world looks different from what the model learned.  
> You may need retraining or updated features.”

This is exactly what your logs showed.

---

## **9.6 — Step 9 Deliverables Completed**

| Component | Status |
|----------|--------|
| Monitoring Middleware | ✅ |
| Prometheus Metrics | ✅ |
| Drift Detection (PSI + KL) | ✅ |
| Drift Logging | ✅ |
| Updated `api.py` | ✅ |
| Updated `predict_single_flight()` | ✅ |
| JSON + CSV Prediction Tests | ✅ |
| PowerShell Testing | ✅ |
| Documentation | ✅ |

---

