
# **📘 Step 8 — Inference API, Dockerization, Helm Deployment & CI/CD (Consolidated)**

This document consolidates all commands, components, and architecture involved in **Step 8** of the MLOps pipeline.  
It covers everything from the inference API to Docker, Helm, CI/CD, Kubernetes deployment, and monitoring.

---

# **8.1 — Inference API (FastAPI)**

### **Run Locally (Uvicorn)**  
```bash
uvicorn inference.api:app --reload --host 0.0.0.0 --port 8000
```

### **Endpoints**
| Endpoint | Description |
|---------|-------------|
| `POST /predict` | Single JSON prediction |
| `POST /batch_predict` | Batch JSON prediction |
| `POST /batch_predict_csv` | CSV file upload prediction |
| `POST /batch_predict_csv_string` | Raw CSV string prediction |
| `GET /health` | Liveness probe |
| `GET /ready` | Readiness probe |
| `GET /version` | Model + preprocessing version |

### **Artifacts Loaded**
- `encoder_mapping.pkl`
- `scaler.pkl`
- `model.pt`

---

# **8.2 — Logging & Error Middleware**

### **Logging Features**
- Structured JSON logs  
- Request lifecycle logs  
- Error logs  
- Optional latency logs  

### **Error Middleware**
- Global exception handler  
- No try/except inside endpoints  
- Clean 500 responses  

---

# **8.3 — Dockerfile (Production‑Grade)**

### **Build Docker Image**
```bash
docker build -t inference-api:latest .
```

### **Run Locally**
```bash
docker run -p 8000:8000 inference-api:latest
```

### **Push to Registry**
```bash
docker tag inference-api:latest <registry>/inference-api:<tag>
docker push <registry>/inference-api:<tag>
```

### **Production Command (Gunicorn + Uvicorn Workers)**  
Executed inside the container:

```
gunicorn inference.api:app \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --workers 2
```

---

# **8.4 — Helm Deployment (Option 1 — Helm Only)**

### **Folder Structure**
```
deploy/
  helm/
    inference-api/
      Chart.yaml
      values.yaml
      templates/
        deployment.yaml
        service.yaml
        hpa.yaml
        configmap.yaml
        ingress.yaml
```

### **PowerShell Commands to Create Helm Structure**
```powershell
New-Item -ItemType Directory -Force -Path "deploy"
New-Item -ItemType Directory -Force -Path "deploy/helm"
New-Item -ItemType Directory -Force -Path "deploy/helm/inference-api"
New-Item -ItemType Directory -Force -Path "deploy/helm/inference-api/templates"

New-Item -ItemType File -Force -Path "deploy/helm/inference-api/Chart.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/values.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/templates/deployment.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/templates/service.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/templates/hpa.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/templates/configmap.yaml"
New-Item -ItemType File -Force -Path "deploy/helm/inference-api/templates/ingress.yaml"
```

### **Service Type**
```
ClusterIP
```

### **Ingress**
- Uses AWS Load Balancer Controller  
- Exposes API externally  
- Routes traffic to ClusterIP service  

---

# **8.5 — CI Pipeline (Harness CI)**

### **CI Responsibilities**
- Clone repo  
- Install dependencies  
- Run tests  
- Build Docker image  
- Push to ECR/DockerHub  
- Emit image tag  

### **CI Output**
```
<registry>/inference-api:<commit-sha>
```

### **CI Trigger**
- On PR  
- On push to main  
- On tag  

---

# **8.6 — CD Pipeline (Harness CD → Helm → EKS)**

### **CD Responsibilities**
- Pull Docker image  
- Inject image tag into Helm values  
- Deploy Helm chart to EKS  
- Rolling/Canary/Blue‑Green rollout  
- Validate readiness probes  
- Roll back on failure  

### **CD Uses**
```
chartPath: deploy/helm/inference-api
valuesPaths:
  - deploy/helm/inference-api/values.yaml
```

### **Deployment Flow**
```
CI builds → pushes image → CD picks tag → Helm deploys → EKS runs pods
```

---

# **8.7 — How Terraform Fits In**

Terraform provisions infrastructure **once**, not on every deployment.

### **Terraform Provisions**
- EKS cluster  
- Node groups  
- VPC + subnets  
- IAM roles  
- ECR registry  
- S3 buckets  
- CloudWatch logging  
- AWS Load Balancer Controller  

### **Terraform Commands**
```bash
terraform init
terraform plan
terraform apply
```

Terraform is **not part of CI/CD** — it is infrastructure provisioning.

---

# **8.8 — Monitoring Hooks**

### **What We Log**
- Input drift signals  
- Prediction drift signals  
- Latency  
- Errors  
- Request metadata  

### **Where Logs Go**
- CloudWatch  
- Grafana/Loki  
- Prometheus (optional)  
- Harness SRM (optional)  

---

# **8.9 — Step 8 Architecture Summary**

```
Terraform (one-time infra)
        │
        ▼
EKS Cluster ←──────────────┐
                           │
CI Pipeline (build image)  │
        │                  │
        ▼                  │
Docker Image in ECR        │
        │                  │
        ▼                  │
CD Pipeline (Helm deploy) ─┘
        │
        ▼
Inference API running in Kubernetes
```

---

# **8.10 — Commands Summary**

### **Local Development**
```bash
uvicorn inference.api:app --reload --host 0.0.0.0 --port 8000
```

### **Docker Build**
```bash
docker build -t inference-api:latest .
```

### **Docker Run**
```bash
docker run -p 8000:8000 inference-api:latest
```

### **Docker Push**
```bash
docker tag inference-api:latest <registry>/inference-api:<tag>
docker push <registry>/inference-api:<tag>
```

### **Terraform**
```bash
terraform init
terraform plan
terraform apply
```

### **Harness CI/CD**
Handled automatically by:

```
.harness/ci-inference.yaml
.harness/cd-inference.yaml
```

---

# **8.11 — Final Deliverables in Step 8**

| Component | Status |
|----------|--------|
| Inference API | ✅ Completed |
| Logging + Error Middleware | ✅ Completed |
| Dockerfile | ✅ Completed |
| Helm Chart | ✅ Completed |
| CI Pipeline (Harness) | ✅ Completed |
| CD Pipeline (Harness → Helm → EKS) | ✅ Completed |
| Monitoring Hooks | ✅ Completed |
| Architecture Documentation | ✅ Completed |

---

