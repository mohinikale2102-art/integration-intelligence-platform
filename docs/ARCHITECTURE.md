# Architecture

The Streamlit frontend calls a FastAPI backend over HTTP. The backend simulates an online store, payment gateway and order management receiver. It validates webhook payloads and stores events and delivery attempts in SQLite.

The investigation service creates deterministic findings from recorded response codes and payload evidence. If a Gemini API key is configured, it can also request a natural-language explanation. The deterministic evidence and recommendations remain available if the AI request fails.

A user can manually retry a failed event. The original event remains in the database and the retry is recorded as a separate attempt.

This is a local portfolio application. A production implementation would need authentication, authorization, durable queues, rate limiting, stronger idempotency contracts, secret rotation, structured observability and deployment hardening.
