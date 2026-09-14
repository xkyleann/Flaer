# Flaer workspace

This repository contains the Flaer product: a decision workspace for European data-centre portfolios, reporting evidence, and site-selection scenarios.

The active application is in [`flaer/`](./flaer). The older [`AIrth-main/`](./AIrth-main) folder is retained as a historical research prototype and is not the production application.

## Product status

- The map contains 15 European metro-level reference locations.
- Location data is not operational telemetry.
- Performance, carbon, PUE, WUE, renewable, forecast, benchmark, and report figures must be connected to authorised sources or clearly shown as illustrative/scenario data.
- The application supports account registration and authenticated dashboard access.

## Run locally

See [the Flaer README](./flaer/README.md) for backend and frontend setup.

```bash
./start.sh
```

The frontend runs at `http://localhost:5173` and the API at `http://localhost:8000`.

## Documentation

- [Change log](./CHANGELOG.md) — dated record of product and engineering changes.
- [Deployment guide](./DEPLOYMENT.md) — Cloudflare Pages and Render deployment.
- [Data sources](./DATA_SOURCES.md) — source and data-status guidance.
- [Product positioning](./PRODUCT_POSITIONING.md) — intended product scope.
- [Testing guide](./TESTING_GUIDE.md) — release checks.

## Repository layout

```text
flaer/
  backend/            FastAPI API, authentication, database models, and tests
  frontend-svelte/    Svelte/Vite website and dashboard
AIrth-main/           Historical research prototype (not deployed)
```

## Before production release

1. Deploy the API and frontend with production environment variables.
2. Restrict the Mapbox token to approved domains.
3. Connect verified operational sources before presenting performance claims.
4. Run the backend test suite and frontend production build.
5. Review [CHANGELOG.md](./CHANGELOG.md) and the deployment guide.
