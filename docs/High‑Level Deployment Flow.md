
# **🚀 High‑Level Deployment Flow**
Here’s the big picture:

```
Developer Pushes Code → CI Pipeline → Docker Image → CD Pipeline → EKS Deployment
```

Terraform sits **underneath** this whole process — it provisions the infrastructure **once**, not on every deployment.

Let’s break it down.

---

# **1️⃣ CI Pipeline (Build + Test + Docker Image)**
CI runs **every time code changes**.

### What CI does:
- Clones repo  
- Installs dependencies  
- Runs tests  
- Builds Docker image  
- Pushes image to ECR (or Docker Hub)  
- Produces an image tag (commit SHA or build number)

### Output of CI:
```
docker.io/altaf/inference-api:<commit-sha>
```

This image tag is passed to CD.

**Terraform is NOT involved in CI.**  
CI only builds artifacts.

---

# **2️⃣ Terraform (Infrastructure Provisioning)**
Terraform is **not part of CI/CD**.  
Terraform is **infrastructure as code**, executed manually or via a separate pipeline.

Terraform provisions:

### ✔ EKS Cluster  
### ✔ Node Groups  
### ✔ VPC / Subnets  
### ✔ IAM Roles  
### ✔ ECR Registry  
### ✔ S3 Buckets  
### ✔ CloudWatch Logging  
### ✔ Security Groups  
### ✔ Load Balancers  

Terraform is run:

- When you create the cluster  
- When you update infrastructure  
- When you add new environments  

**Terraform does NOT run on every deployment.**

### Terraform output includes:
- EKS cluster endpoint  
- OIDC provider  
- IAM roles  
- Node group ARNs  
- VPC networking  
- ECR repo URL  

Harness CD uses these outputs to deploy workloads.

---

# **3️⃣ CD Pipeline (Harness → Kubernetes Deployment)**
Once CI finishes and pushes an image, CD takes over.

### CD does:
- Pulls the new Docker image  
- Applies Kubernetes manifests (Deployment, Service, HPA, etc.)  
- Performs Rolling / Canary / Blue‑Green deployment  
- Validates readiness probes  
- Rolls back if needed  

### CD uses:
- The EKS cluster provisioned by Terraform  
- The Docker image built by CI  
- The Kubernetes manifests stored in your repo  

### CD does NOT:
- Build images  
- Run tests  
- Provision infrastructure  

CD only deploys.

---

# **🔥 Putting It All Together (End‑to‑End Flow)**

Here is the full lifecycle in one clean diagram:

```
                ┌──────────────────────────┐
                │        Developer         │
                │       pushes code        │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │           CI             │
                │  - Install deps          │
                │  - Run tests             │
                │  - Build Docker image    │
                │  - Push to ECR           │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │           CD             │
                │  - Pull image            │
                │  - Apply K8s manifests   │
                │  - Rolling/Canary deploy │
                │  - Health checks         │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │        Kubernetes        │
                │         (EKS)            │
                │  - Pods / Services       │
                │  - HPA / Ingress         │
                └──────────────────────────┘

                ┌──────────────────────────┐
                │        Terraform         │
                │  - Provisions EKS        │
                │  - Creates ECR           │
                │  - Networking / IAM      │
                └──────────────────────────┘
```

---

# **🧠 Key Insight**
Terraform is **infrastructure provisioning**.  
CI is **artifact creation**.  
CD is **artifact deployment**.

They are **separate concerns**, but they work together like this:

### Terraform → Creates the environment  
### CI → Creates the Docker image  
### CD → Deploys the image into the environment  

This is the cleanest, most scalable architecture.

---

# **💡 What Happens When You Push Code?**

### Step 1 — CI runs  
- Builds Docker image  
- Pushes to ECR  
- Emits image tag  

### Step 2 — CD triggers  
- Takes the image tag  
- Applies Kubernetes manifests  
- Deploys to EKS  

### Step 3 — Kubernetes runs your app  
- Pods start  
- Readiness/liveness probes check health  
- Traffic shifts gradually (if canary)  

Terraform is **not touched** during this process.

---

# **📌 What Happens When You Change Infrastructure?**

You run:

```
terraform plan
terraform apply
```

This updates:

- Cluster  
- Node groups  
- Networking  
- IAM  
- ECR  
- S3  
- etc.

CI/CD is **not touched** during this process.

---
