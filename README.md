# 🌌 TechNova Solutions: Enterprise Multi-Agent LLMOps Platform

[![Production Ready](https://img.shields.io/badge/Status-Production--Ready-brightgreen.svg)](https://github.com/bittush8789/llmops-multi-agent-rag-chatbot)
[![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes-blue.svg)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-blueviolet.svg)](https://www.terraform.io/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## 📋 1. Project Overview
**TechNova Solutions** is a high-performance, production-grade LLMOps platform designed to automate enterprise intelligence. Built on a **Multi-Agent Orchestration** architecture, it leverages 10 specialized AI agents (Sales, HR, IT, etc.) and a deep **RAG pipeline** to provide grounded, secure, and accurate responses.

This repository serves as a master template for **LLMOps best practices**, covering everything from IaC and Containerization to automated AI Quality Evaluation.

---

## 🏗️ 2. Production Architecture
A decoupled, cloud-native design optimized for horizontal scalability and observability.

```mermaid
graph TD
    subgraph Client_Layer
        User([User]) --> Ingress[Nginx Ingress / ALB]
    end

    subgraph Orchestration_Layer
        Ingress --> K8s[EKS Cluster / Kind]
        K8s --> NS[technova Namespace]
        NS --> Pods[FastAPI Backend Pods]
        Pods --> Graph[LangGraph Orchestrator]
    end

    subgraph Intelligence_Layer
        Graph --> Retriever[Qdrant Cloud Retriever]
        Graph --> Agents[Domain Agents]
        Agents --> LLM[Groq Inference Engine]
        Agents --> Eval[Ragas Evaluation Suite]
    end

    subgraph Ops_Layer
        Pods --> Metrics[Prometheus / Grafana]
        GitHub[GitHub Actions] --> Docker[Docker Hub]
        Docker --> K8s
        Terraform[Terraform IaC] --> K8s
    end
```

---

## 🛠️ 3. Industry-Standard Setup (Step-by-Step)

Follow these precise steps to deploy the entire stack.

### **Phase 1: Environment Preparation**
Ensure you have the following tools installed:
- **Python 3.10+**
- **Docker & Docker Compose**
- **Terraform**
- **Kubectl & Helm**
- **AWS CLI** (Configured)
- **Kind** (For local K8s testing)

### **Phase 2: Data Ingestion (Vector Database)**
Populate the Qdrant Cloud Vector Store with 60+ enterprise documents.
```bash
# 1. Clone & Setup
git clone -b cicd https://github.com/bittush8789/llmops-multi-agent-rag-chatbot.git
cd llmops-multi-agent-rag-chatbot
python -m venv venv && source venv/bin/activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Ingest Data to Qdrant Cloud
python -m backend.ingest
```

### **Phase 3: AI Quality Evaluation (LLMOps CI)**
Validate the RAG system's faithfulness and accuracy before infrastructure rollout.
```bash
# Run Ragas metrics against ground-truth dataset
python -m backend.evaluator
```

### **Phase 4: Containerization (Docker)**
Build and optimize the production image.
```bash
# Multi-stage build for minimal image size
docker build -t bittush8789/llmops-chatbot:v1.0.0 .

# Verify locally
docker run -p 8000:8000 --env-file .env bittush8789/llmops-chatbot:v1.0.0
```

### **Phase 5: Infrastructure as Code (Terraform)**
Provision the AWS EKS Cluster and VPC Networking.
```bash
cd infra
terraform init
terraform plan -out=tfplan
terraform apply "tfplan"
```

### **Phase 6: Kubernetes Deployment (Kind/EKS)**
Deploy the modular manifests into the `technova` namespace.

**For Local Testing (Kind):**
```bash
kind create cluster --name technova-local
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**For Production (AWS EKS):**
```bash
aws eks update-kubeconfig --region us-east-2 --name technova-eks-cluster
kubectl apply -f k8s/
kubectl rollout status deployment/technova-backend -n technova
```

---

## 📊 4. Monitoring & Observability
| Tool | Access | Purpose |
| :--- | :--- | :--- |
| **Grafana** | `http://localhost:3000` | Real-time dashboards for latency & token usage. |
| **Prometheus** | `http://localhost:9090` | Time-series data scraping from pods. |
| **Langfuse** | Cloud Dashboard | Trace analysis for multi-agent "Thinking" steps. |
| **Health Check** | `/health` | Kubernetes Readiness/Liveness monitoring. |

---

## 🛡️ 5. Security & Compliance
- **Guardrails AI**: Validates LLM outputs for PII and toxicity.
- **RBAC**: Fine-grained access control implemented via `k8s/rbac.yaml`.
- **Secrets Management**: Credentials injected via K8s Secrets, never hardcoded.
- **Namespace Isolation**: All resources live in the protected `technova` namespace.

---

## 👨‍💻 Developed By
**Bittu Sharma**  
*AI and MLOps Engineer*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-lightgrey?style=flat&logo=github)](https://github.com/bittush8789)

⚖️ **Apache License 2.0**
