# Flaer

Clean rebrand and new product scaffold for the AIrth project.

## Structure

- `frontend/index.html` — Flaer marketing website
- `frontend/dashboard.html` — Flaer dashboard workspace
- `backend/app.py` — Flask API scaffold
- `backend/requirements.txt` — Python dependencies

## Run backend

```bash
cd flaer/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Backend runs at:

- `http://127.0.0.1:5001`
- health check: `http://127.0.0.1:5001/api/health`

## Run frontend

You can open these files directly in the browser:

- `flaer/frontend/index.html`
- `flaer/frontend/dashboard.html`

Or serve them locally:

```bash
cd flaer/frontend
python3 -m http.server 8080
```

Then open:

- `http://127.0.0.1:8080`
- `http://127.0.0.1:8080/dashboard.html`

## API endpoints

- `/api/health`
- `/api/portfolio`
- `/api/regions`
- `/api/scenarios`
- `/api/actions`

## Next recommended implementation

- Connect dashboard cards and charts to the Flask API
- Add real analytics derived from the original AIrth models
- Add authentication and organization workspaces
- Replace static SVG charts with live rendered data