# Radiogenomics Imaging Genomics Agent

> **Domain:** Diagnostic Radiology & Medical Imaging AI
> **Reference Guidelines & Standards:** `American College of Radiology (ACR) RADS & Fleischner Society`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Radiogenomics Imaging Genomics Agent** is an advanced analytical and computational platform implementing 3D PyRadiomics texture GLCM & EGFR/IDH1 driver mutation association agent. It provides multi-worker evaluation, cryptographic audit trails, and zero-PHI outbound protection for medical imaging analysis workflows.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.
- **Multi-Worker Architecture**: InvariantQC, Safety Escalation, and Protocol Conformance workers.
- **Batch Processing**: CSV-based batch evaluation with error handling and reporting.

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/radiogenomics-imaging-genomics-agent.git
cd radiogenomics-imaging-genomics-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# Optional: Set audit secret key (recommended for production)
export AUDIT_SECRET_KEY="your-secure-random-key-here"
```

---

## 💻 CLI Quickstart & Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target TARGET-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch CSV Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch FastAPI REST Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Parameter | Description | Default |
|:----------|:------------|:--------|
| `--task-id` | Unique task/case identifier | `TASK-2026-001` |
| `--target` | Entity or target identifier | `KEY-TARGET-01` |
| `--primary` | Primary domain measurement (float) | `28.5` |
| `--secondary` | Secondary kinetic/confidence score (float) | `14.2` |
| `--critical` | Emergency escalation flag | `False` |
| `--status` | Status code or phenotype descriptor | `DISCORDANT` |

### Input Data Schema (CSV)

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Parameter / observation metric | Required |
| `target_identifier` | Parameter / observation metric | Required |
| `primary_metric` | Primary measurement value (float) | Required |
| `secondary_metric` | Secondary measurement value (float) | Optional |
| `is_critical_flag` | Emergency escalation flag (true/false) | Optional |
| `status_descriptor` | Status code or phenotype descriptor | Optional |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).
* **Security Headers:** All API responses include X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, and HSTS headers.
* **Path Traversal Protection:** Batch processing validates file paths to prevent directory traversal attacks.

### Environment Variables

| Variable | Description | Required |
|:---------|:------------|:---------|
| `AUDIT_SECRET_KEY` | Secret key for HMAC-SHA256 audit trail signing | Recommended |
| `MODEL_PROVIDER` | LLM provider (mock, ollama, claude, openai) | No (default: mock) |

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py --tasks 1000 --concurrency 8
```

---

## 🐳 Container Deployment

### Docker
```bash
# Build and run
docker build -t radiogenomics-imaging-genomics-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY="your-secret-key" radiogenomics-imaging-genomics-agent
```

### Docker Compose
```bash
# Create .env file with required variables
echo "AUDIT_SECRET_KEY=your-secure-random-key-here" > .env

# Start services
docker-compose up -d
```

---

## 📁 Project Structure

```
radiogenomics-imaging-genomics-agent/
├── agents/                      # Core agent modules
│   ├── __init__.py
│   ├── api.py                   # FastAPI REST server
│   ├── base.py                  # Security, PHI guard, audit trail
│   ├── learning.py              # Bayesian calibration engine
│   ├── llm_factory.py           # LLM provider factory
│   ├── metrics.py               # Prometheus metrics exporter
│   ├── models.py                # Pydantic data models
│   ├── streamer.py              # WebSocket telemetry streamer
│   ├── supervisor.py            # Supervisor orchestrator
│   └── workers.py               # Specialized worker agents
├── radiogenomics_sentinel/      # Frontier domain modules
│   ├── __init__.py
│   ├── agents.py                # Sub-agents and coordinator
│   ├── cli.py                   # Frontier CLI
│   ├── engine.py                # Core algorithmic engine
│   ├── models.py                # Frontier data models
│   └── server.py                # Frontier FastAPI server
├── tests/                       # Test suite
│   ├── test_enrichment.py
│   ├── test_radiogenomics_imaging_genomics_agent.py
│   └── test_radiogenomics_sentinel.py
├── web/                         # Web interface
│   └── index.html
├── cli.py                       # Main CLI entry point
├── radiogenomics_sentinel_app.py  # Frontier CLI entry point
├── simulator.py                 # High-throughput simulator
├── enrichment.py                # Enrichment feature suite
├── sample.csv                   # Sample batch input
├── sample_payload.json          # Sample API payload
├── benchmark_dataset.json       # Golden benchmark test cases
├── pyproject.toml               # Project configuration
├── Dockerfile                   # Docker build config
├── docker-compose.yml           # Docker Compose config
└── .gitignore                   # Git ignore rules
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
