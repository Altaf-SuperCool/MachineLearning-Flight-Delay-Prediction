# ✈️ **Airline Delay MLOps: End-to-End Deep Learning Pipeline**

This repository contains a production-grade MLOps system for predicting airline delays. It covers the entire lifecycle from Infrastructure as Code (IaC) and PyTorch model training to FastAPI deployment on Kubernetes with real-time drift monitoring.

## 👨‍💻 Author
**Altaf Hussain Shaik**  
*AI Generalist*  
📧 [shaikusa@outlook.com](mailto:shaikusa@outlook.com)

---
## 🏗️ Architecture Diagram

![ML Pipeline Architecture](docs/Images/ArchitectureDiagramm.png)

## **1. Project Vision & Objectives**
In the aviation industry, delays cause significant operational costs and passenger dissatisfaction. This project achieves the following:
* **Predictive Intelligence:** Anticipates disruptions by converting flight schedules and historical patterns into a binary classification (Delay vs. On-time).
* **Operational Readiness:** Uses a "Lean Feature Set" (Carrier, Route, Timing) for high-signal, low-latency predictions.
* **MLOps Excellence:** Demonstrates a full lifecycle including automated infrastructure provisioning, CI/CD pipelines, and post-deployment observability.

---

## **2. 🚀 Complete Project Folder Structure**
The project follows a modular, production-ready layout to ensure a clean separation of concerns:

```text
airline-delay-mlops/
├── training/                 # Data Ingestion, Split, & PyTorch Training
│   ├── config/               # config.yaml, params.yaml, schema.json
│   ├── data_ingestion/       # CSV/S3 loading logic
│   ├── data_validation/      # validate.py & expectations.json
│   ├── feature_engineering/  # Encoding, Scaling, & Tensor Conversion
│   └── model/                # Model definition, training loop, & evaluation
├── inference/                # FastAPI Application
│   ├── app/                  # Prediction logic, drift monitoring, & metrics
│   ├── routers/              # Health, Prediction, and Metadata endpoints
│   └── Dockerfile            # Containerization manifest
├── mcp-server/               # Model Context Protocol (MCP) Server logic
├── terraform/                # IaC (EKS, ECR, VPC, IAM, Prometheus)
├── helm/                     # K8s Deployment manifests (Inference & MCP)
├── harness/                  # CI/CD Pipeline definitions (YAML)
├── monitoring/               # Prometheus rules and Grafana dashboards
└── scripts/                  # Build, deploy, and cleanup utilities
```
*(Detailed sub-directories included for all modules from infrastructure to monitoring.)*

---

## **3. High-Level Architecture**

* **Infrastructure (Terraform):** Provisions the foundation (VPC, EKS, ECR, S3) once. It is not part of the daily CI/CD flow.
* **CI Pipeline (Harness/GitHub):** Clones the repo, runs tests, builds Docker images, and pushes them to ECR on every code change.
* **CD Pipeline:** Pulls the versioned Docker image and deploys it to EKS using Helm charts.
* **Monitoring:** Tracks system health and data drift using Prometheus and Grafana.

---

## **4. Data & Feature Engineering**

### **4.1 Data Source**
We utilize the **Kaggle Airline Delay Dataset**.
* **Raw Data Path:** `data/raw/airline_delays.csv`
* **Ingestion:** `python -m training.data_ingestion.ingest`

### **4.2 The Lean Feature Set (6 Features)**
The model uses exactly 6 inputs to ensure high performance and stability:
1.  **Categorical:** `OP_CARRIER`, `ORIGIN`, `DEST` (Ordinal Encoded).
2.  **Numeric:** `CRS_DEP_TIME`, `CRS_ARR_TIME`, `DISTANCE` (Standard Scaled).

### **4.3 Processing Execution**
```powershell
# Split data into train/test
python -m training.data_split.split

# Encode, Scale, and convert to PyTorch Tensors (.pt)
python -m training.feature_engineering.feature_engineer
```
**Artifacts Generated:** `X_train.pt`, `y_train.pt`, `encoder_mapping.pkl`, and `scaler.pkl`.

---

## **5. Model Training (PyTorch)**

The model is a **Multi-Layer Perceptron (MLP)** dense neural network.
* **Input Shape:** `[N, 6]`
* **Execution:** `python -m training.model_training.train`
* **Output:** `artifacts/model.pt` (Trained weights for Step 8).

---

## **6. Inference API & Deployment**

### **6.1 FastAPI Service**
Supports high-throughput prediction via several endpoints:
* `POST /predict`: Single flight JSON.
* `POST /batch_predict_csv`: Bulk CSV upload.
* `GET /health` & `GET /ready`: Kubernetes liveness/readiness probes.

### **6.2 Deployment Commands**
```bash
# Local Development
uvicorn inference.api:app --host 0.0.0.0 --port 8000

# Docker Build & Push
docker build -t inference-api:latest .
docker push <registry>/inference-api:<tag>

# Helm Deployment
helm install inference-api ./helm/inference
```
*(Commands summary for local, Docker, and Terraform.)*

---

## **7. Monitoring & Drift Detection**

### **7.1 Drift Metrics**
To prevent model decay, we monitor the difference between training data and live production data.
* **PSI (Population Stability Index):** Monitors input feature shifts.
* **KL Divergence:** Monitors shifts in the model’s prediction distribution.

| Metric | Moderate Drift | Significant Drift (Alert) |
| :--- | :--- | :--- |
| **PSI** | 0.1 – 0.25 | > 0.25 |
| **KL Divergence** | 0.05 – 0.15 | > 0.15 |

### **7.2 Observability Stack**
* **Prometheus:** Scrapes `drift_input_alerts_total` and latency metrics.
* **Grafana:** Provides real-time dashboards for PSI, KL Divergence, and error rates.

---
My journey through this project has evolved from a series of technical steps into a comprehensive mastery of the MLOps lifecycle. By integrating a deep learning model into a production-grade cloud environment, i have transitioned from a data scientist to an M-L engineer.

### 🧠 What i Have Learnt

* **Deep Learning Lifecycle:** I have mastered the transition from raw data ingestion and feature engineering to training a PyTorch Multi-Layer Perceptron (MLP) for binary classification.

* **Production-Grade API Design:** I gained experience building high-performance FastAPI services that support various input types, including single JSON objects and bulk CSV uploads.

* **Model Observability:** I have implemented industry-standard monitoring, learning how to use Population Stability Index (PSI) and KL Divergence to detect data and prediction drift in real-time.


---

### 🏆 Key Achievements

* **End-to-End Pipeline Integration:** I have successfully connected disparate stages—data engineering, model training, DevOps, and monitoring—into a single, cohesive ecosystem.
* **Scalable Architecture:** I built a stateless, containerized inference service capable of horizontal scaling within a Kubernetes (EKS) cluster to handle high-traffic flight prediction requests.
* **"Lean" Feature Optimization:** I achieved a high-signal baseline model by identifying and engineering a 6-feature "Lean Set" (Carrier, Origin, Dest, Dep/Arr Time, Distance) that balances accuracy with low-latency performance.
* **Automated Drift Guardrails:** I established a proactive alerting system that notifies engineers when the environment shifts (e.g., weather-related delays), ensuring the model never makes stale or "blind" predictions in production.
* **Enterprise-Ready Documentation:** I consolidated a complex project into a professional-grade repository structure that follows industry standards for folder organization and documentation.

This project serves as a powerful demonstration of my ability to manage the **entire** machine learning value chain, from the first line of code to the final monitoring dashboard.
