import os
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_hydration_feedback(total_ml: int, logs: List, goal_ml: int = 2500) -> str:
    """
    Use LangChain + OpenAI to generate personalized hydration feedback
    based on the user's intake history for the day.
    """
    if not OPENAI_API_KEY:
        return _fallback_feedback(total_ml, goal_ml)

    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=OPENAI_API_KEY,
        )

        # Build a readable log summary for the prompt
        if logs:
            log_entries = "\n".join(
                [
                    f"  - {log.logged_at.strftime('%H:%M')}: {log.amount_ml}ml"
                    + (f" ({log.note})" if log.note else "")
                    for log in logs
                ]
            )
        else:
            log_entries = "  No entries yet today."

        remaining_ml = max(0, goal_ml - total_ml)
        percentage = round((total_ml / goal_ml) * 100, 1)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a friendly, knowledgeable hydration coach. 
Your job is to give personalized, encouraging feedback on someone's daily water intake.
Keep your response to 2-3 sentences. Be specific to their numbers. 
Use a warm, motivational tone. Occasionally use a water or nature emoji to keep it fun.
Never be preachy or negative — always find something positive to say.""",
                ),
                (
                    "human",
                    """Here is my water intake for today:

Daily goal: {goal_ml}ml
Total consumed: {total_ml}ml ({percentage}% of goal)
Remaining to reach goal: {remaining_ml}ml
Number of entries: {entry_count}

Today's log:
{log_entries}

Please give me personalized hydration feedback and a tip for the rest of the day.""",
                ),
            ]
        )

        chain = prompt | llm | StrOutputParser()

        feedback = chain.invoke(
            {
                "goal_ml": goal_ml,
                "total_ml": total_ml,
                "percentage": percentage,
                "remaining_ml": remaining_ml,
                "entry_count": len(logs),
                "log_entries": log_entries,
            }
        )

        return feedback.strip()

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return _fallback_feedback(total_ml, goal_ml)


def _fallback_feedback(total_ml: int, goal_ml: int) -> str:
    """
    Rule-based fallback feedback when OpenAI is not configured.
    Used for development/demo without an API key.
    """
    percentage = (total_ml / goal_ml) * 100
    remaining = max(0, goal_ml - total_ml)

    if total_ml == 0:
        return (
            "💧 You haven't logged any water yet today! Start with a glass of water "
            "right now to kickstart your hydration. Your body will thank you!"
        )
    elif percentage < 25:
        return (
            f"💧 You've had {total_ml}ml so far — a great start! "
            f"Try to drink {remaining}ml more throughout the day. "
            "Keep a water bottle at your desk as a reminder!"
        )
    elif percentage < 50:
        return (
            f"🌊 You're at {percentage:.0f}% of your goal — nice progress! "
            f"Just {remaining}ml to go. Consider setting a reminder every hour."
        )
    elif percentage < 75:
        return (
            f"✨ Impressive! You're {percentage:.0f}% of the way to your goal. "
            f"Only {remaining}ml left — you've got this!"
        )
    elif percentage < 100:
        return (
            f"🏆 Almost there! You're at {percentage:.0f}% with just {remaining}ml remaining. "
            "One or two more glasses and you'll hit your daily goal!"
        )
    else:
        return (
            f"🎉 Goal achieved! You've drunk {total_ml}ml today — that's {percentage:.0f}% of your target. "
            "Excellent hydration! Keep it up tomorrow too."
        )
