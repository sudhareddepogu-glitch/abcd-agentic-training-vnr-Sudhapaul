# 💧 AI Water Tracker

An intelligent hydration tracking app built with **FastAPI**, **LangChain**, **OpenAI**, and **Streamlit**.

Business Problem
Dehydration is a silent epidemic. Studies show that 75% of people are chronically dehydrated without realizing it — and dehydration reduces cognitive performance by up to 20%, affects mood, energy levels, and physical endurance.
Pain PointImpactNo real-time feedbackUsers don't know if they are on track until symptoms appearManual & tedious trackingExisting apps require precise input with no guidanceGeneric, one-size-fits-all adviceTips ignore personal patterns, timing, and daily progressNo intelligent nudgingNo system adapts coaching to what you've actually consumed
The gap: There is no lightweight, intelligent, open-source tool that combines easy water logging, live data visualization, and a personalized AI coaching layer — all in one app that a developer can run locally in minutes.

Possible Solution:

ApproachProsConsNative mobile app (iOS/Android)Great UX, push notificationsHigh dev cost, app store frictionWearable integration (Apple Watch)Passive, automaticExpensive hardware dependencySimple spreadsheet trackerZero setupNo intelligence, no visualizationFull-stack web app with AI Accessible, intelligent, extensibleRequires local setup
We evaluated multiple approaches and chose a Python-first full-stack web application because:

It is accessible from any browser with zero app install
FastAPI gives us a production-grade REST API instantly
LangChain + OpenAI enables true personalized coaching
Streamlit eliminates frontend complexity — no HTML/CSS/JS needed
The entire stack is open source and locally runnable



## Project Structure

```
water_tracker/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI app + all endpoints
│   ├── database.py      # SQLAlchemy engine + session
│   ├── models.py        # ORM model (IntakeLog)
│   ├── schemas.py       # Pydantic request/response schemas
│   └── ai_assistant.py  # LangChain + OpenAI hydration coach
├── frontend/
│   └── app.py           # Streamlit dashboard
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

### 1. Clone / open in Cursor

Open this folder in Cursor (or any editor).

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

> **Note:** The app works without an OpenAI key — it falls back to smart rule-based feedback automatically.

### 5. Start the FastAPI backend

From the project root:

```bash
uvicorn backend.main:app --reload --port 8000
```

The API will be live at: http://localhost:8000  
Interactive API docs: http://localhost:8000/docs

recording : https://drive.google.com/drive/u/0/folders/1F7Hut5W2QloScRh9Os5Qz41HWGzcxj-8

### 6. Start the Streamlit frontend

In a **second terminal** (with the venv activated):

```bash
streamlit run frontend/app.py
```

The dashboard opens at: http://localhost:8501

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/log-intake` | Log a new water entry |
| GET | `/history` | Get recent entries |
| GET | `/summary` | Today's total + goal % |
| GET | `/ai-feedback` | AI hydration coaching |
| DELETE | `/log/{id}` | Delete an entry |

### Example: Log water with curl

```bash
curl -X POST http://localhost:8000/log-intake \
  -H "Content-Type: application/json" \
  -d '{"amount_ml": 500, "note": "after run"}'
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit + Plotly |
| Backend | FastAPI + Pydantic |
| Database | SQLite + SQLAlchemy |
| AI | LangChain + OpenAI GPT-3.5 |

---

## How the AI works

1. User clicks "Get AI Feedback" in the dashboard
2. Streamlit calls `GET /ai-feedback` on the FastAPI backend
3. FastAPI fetches today's logs from SQLite
4. `ai_assistant.py` builds a LangChain prompt with the intake data
5. LangChain calls OpenAI GPT-3.5-turbo
6. Personalized coaching advice is returned and displayed

Without an OpenAI key, `_fallback_feedback()` in `ai_assistant.py` provides rule-based responses based on the percentage of the daily goal reached.

---

## Extending the project

- **Add user accounts** — FastAPI supports OAuth2/JWT out of the box
- **Weekly email report** — use APScheduler + SendGrid
- **Mobile app** — the FastAPI backend is already a REST API, connect any mobile client
- **Custom goals** — add a `users` table with per-user daily targets
- **Reminders** — add a background task that sends push notifications at set intervals
