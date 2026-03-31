# Trend Buddy Frontend

This frontend has been replaced with a Vue 3 application modeled on the structure of the referenced
`algotrader` frontend: `App.vue`, a router-driven shell, Pinia stores, Naive UI controls, and a
lightweight-charts telemetry panel.

## What It Does

- Polls the Go API root endpoint and `/health`
- Shows rolling latency data in a terminal-style chart
- Keeps endpoint selection and refresh interval in local storage
- Presents recent probe history and structured response payloads

## Running

Prefer the repo's Docker workflow from the project root:

```bash
docker compose up --build frontend
```

The app listens on `5173` and targets `VITE_API_BASE_URL`, defaulting to `http://localhost:8081`.
