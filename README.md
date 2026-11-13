# Integration Intelligence Platform

An integration monitoring and troubleshooting application for support and engineering teams. The local demonstration environment simulates an online store, a payment gateway and an order management system, then records webhook deliveries and failures.

## Features

- Simulates an order and payment workflow without moving real money.
- Sends webhook-style events to a receiving service.
- Records request payloads, responses, HTTP status codes and delivery attempts.
- Reproduces missing-field, authentication, timeout and duplicate-delivery scenarios.
- Provides event monitoring, incident investigation and delivery history.
- Generates evidence-based troubleshooting guidance. Gemini explanations are optional; deterministic findings remain available without an API key.
- Supports a human-initiated retry flow and CSV event export.

## Technology

Python, FastAPI, Streamlit, SQLite, Plotly and optional Gemini API integration.

## Requirements

Python 3.11 or newer.

## Setup on Windows PowerShell

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Gemini is optional. To enable AI-generated explanations, add your key to `.env`:

```text
GEMINI_API_KEY=your_key_here
```

Do not commit `.env` or share your API key.

## Run

```powershell
python run.py
```

Open the dashboard at http://localhost:8501. FastAPI documentation is at http://127.0.0.1:8000/docs.

Stop both services with Ctrl+C in the terminal.

## Demo

1. Open **Demo Simulator**.
2. Create an order using the successful delivery scenario.
3. Repeat with **Missing required order_id**.
4. Open **Events** and inspect the failed event.
5. Open **AI Investigations** and generate an explanation.
6. Open **Retries** and retry the event.
7. Return to **Dashboard** and **Reports**.

All customer names, orders, payment references and transactions are fictional. No real payment is processed.

## Failure scenarios

| Scenario | Expected result |
|---|---|
| Successful delivery | HTTP 200 |
| Missing required field | HTTP 400 |
| Invalid authentication | HTTP 401 |
| Receiver timeout | HTTP 504 |
| Duplicate delivery | Duplicate attempt recorded without a second business action |
| Payment declined | Payment fails and no payment webhook is sent |

## Current limitations

- The business applications are local simulators, not external payment or commerce integrations.
- The application is a local portfolio demonstration, not a production deployment.
- Authentication, multi-tenancy, distributed tracing and production-grade secret management are outside this release.
- The retry demonstration corrects the known sample payload issue for the local simulator. A production retry system needs explicit mapping controls, receiver contracts and stronger idempotency guarantees.

## Security

Use fictional data only. Do not upload API keys, customer information, production payloads or private credentials to GitHub. The local SQLite database is excluded from version control.
