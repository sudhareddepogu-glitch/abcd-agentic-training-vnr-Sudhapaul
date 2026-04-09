from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
import uvicorn

from .database import engine, get_db, Base
from .models import IntakeLog
from .schemas import IntakeCreate, IntakeResponse, DailySummary, AIFeedbackResponse
from .ai_assistant import get_hydration_feedback

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Water Tracker API",
    description="Track daily water intake with AI-powered hydration feedback",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI Water Tracker API is running 💧"}


@app.post("/log-intake", response_model=IntakeResponse)
def log_intake(intake: IntakeCreate, db: Session = Depends(get_db)):
    """Log a new water intake entry."""
    log = IntakeLog(amount_ml=intake.amount_ml, note=intake.note)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@app.get("/history", response_model=list[IntakeResponse])
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    """Get recent intake history."""
    logs = (
        db.query(IntakeLog)
        .order_by(IntakeLog.logged_at.desc())
        .limit(limit)
        .all()
    )
    return logs


@app.get("/summary", response_model=DailySummary)
def get_daily_summary(target_date: Optional[date] = None, db: Session = Depends(get_db)):
    """Get total intake for a specific date (defaults to today)."""
    if target_date is None:
        target_date = date.today()

    logs = db.query(IntakeLog).filter(
        IntakeLog.logged_at >= f"{target_date} 00:00:00",
        IntakeLog.logged_at <= f"{target_date} 23:59:59",
    ).all()

    total_ml = sum(log.amount_ml for log in logs)
    return DailySummary(
        date=target_date,
        total_ml=total_ml,
        entry_count=len(logs),
        goal_ml=2500,
        percentage=round((total_ml / 2500) * 100, 1),
    )


@app.get("/ai-feedback", response_model=AIFeedbackResponse)
def ai_feedback(db: Session = Depends(get_db)):
    """Get personalized AI hydration feedback based on today's intake."""
    today = date.today()
    logs = db.query(IntakeLog).filter(
        IntakeLog.logged_at >= f"{today} 00:00:00",
        IntakeLog.logged_at <= f"{today} 23:59:59",
    ).order_by(IntakeLog.logged_at.asc()).all()

    total_ml = sum(log.amount_ml for log in logs)
    feedback = get_hydration_feedback(total_ml=total_ml, logs=logs, goal_ml=2500)
    return AIFeedbackResponse(feedback=feedback, total_ml=total_ml)


@app.delete("/log/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(IntakeLog).filter(IntakeLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log entry not found")
    db.delete(log)
    db.commit()
    return {"message": f"Log {log_id} deleted"}


