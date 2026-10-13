# Radiogenomics Imaging Genomics Agent

A Python research-software prototype for **deterministic threshold and descriptor checks**, with two CLI implementations, a FastAPI service, batch CSV processing, an in-memory HMAC audit chain, and a browser-only demonstrator.

**Scope:** This repository does **not** extract features from medical images, parse DICOM volumes, perform PyRadiomics/IBSI calculations, analyze genomic variants, or establish imaging–genomics associations. Despite the repository name, the implemented rules are **not validated clinical thresholds**. Do not use its alerts or descriptors for diagnosis, patient triage, or treatment decisions.

## Browser demonstration

Open [`web/index.html`](web/index.html) in a modern browser. The static interface executes the same basic three worker rules as the primary Python implementation locally, displays their classifications, and exports the result as JSON. It requires no server or Python installation.

Inputs remain in the browser's current page; the interface makes no API calls and does not create cryptographic audit signatures. **Use synthetic, non-patient data only.** A GitHub Pages deployment workflow is included; deployment availability depends on the repository's Pages configuration.

## Implemented functionality

| Component | Current behavior |
| --- | --- |
| Primary Python workers (`agents/`) | Elevated alert if primary metric >25, elevated alert if secondary metric >12, critical alert if explicit critical flag, keyword alert for `DISCORDANT`, `ANOMALY`, `MUTANT`, `VIOLATION`, `FAIL`, or `REJECT` |
| Main CLI (`cli.py`) | Single case, configuration-response mock, CSV batch, audit verification, and API server |
| Main API (`agents/api.py`) | `GET /health`, `GET /metrics`, `POST /api/audit`, `POST /api/chat`, `GET /api/audit/logs`; interactive schema at `/docs` |
| Legacy research prototype (`radiogenomics_sentinel/`) | Separate CLI/API and illustrative primary >25 / secondary >10 rules |
| `enrichment.py` | Experimental generic threshold-check stubs; **not** a survivorship-plan generator or radiogenomics analysis |
| Audit trail | In-process chained HMAC-SHA256 over selected audit metadata and hashed details; does **not** persist between restarts |
| Identifier screening | Heuristic pattern checks for common identifiers on the primary Python path; **not** reliable anonymization, HIPAA certification, or a substitute for data governance |

The browser and Python rules are intentionally distinguished: only the Python primary path creates a signed in-memory audit entry. No actual external LLM integrations are implemented; `mock` is the only supported provider.

## Install and run

Requires Python 3.9 or newer. For development and tests:

```bash
git clone https://github.com/abusuraihsakhri/radiogenomics-imaging-genomics-agent.git
cd radiogenomics-imaging-genomics-agent
python -m pip install -e ".[dev]"
python -m pytest -q
```

For the primary CLI:

```bash
python cli.py audit --task-id SYNTHETIC-001 --target MODEL-A --primary 28.5 --secondary 14.2
python cli.py batch --input sample.csv --output results.csv
python cli.py verify-audit
```

To start the local API:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python cli.py serve --host 127.0.0.1 --port 8000
```

Visit `http://127.0.0.1:8000/docs`. For the separate prototype, use `python radiogenomics_sentinel_app.py --help`. The CSV batch input uses `task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor` headers. Rows with invalid numeric values or blocked identifiers in the primary CLI are skipped with a diagnostic; any output may contain supplied labels, so use synthetic identifiers.

## Docker

```bash
cp .env.example .env
# Set AUDIT_SECRET_KEY in .env to a random secret before starting
docker compose up --build
```

Compose binds port 8000 to the host loopback interface by default. The API has **no authentication**, so it must not be exposed to untrusted networks without appropriate access controls. The development audit key fallback is randomly generated per process and is not a persistent signing identity.

## Quality, privacy, and limitations

Run `python -m pytest -q` and `python -m pip check`. CI runs tests and Python compilation across supported Python versions, plus a Node-based static browser JavaScript regression check. The API is a runtime Python service and **cannot run directly on GitHub Pages**; only the standalone static demonstration is suitable for Pages. Pyodide is unnecessary for these lightweight demonstration rules, and would not enable the missing image-processing functionality.

The Python service stores dossiers and audit metadata **only in process memory**; it does not implement durable ledgers, secure user authentication, validated PHI de-identification, clinical guideline conformance, medical image segmentation, radiomic feature extraction, genomic variant association, or clinical decision support. Test and demonstration use should employ synthetic data.

## Technology and license

Python, Pydantic v2, FastAPI/Uvicorn, pytest; HTML/CSS/vanilla JavaScript for the local static interface. The browser demonstrator targets current desktop and mobile browsers supporting ES2020 features, Blob downloads, and basic DOM APIs. Licensed under the [MIT License](LICENSE).
