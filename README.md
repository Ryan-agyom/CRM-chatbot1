# Chatbot + CRM Monorepo

This repo now uses:

- `frontend/` for the Vite UI
- `backend1/` for the Python FastAPI backend

The old Node backend has been replaced by the Python service.

## Project Structure

```text
project-root/
|-- frontend/
|-- backend1/
|-- docs/
|-- docker/
|-- .env
|-- .env.example
|-- docker-compose.yml
`-- README.md
```

## Backend Features

The FastAPI backend exposes:

- `POST /api/chat`
- `GET /api/health`
- `GET /api/crm/overview`
- `GET /api/crm/leads`
- `POST /api/crm/leads`
- `POST /api/crm/leads/qualify`
- `POST /api/crm/appointments`
- `GET /api/crm/campaigns`
- `POST /api/crm/campaigns`
- `GET /api/crm/support/tickets`
- `POST /api/crm/support/tickets`
- `GET /api/crm/analytics/insights`
- `POST /api/crm/dev/seed`

It also supports deterministic CRM analytics over the CSV datasets in `backend1/data/`, including join-style questions such as company-level ticket analysis.

## Environment Setup

Copy `.env.example` to `.env` if needed, then set:

```env
PORT=8000
FRONTEND_URL=http://localhost:5173
VITE_API_URL=http://localhost:8000/api
AI_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_API_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

## Run Locally

Install backend dependencies:

```bash
cd backend1
pip install -r requirements.txt
```

Start the backend:

```bash
cd backend1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Start the frontend in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/api/health`

## Synthetic CRM Data

You can regenerate the CSV datasets with:

```bash
cd backend1
python scripts/generate_synthetic_data.py
```

Or reseed through the API:

```http
POST /api/crm/dev/seed
Content-Type: application/json
```

Example body:

```json
{
  "leads": 40,
  "campaigns": 8,
  "tickets": 20
}
```
