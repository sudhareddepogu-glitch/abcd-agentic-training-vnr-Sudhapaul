import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta

# ── Config ────────────────────────────────────────────────────────────────────
API_BASE = "http://localhost:8000"
DAILY_GOAL_ML = 2500

st.set_page_config(
    page_title="AI Water Tracker 💧",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def api_get(path: str, params: dict = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the backend. Is the FastAPI server running on port 8000?")
        return None
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def api_post(path: str, data: dict):
    try:
        r = requests.post(f"{API_BASE}{path}", json=data, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the backend.")
        return None
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def api_delete(path: str):
    try:
        r = requests.delete(f"{API_BASE}{path}", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Delete error: {e}")
        return None


def ml_to_glasses(ml: int) -> float:
    return round(ml / 250, 1)


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("💧 Water Tracker")
    st.markdown("---")

    st.subheader("Log Water Intake")

    # Quick-add buttons
    st.caption("Quick add:")
    col1, col2, col3 = st.columns(3)
    quick_add = None
    with col1:
        if st.button("🥤 250ml"):
            quick_add = 250
    with col2:
        if st.button("🍶 500ml"):
            quick_add = 500
    with col3:
        if st.button("🫙 750ml"):
            quick_add = 750

    st.markdown("")

    # Custom amount form
    with st.form("log_form", clear_on_submit=True):
        amount = st.number_input(
            "Custom amount (ml)",
            min_value=50,
            max_value=2000,
            value=quick_add if quick_add else 250,
            step=50,
        )
        note = st.text_input("Note (optional)", placeholder="e.g. after workout")
        submitted = st.form_submit_button("➕ Log Water", use_container_width=True)

        if submitted or quick_add:
            log_amount = quick_add if quick_add and not submitted else amount
            result = api_post("/log-intake", {"amount_ml": log_amount, "note": note or None})
            if result:
                st.success(f"✅ Logged {log_amount}ml!")
                st.rerun()

    st.markdown("---")
    st.caption("Built with FastAPI · LangChain · Streamlit")


# ── Main Page ─────────────────────────────────────────────────────────────────

st.title("💧 AI Hydration Dashboard")

summary = api_get("/summary")
history = api_get("/history", {"limit": 100})

if summary is None:
    st.stop()

# ── Metric Cards ──────────────────────────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)

total_ml = summary["total_ml"]
percentage = summary["percentage"]
remaining = max(0, DAILY_GOAL_ML - total_ml)

col1.metric("💧 Today's Intake", f"{total_ml} ml", f"{ml_to_glasses(total_ml)} glasses")
col2.metric("🎯 Daily Goal", f"{DAILY_GOAL_ML} ml", f"{percentage}% reached")
col3.metric("📉 Remaining", f"{remaining} ml", f"{ml_to_glasses(remaining)} glasses to go")
col4.metric("📝 Entries Today", summary["entry_count"], "log entries")

st.markdown("---")

# ── Progress Bar ──────────────────────────────────────────────────────────────

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Today's Progress")

    progress = min(percentage / 100, 1.0)
    bar_color = "#2196F3" if percentage < 100 else "#4CAF50"

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=total_ml,
        delta={"reference": DAILY_GOAL_ML, "valueformat": ".0f", "suffix": "ml"},
        number={"suffix": " ml", "font": {"size": 36}},
        gauge={
            "axis": {"range": [0, DAILY_GOAL_ML], "ticksuffix": "ml"},
            "bar": {"color": bar_color},
            "steps": [
                {"range": [0, DAILY_GOAL_ML * 0.33], "color": "#E3F2FD"},
                {"range": [DAILY_GOAL_ML * 0.33, DAILY_GOAL_ML * 0.66], "color": "#BBDEFB"},
                {"range": [DAILY_GOAL_ML * 0.66, DAILY_GOAL_ML], "color": "#90CAF9"},
            ],
            "threshold": {
                "line": {"color": "#1565C0", "width": 3},
                "thickness": 0.75,
                "value": DAILY_GOAL_ML,
            },
        },
        title={"text": f"Daily Goal: {DAILY_GOAL_ML}ml"},
    ))
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)


# ── AI Feedback ────────────────────────────────────────────────────────────────

with right_col:
    st.subheader("🤖 AI Hydration Coach")
    if st.button("✨ Get AI Feedback", use_container_width=True):
        with st.spinner("Analyzing your hydration..."):
            ai_data = api_get("/ai-feedback")
            if ai_data:
                st.session_state["ai_feedback"] = ai_data["feedback"]

    if "ai_feedback" in st.session_state:
        st.info(st.session_state["ai_feedback"])
    else:
        st.caption("Click the button above to get personalized feedback from your AI hydration coach.")

    st.markdown("---")
    st.caption("**Hydration tips:**")
    st.caption("• 8 glasses (2L) per day is the classic target")
    st.caption("• Drink a glass first thing in the morning")
    st.caption("• Add one glass before each meal")
    st.caption("• Increase intake when exercising or in hot weather")


st.markdown("---")

# ── Intake Chart ──────────────────────────────────────────────────────────────

st.subheader("📊 Today's Intake Timeline")

if history:
    df = pd.DataFrame(history)
    df["logged_at"] = pd.to_datetime(df["logged_at"])

    today = date.today()
    df_today = df[df["logged_at"].dt.date == today].copy()

    if not df_today.empty:
        df_today = df_today.sort_values("logged_at")
        df_today["cumulative_ml"] = df_today["amount_ml"].cumsum()
        df_today["time_str"] = df_today["logged_at"].dt.strftime("%H:%M")

        fig_line = px.area(
            df_today,
            x="time_str",
            y="cumulative_ml",
            labels={"time_str": "Time", "cumulative_ml": "Cumulative Intake (ml)"},
            color_discrete_sequence=["#2196F3"],
        )
        fig_line.add_hline(
            y=DAILY_GOAL_ML,
            line_dash="dash",
            line_color="#1565C0",
            annotation_text="Daily goal",
            annotation_position="top right",
        )
        fig_line.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No entries for today yet. Log your first glass of water! 💧")
else:
    st.info("No history available. Start logging your water intake!")


# ── Recent Entries Table ───────────────────────────────────────────────────────

st.subheader("📋 Recent Entries")

if history:
    df_display = pd.DataFrame(history[:20])
    df_display["logged_at"] = pd.to_datetime(df_display["logged_at"]).dt.strftime("%Y-%m-%d %H:%M")
    df_display["glasses"] = (df_display["amount_ml"] / 250).round(1)
    df_display = df_display.rename(columns={
        "id": "ID",
        "amount_ml": "Amount (ml)",
        "glasses": "Glasses",
        "note": "Note",
        "logged_at": "Logged At",
    })
    df_display["Note"] = df_display["Note"].fillna("—")

    st.dataframe(
        df_display[["ID", "Logged At", "Amount (ml)", "Glasses", "Note"]],
        use_container_width=True,
        hide_index=True,
    )

    # Delete entry
    with st.expander("🗑️ Delete an entry"):
        entry_ids = [row["id"] for row in history[:20]]
        del_id = st.selectbox("Select entry ID to delete", entry_ids)
        if st.button("Delete entry", type="secondary"):
            result = api_delete(f"/log/{del_id}")
            if result:
                st.success(f"Entry {del_id} deleted.")
                st.rerun()
else:
    st.info("No entries yet.")


# ── Weekly Bar Chart ───────────────────────────────────────────────────────────

st.subheader("📅 This Week's Hydration")

if history:
    df_all = pd.DataFrame(history)
    df_all["logged_at"] = pd.to_datetime(df_all["logged_at"])
    df_all["day"] = df_all["logged_at"].dt.date

    week_ago = date.today() - timedelta(days=6)
    df_week = df_all[df_all["day"] >= week_ago]

    if not df_week.empty:
        daily_totals = df_week.groupby("day")["amount_ml"].sum().reset_index()
        daily_totals.columns = ["Date", "Total (ml)"]
        daily_totals["Date"] = daily_totals["Date"].astype(str)
        daily_totals["Goal Met"] = daily_totals["Total (ml)"] >= DAILY_GOAL_ML

        fig_bar = px.bar(
            daily_totals,
            x="Date",
            y="Total (ml)",
            color="Goal Met",
            color_discrete_map={True: "#4CAF50", False: "#2196F3"},
            labels={"Total (ml)": "Water Intake (ml)"},
        )
        fig_bar.add_hline(
            y=DAILY_GOAL_ML,
            line_dash="dash",
            line_color="#1565C0",
            annotation_text="Daily goal",
        )
        fig_bar.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No data for the past week yet.")
