# Trend Buddy

Trend Buddy is an open-source trading companion for market analysis, backtesting, portfolio tracking, and automated execution workflows.

## Current Spike

The repository now includes a lightweight backend and dashboard spike:

- **FastAPI** powers typed REST and realtime endpoints.
- **SvelteKit** provides the dashboard shell with SSR plus client-side interactivity.
- **Pydantic contracts** live in `packages/shared/contracts` and back both API routes and UI data shapes.

## API Surface

- `GET /health` returns an application health probe.
- `GET /portfolio/summary` returns a typed portfolio overview payload for the dashboard.
- `GET /market-data/snapshot` returns a typed market snapshot payload.
- `WS /ws/market-data` streams live market ticks for the UI pulse widget.
- `GET /docs` exposes the generated OpenAPI documentation.

## Local Development

1. Create the Python environment and install backend dependencies:

```bash
uv sync
```

2. Install frontend dependencies:

```bash
npm --prefix apps/frontend install
```

3. Start the API:

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

4. In a second terminal, start the frontend:

```bash
npm --prefix apps/frontend run dev -- --host 0.0.0.0 --port 5173
```

The frontend expects the browser-facing API at `PUBLIC_API_BASE_URL`, which defaults to `http://localhost:3000`.

## Testing

Run the API smoke tests with:

```bash
uv run unittest tests.test_api_spike
```

## Docker

Build the API image and run it with:

```bash
docker build -t trend-buddy .
docker run --rm -p 3000:3000 trend-buddy
```

## Docker Compose

Run the API and frontend together for local development with:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:3000` and the SvelteKit dashboard at `http://localhost:5173`.

Compose notes:

- The API image installs Python dependencies at build time and runs the app with live reload.
- The frontend image installs Node dependencies at build time and uses a named volume for `node_modules`.
- Source code is bind-mounted so edits on the host are reflected inside the running containers.
