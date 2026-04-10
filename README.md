# 💧 AI Water Tracker

> An intelligent full-stack hydration monitoring app built with **FastAPI**, **LangChain**, **OpenAI GPT**, and **Streamlit** — log your water intake, visualize progress, and get AI-powered coaching in real time.

---

## 📋 Table of Contents

1. [Business Problem](#1-business-problem)
2. [Possible Solutions](#2-possible-solutions)
3. [Implemented Solution](#3-implemented-solution)
4. [Tech Stack](#4-tech-stack)
5. [Architecture Diagram](#5-architecture-diagram)
6. [How to Run Locally](#6-how-to-run-locally)
7. [Screenshots](#7-screenshots)
8. [Recording](#8-recording)
9. [Problems Faced & Solutions](#9-problems-faced--solutions)
10. [References & Resources](#10-references--resources)

---

## 1. 🏢 Business Problem

Dehydration is a silent epidemic. Studies show that **75% of people are chronically dehydrated** without realizing it — and dehydration reduces cognitive performance by up to 20%, affects mood, energy levels, and physical endurance.

| Pain Point | Impact |
|---|---|
| No real-time feedback | Users don't know if they are on track until symptoms appear |
| Manual & tedious tracking | Existing apps require precise input with no guidance |
| Generic, one-size-fits-all advice | Tips ignore personal patterns, timing, and daily progress |
| No intelligent nudging | No system adapts coaching to what you've actually consumed |

**The gap:** There is no lightweight, intelligent, open-source tool that combines easy water logging, live data visualization, and a personalized AI coaching layer — all in one app that a developer can run locally in minutes.

---

## 2. 💡 Possible Solutions

| Approach | Pros | Cons |
|---|---|---|
| Native mobile app (iOS/Android) | Great UX, push notifications | High dev cost, app store friction |
| Wearable integration (Apple Watch) | Passive, automatic | Expensive hardware dependency |
| Simple spreadsheet tracker | Zero setup | No intelligence, no visualization |
| **Full-stack web app with AI** ✅ | Accessible, intelligent, extensible | Requires local setup |

We evaluated multiple approaches and chose a **Python-first full-stack web application** because:
- It is accessible from any browser with zero app install
- FastAPI gives us a production-grade REST API instantly
- LangChain + OpenAI enables true personalized coaching
- Streamlit eliminates frontend complexity — no HTML/CSS/JS needed
- The entire stack is open source and locally runnable

---

## 3. ✅ Implemented Solution

The AI Water Tracker is a three-tier application:

```
User → Streamlit Dashboard → FastAPI Backend → SQLite Database
                                    ↓
                             LangChain Agent → OpenAI GPT
                                    ↓
                          Personalized Feedback → Dashboard
```

### Key Features

- **⚡ Quick-log buttons** — One click to log 250ml, 500ml, or 750ml; custom amounts with optional notes
- **📊 Live dashboard** — Gauge chart showing % of daily goal, cumulative intake timeline, weekly bar chart
- **🤖 AI hydration coach** — Click one button; LangChain builds a prompt from your day's log and GPT returns personalized advice
- **💾 Persistent history** — Every log entry saved to SQLite with timestamp; full delete support
- **🔌 REST API** — FastAPI with auto-generated Swagger docs at `localhost:8000/docs`
- **🛡️ Offline fallback** — Smart rule-based feedback when no OpenAI key is configured

### What the AI Coach Does

1. Fetches all of today's intake entries from SQLite
2. Calculates total consumed, goal percentage, remaining ml, and entry timing
3. Passes a structured prompt to LangChain's `ChatOpenAI` chain
4. GPT-3.5-turbo returns 2–3 sentences of personalized, encouraging feedback
5. Falls back to deterministic rules if the API key is missing

---

## 4. 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Frontend** | Streamlit | 1.39+ | Dashboard UI, charts, forms |
| **Charts** | Plotly | 5.24+ | Gauge, area, and bar charts |
| **Backend** | FastAPI | 0.115+ | REST API, routing, middleware |
| **Validation** | Pydantic | 2.9+ | Request/response schema validation |
| **Server** | Uvicorn | 0.30+ | ASGI server with hot reload |
| **Database** | SQLite + SQLAlchemy | 2.0+ | ORM, persistent log storage |
| **AI Orchestration** | LangChain | 0.3+ | Prompt templates, chains, parsers |
| **Language Model** | OpenAI GPT-3.5-turbo | via API | Personalized hydration coaching |
| **Environment** | python-dotenv | 1.0+ | `.env` secret management |
| **Language** | Python | 3.10+ | Full stack |

---

## 5. 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND LAYER                        │
│                                                         │
│  ┌──────────────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Streamlit Dashboard│  │ Log Form │  │ Goals/History│  │
│  │ Charts & Gauges  │  │ Quick-add│  │ Weekly Trend │  │
│  └────────┬─────────┘  └────┬─────┘  └──────┬───────┘  │
└───────────┼─────────────────┼───────────────┼───────────┘
            │   HTTP / REST   │               │
┌───────────┼─────────────────┼───────────────┼───────────┐
│           ▼   BACKEND LAYER ▼               ▼           │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │                   FastAPI App                    │   │
│  │  POST /log-intake   GET /history   GET /summary  │   │
│  │  GET /ai-feedback   DELETE /log/{id}             │   │
│  └──────┬──────────────────────────────┬────────────┘   │
│         │  Pydantic Validation         │ AI Trigger     │
└─────────┼──────────────────────────────┼────────────────┘
          │                              │
┌─────────▼──────────┐   ┌──────────────▼────────────────┐
│   DATA LAYER       │   │         AI LAYER               │
│                    │   │                                │
│  SQLite Database   │   │  LangChain ChatPromptTemplate  │
│  intake_logs table │   │         ↓                      │
│  id, amount_ml,    │   │  ChatOpenAI (GPT-3.5-turbo)    │
│  note, logged_at   │   │         ↓                      │
│                    │   │  StrOutputParser → feedback    │
└────────────────────┘   └────────────────────────────────┘
```

### Data Flow

```
1. User clicks "Log Water" in Streamlit
2. Streamlit POST /log-intake → FastAPI
3. FastAPI validates with Pydantic → writes to SQLite
4. User clicks "Get AI Feedback"
5. FastAPI reads today's logs from SQLite
6. LangChain builds structured prompt with intake data
7. OpenAI GPT-3.5-turbo returns personalized coaching
8. Feedback displayed back in Streamlit dashboard
```

---

## 6. 🚀 How to Run Locally

### Prerequisites

- Python 3.10 or higher — [Download](https://www.python.org/downloads/)
- An OpenAI API key (optional) — [Get one here](https://platform.openai.com/api-keys)
- Git (optional)

---

### Step 1 — Get the code

Unzip the project or clone it, then open the folder in your terminal:

```bash
cd water_tracker
```

Confirm you are in the right folder — you should see these files:

```
water_tracker/
├── backend/
├── frontend/
├── requirements.txt
├── .env.example
└── README.md
```

---

### Step 2 — Create a virtual environment

```bash
# Create
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows (PowerShell)
venv\Scripts\activate
```

You will see `(venv)` appear in your terminal prompt.

---

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

> **Windows + Python 3.13 note:** If you get a numpy build error, run this instead:
> ```bash
> pip install fastapi uvicorn[standard] sqlalchemy pydantic python-dotenv langchain langchain-openai openai "streamlit>=1.39" requests pandas plotly
> ```

---

### Step 4 — Configure environment variables

```bash
# Copy the template
cp .env.example .env
```

Open `.env` and add your OpenAI key:

```env
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=sqlite:///./water_tracker.db
```

> ⚠️ **No OpenAI key?** The app still works. It uses smart rule-based feedback as a fallback — no API call needed.

---

### Step 5 — Start the FastAPI backend

Open **Terminal 1** (make sure `(venv)` is active):

```bash
# Windows PowerShell
$env:PYTHONPATH = "."; uvicorn backend.main:app --reload --port 8000

# macOS / Linux
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000
```

✅ You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Interactive API docs available at: **http://localhost:8000/docs**

---

### Step 6 — Start the Streamlit frontend

Open **Terminal 2** (activate venv again, navigate to project root):

```bash
streamlit run frontend/app.py
```

✅ You should see:
```
  Local URL: http://localhost:8501
```

Your browser will open automatically. If it doesn't, visit **http://localhost:8501**

---

### Running both — quick reference

| Terminal | Command | URL |
|---|---|---|
| Terminal 1 (backend) | `$env:PYTHONPATH="."; uvicorn backend.main:app --reload --port 8000` | http://localhost:8000/docs |
| Terminal 2 (frontend) | `streamlit run frontend/app.py` | http://localhost:8501 |

> Keep both terminals open while using the app. Closing either will stop that service.

---

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/log-intake` | Log a new water entry |
| `GET` | `/history` | Get recent entries (default: last 50) |
| `GET` | `/summary` | Today's total ml + goal percentage |
| `GET` | `/ai-feedback` | Get AI coaching based on today's log |
| `DELETE` | `/log/{id}` | Delete a specific entry by ID |

**Example curl:**
```bash
curl -X POST http://localhost:8000/log-intake \
  -H "Content-Type: application/json" \
  -d '{"amount_ml": 500, "note": "after workout"}'
```

---

## 7. 📸 Screenshots

### Dashboard Overview
![Dashboard](screenshots/dashboard.png)
> Main dashboard showing today's progress gauge, AI coach panel, metric cards, and quick-log sidebar

### Weekly Progress Chart
![Weekly Chart](screenshots/weekly_chart.png)
> Bar chart showing daily intake for the past 7 days — green bars = goal met, blue = in progress

### AI Hydration Feedback
![AI Feedback](screenshots/ai_feedback.png)
> Personalized coaching from LangChain + GPT based on the day's actual intake log

### FastAPI Swagger Docs
![API Docs](screenshots/api_docs.png)
> Auto-generated interactive API documentation at localhost:8000/docs

### Log History Table
![Log History](screenshots/log_history.png)
> Tabular view of recent entries with timestamp, amount, glasses equivalent, and delete option

---

## 8. 🎥 Recording

> 📹 **Demo video:** [Add your Loom / YouTube link here]

The recording covers:
- Project overview and architecture walkthrough (0:00 – 1:30)
- Starting the backend and frontend locally (1:30 – 3:00)
- Logging water with quick-add buttons and custom input (3:00 – 4:30)
- Viewing the gauge chart and weekly bar chart (4:30 – 6:00)
- Clicking "Get AI Feedback" and seeing the LangChain + GPT response (6:00 – 7:30)
- Exploring the Swagger API docs (7:30 – 8:30)

---

## 9. 🐛 Problems Faced & Solutions

### Problem 1 — `ModuleNotFoundError: No module named 'backend'`

**Symptom:** Uvicorn starts but crashes immediately with a module import error.

**Cause:** Python cannot find the `backend` package because the working directory is not set correctly. Python needs to know to look in the current folder for the `backend/` subdirectory.

**Solution:**
```bash
# Windows PowerShell — set PYTHONPATH before running
$env:PYTHONPATH = "."; uvicorn backend.main:app --reload --port 8000

# macOS / Linux
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000
```

---

### Problem 2 — `ModuleNotFoundError: No module named 'langchain.prompts'`

**Symptom:** Backend crashes on startup with a LangChain import error.

**Cause:** LangChain restructured its package in v0.3+. `ChatPromptTemplate` and `StrOutputParser` moved from `langchain.*` to `langchain_core.*`.

**Solution:** Update the imports in `backend/ai_assistant.py`:

```python
# ❌ Old (broken in langchain 0.3+)
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# ✅ New (correct)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
```

Then upgrade the packages:
```bash
pip install langchain-core langchain-openai --upgrade
```

---

### Problem 3 — `numpy` build failure on Python 3.13 (Windows)

**Symptom:** `pip install -r requirements.txt` fails with a Meson/compiler error for numpy 1.26.4.

**Cause:** numpy 1.26.x does not support Python 3.13. It requires a C compiler to build from source, and no pre-built wheel exists for this Python version.

**Solution:** Skip the pinned requirements file and let pip resolve compatible versions:

```bash
pip install fastapi uvicorn[standard] sqlalchemy pydantic python-dotenv \
    langchain langchain-openai openai "streamlit>=1.39" requests pandas plotly
```

pip will automatically select numpy 2.x which has pre-built wheels for Python 3.13.

---

### Problem 4 — `streamlit: command not found` after installing

**Symptom:** Running `streamlit run frontend/app.py` gives "command not recognized".

**Cause:** The virtual environment was not activated in the current terminal, or Streamlit was installed in a different Python environment.

**Solution:** Always activate the venv first:
```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```
Then verify: `python -m streamlit --version` should print a version number.

---

### Problem 5 — `File does not exist: frontend\app.py`

**Symptom:** Streamlit cannot find `app.py`.

**Cause:** The terminal is in the wrong directory — either one level above or below the project root.

**Solution:**
```bash
# Check current directory
ls   # (Windows: dir)

# You should see: backend/  frontend/  requirements.txt  README.md
# If you see another water_tracker/ folder, go one level deeper:
cd water_tracker
```

---

### Problem 6 — Backend runs but Streamlit shows "Cannot connect to backend"

**Symptom:** Dashboard loads but every API call shows a connection error banner.

**Cause:** The FastAPI backend is not running, or it crashed after starting.

**Solution:** Open a separate terminal tab, activate the venv, and start the backend. Both services must run simultaneously — one terminal each.

---

## 10. 📚 References & Resources

### Official Documentation

| Resource | URL |
|---|---|
| FastAPI Docs | https://fastapi.tiangolo.com |
| Streamlit Docs | https://docs.streamlit.io |
| LangChain Docs | https://python.langchain.com/docs |
| OpenAI API Reference | https://platform.openai.com/docs |
| SQLAlchemy ORM | https://docs.sqlalchemy.org |
| Pydantic v2 | https://docs.pydantic.dev |
| Plotly Python | https://plotly.com/python |
| Uvicorn | https://www.uvicorn.org |

### Key Concepts Used

| Concept | Resource |
|---|---|
| FastAPI dependency injection (`Depends`) | https://fastapi.tiangolo.com/tutorial/dependencies |
| LangChain LCEL (pipe syntax) | https://python.langchain.com/docs/expression_language |
| SQLAlchemy declarative base | https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html |
| Streamlit session state | https://docs.streamlit.io/library/api-reference/session-state |
| Pydantic field validators | https://docs.pydantic.dev/latest/concepts/validators |

### Tools & Utilities

| Tool | Purpose |
|---|---|
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Load `.env` variables into `os.environ` |
| [Swagger UI](http://localhost:8000/docs) | Auto-generated interactive API docs (built into FastAPI) |
| [DB Browser for SQLite](https://sqlitebrowser.org/) | Visual SQLite database explorer |
| [Postman](https://www.postman.com/) | API testing and request building |

---

## 📁 Project Structure

```
water_tracker/
├── backend/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI app + all endpoints
│   ├── database.py          # SQLAlchemy engine + session factory
│   ├── models.py            # ORM model — IntakeLog table
│   ├── schemas.py           # Pydantic request/response schemas
│   └── ai_assistant.py      # LangChain + OpenAI hydration coach
├── frontend/
│   └── app.py               # Streamlit dashboard (full UI)
├── requirements.txt         # All Python dependencies
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
  Built with 💧 by the AI Water Tracker team
  <br/>
  <em>Stay Hydrated. Stay Smart.</em>
</div>



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
