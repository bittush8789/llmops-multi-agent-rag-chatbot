# 🌌 TechNova Solutions – Enterprise Multi-Agent RAG FAQ Chatbot

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/LLM-Groq_Llama3-blueviolet.svg)](https://groq.com/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-Chroma-yellow.svg)](https://www.trychroma.com/)

## 📝 Project Overview

**TechNova Solutions** is a state-of-the-art enterprise AI platform designed to automate customer support, HR queries, IT troubleshooting, and sales intelligence. Built with a **Multi-Agent Orchestration** architecture and a deep **RAG (Retrieval-Augmented Generation)** engine, the assistant provides highly accurate, context-aware responses grounded in 60+ internal enterprise documents.

---

## ✨ Features

- **🧠 Specialized Multi-Agent System**: 10 intelligent agents working in sync to handle Sales, HR, IT, and more.
- **📚 Advanced RAG Pipeline**: Semantic search across 850+ indexed entries using ChromaDB.
- **🛡️ Hallucination Guardrails**: Dedicated Validator node ensures zero misinformation.
- **📊 Real-time Performance Analytics**: Internal dashboard to monitor agent distribution and latency.
- **🎨 Premium Enterprise UI**: Dark-themed responsive interface with real-time "Thinking" animations.

---

## 🏗️ Multi-Agent Architecture & RAG Workflow

The application uses **LangGraph** to manage the state and transitions between agents. Below is the technical breakdown of how a user query is processed end-to-end.

```mermaid
graph TD
    User([User Input]) --> Orchestrator{Orchestrator Agent}
    Orchestrator -->|Analyze Intent| Retriever[Retriever Agent]
    Retriever --> Context[(ChromaDB Vector Store)]
    Context --> Routing{Domain Specialist Routing}
    
    Routing -->|Sales| SalesAgent[Sales Agent]
    Routing -->|HR| HRAgent[HR Agent]
    Routing -->|IT| ITAgent[IT Helpdesk]
    Routing -->|General| SupportAgent[Support Agent]
    
    SalesAgent --> Validator{Validator Agent}
    HRAgent --> Validator
    ITAgent --> Validator
    SupportAgent --> Validator
    
    Validator -->|Verified Grounding| Output([Final Answer])
    Validator -->|Not Grounded| Fallback[Standard Fallback Response]
```

---

## 🚀 End-to-End Setup & Deployment Guide

Follow these steps to get the enterprise platform running from scratch on your local machine.

### **Step 1: Clone & Environment Setup**
First, clone the repository and set up a clean Python environment.
```bash
git clone https://github.com/yourusername/technova-ai-assistant.git
cd technova-ai-assistant
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **Step 2: Configuration**
Create a `.env` file in the root directory and add your Groq API Key.
```env
GROQ_API_KEY=your_groq_api_key_here
```

### **Step 3: Knowledge Base Ingestion**
This step processes the 60+ technical documents in the `docs/` folder, creates embeddings, and stores them in the ChromaDB vector database.
```bash
python backend/ingest.py
```

### **Step 4: Launch the Multi-Agent Platform**
Start the FastAPI server. This will launch the backend orchestration graph and serve the modern frontend.
```bash
python backend/main.py
```

### **Step 5: Access & Interaction**
- **Main Chat Interface**: [http://localhost:8000](http://localhost:8000)
- **Analytics Dashboard**: [http://localhost:8000/analytics](http://localhost:8000/analytics)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📸 Project Walkthrough (Step-by-Step)

### 1. Landing Page Initialization
The entry point of the application, featuring the TechNova Solutions brand and service overview.
![Homepage](photo/WhatsApp Image 2026-05-02 at 18.22.03.jpeg)

### 2. Specialized Service Exploration
Users can scroll through the services and products to understand the company's domain before interacting.
![Services Section](photo/WhatsApp Image 2026-05-02 at 18.22.03 (3).jpeg)

### 3. Activating the AI Assistant
Clicking the floating chat bubble launches the multi-agent widget.
![Products Section](photo/WhatsApp Image 2026-05-02 at 18.22.03 (4).jpeg)

### 4. Intent Detection & Agent Orchestration
When a user asks a question, the Orchestrator identifies the department and routes the query.
![Thinking State](photo/WhatsApp Image 2026-05-02 at 18.22.03 (2).jpeg)

### 5. Grounded RAG Response Delivery
The final response is delivered only after the Validator confirms the data is present in our enterprise knowledge base.
![Product Query](photo/WhatsApp Image 2026-05-02 at 18.22.03 (1).jpeg)

### 6. Support & FAQ Engagement
Integrated FAQ and Contact sections ensure users have multiple paths for resolution.
![FAQ Section](photo/WhatsApp Image 2026-05-02 at 18.22.03 (5).jpeg)

---

## 📂 Project Structure

```text
Multi-Agent-AI-FAQ-Chatbot/
├── backend/                # Core AI Logic
│   ├── agents.py           # 10 specialized agent nodes
│   ├── graph.py            # LangGraph workflow orchestration
│   ├── main.py             # FastAPI serving & API layer
│   ├── ingest.py           # Vector database management
│   └── analytics.py        # Real-time usage tracking
├── docs/                   # 60+ Enterprise documents
├── frontend/               # Modern Vanilla JS App
├── photo/                  # Walkthrough Screenshots
├── requirements.txt        # Backend dependencies
└── .env                    # Secure configuration
```

---

## 🔮 Future Roadmap

- **Multi-Modal IT Support**: Analyze screenshots for hardware troubleshooting.
- **Enterprise SSO Integration**: For secure HR and Management access.
- **Predictive Analytics**: Analyzing query trends to suggest document updates.

---

## ⚖️ License
Distributed under the **MIT License**.

<p align="center">
  Built with ❤️ for the TechNova Solutions Engineering Team
</p>

---

## 👨‍💻 Developed By

**Bittu Sharma**  
*AI and MLOps Engineer*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-lightgrey?style=flat&logo=github)](https://github.com/bittush8789)

