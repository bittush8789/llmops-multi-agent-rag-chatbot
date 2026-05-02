# 🚀 Production LLMOps: Multi-Agent Enterprise RAG Platform

This document serves as the **Complete Implementation Guide** for transforming the TechNova Multi-Agent system into a production-grade LLMOps project. 

---

## 🏗️ 1. Architecture Overview
The platform follows a modern cloud-native architecture optimized for scale, security, and observability.

- **Frontend**: Vanilla JS (served by FastAPI)
- **Backend**: FastAPI (Async)
- **Agents**: LangGraph (Dynamic Orchestration)
- **Vector DB**: Qdrant Cloud (Managed)
- **LLM**: Groq (Llama 3.1)
- **Orchestration**: Kubernetes (AWS EKS)
- **CI/CD**: GitHub Actions
- **IaC**: Terraform

---

## 🐳 2. Containerization (Docker)
### Why Docker?
Docker ensures the application runs identically across Development, Staging, and Production environments by packaging the OS, dependencies, and code into a single immutable image.

### Implementation
We use a **Multi-Stage Build** to minimize the final image size and reduce the attack surface.
- **Stage 1 (Builder)**: Installs build dependencies and creates wheels.
- **Stage 2 (Runtime)**: Copies only the necessary files and runs as a non-root user.

**Commands:**
```bash
# Build the image
docker build -t technova-backend:latest .

# Run locally
docker run -p 8000:8000 --env-file .env technova-backend:latest
```

---

## ☸️ 3. Orchestration (Kubernetes)
The platform supports a dual-track deployment strategy: **Local Testing (Kind)** and **Production (AWS EKS)**.

### **A. Local Development with Kind**
`Kind` (Kubernetes in Docker) allows you to run a full cluster on your laptop for rapid iteration.
```bash
# Create local cluster
kind create cluster --name technova-dev

# Deploy components
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### **B. Production Deployment with AWS EKS**
For production, we use Terraform to provision a high-availability EKS cluster.
```bash
# Switch context to EKS
aws eks update-kubeconfig --region us-east-2 --name technova-eks-cluster

# Deploy production manifests
kubectl apply -f k8s/
```

### **C. Components Breakdown**
- **Deployment**: Manages pod replicas and self-healing.
- **Service**: Internal/External load balancing.
- **Ingress**: Domain-based routing and SSL termination.
- **RBAC**: Secure Role-Based Access Control within the `technova` namespace.


---

## 🛠️ 4. Infrastructure as Code (Terraform)
We use Terraform to provision the AWS EKS cluster and VPC automatically.
- **VPC Module**: Creates isolated subnets.
- **EKS Module**: Sets up the control plane and managed node groups.

**Commands:**
```bash
cd infra
terraform init
terraform plan
terraform apply --auto-approve
```

---

## 🔄 5. CI/CD Pipeline (GitHub Actions)
The pipeline automates the entire lifecycle:
1. **Linting & Testing**: Ensures code quality.
2. **Docker Push**: Builds and pushes the image to Docker Hub.
3. **K8s Deployment**: Updates the cluster image to the latest SHA.

---

## 📊 6. Monitoring & Observability
### Prometheus & Grafana
- **Prometheus**: Scrapes metrics from the `/metrics` endpoint (enabled via `prometheus-client`).
- **Grafana**: Visualizes agent usage, latency, and success rates.

### LangSmith
Integrated for deep trace analysis of LangGraph workflows to debug agent "thinking" steps.

---

## 🛡️ 7. Security Best Practices
- **Secrets Management**: Credentials (Groq, Qdrant) are injected via K8s Secrets/AWS Secrets Manager.
- **Non-Root User**: The Docker container runs as `llmops_user` (UID 1000).
- **Network Policies**: Restricts traffic only to necessary ports.
- **IAM Roles for Service Accounts (IRSA)**: Fine-grained access control for EKS pods.

---

## 🧪 9. AI Quality Evaluation (RAGAS)
To ensure the system is production-ready, we implement an automated evaluation pipeline.
- **Metrics**: Faithfulness (Hallucination check), Answer Relevancy, and Context Precision.
- **Workflow**: Compares AI answers against a "Ground Truth" dataset.

**Commands:**
```bash
# Run the evaluation suite
python -m backend.evaluator
```

---

## 📚 10. Deployment Steps (End-to-End)

1. **Step 1: Setup Infrastructure**
   Run Terraform to create the EKS cluster.
2. **Step 2: Configure Secrets**
   `kubectl create secret generic technova-secrets --from-env-file=.env`
3. **Step 3: Data Ingestion**
   Run `python backend/ingest.py` to populate Qdrant Cloud.
4. **Step 4: Quality Check**
   Run `python -m backend.evaluator` to verify system accuracy.
5. **Step 5: Push Code**
   Commit to `cicd` to trigger the GitHub Actions deployment.

---

### **Maintainer**
**Bittu Sharma**  
*AI and MLOps Engineer*
