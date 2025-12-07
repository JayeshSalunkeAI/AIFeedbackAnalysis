# utils/database.py

import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = os.path.join("data", "feedback.db")


def init_db():
    """Initialize SQLite database with feedback table"""
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            email TEXT,
            category TEXT NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            message TEXT NOT NULL,
            sentiment TEXT,
            summary TEXT,
            ai_response TEXT,
            recommendations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def add_feedback(user_name, email, category, rating, message, sentiment, ai_response, summary, recommendations=None):
    """Add feedback record to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO feedback
        (user_name, email, category, rating, message, sentiment, summary, ai_response, recommendations, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_name,
            email,
            category,
            rating,
            message,
            sentiment,
            summary,
            ai_response,
            recommendations,
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def get_all_feedback():
    """Retrieve all feedback records ordered by newest first"""
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            "SELECT * FROM feedback ORDER BY created_at DESC",
            conn,
        )
        conn.close()
        return df if len(df) > 0 else pd.DataFrame()
    except Exception as e:
        print(f"Database error: {e}")
        return pd.DataFrame()


def get_feedback_by_category(category):
    """Get feedback filtered by category"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM feedback WHERE category = ? ORDER BY created_at DESC",
        conn,
        params=(category,),
    )
    conn.close()
    return df if len(df) > 0 else pd.DataFrame()


def get_feedback_by_sentiment(sentiment):
    """Get feedback filtered by sentiment"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM feedback WHERE sentiment = ? ORDER BY created_at DESC",
        conn,
        params=(sentiment,),
    )
    conn.close()
    return df if len(df) > 0 else pd.DataFrame()


def get_feedback_by_rating_range(min_rating, max_rating):
    """Get feedback within rating range"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM feedback WHERE rating >= ? AND rating <= ? ORDER BY created_at DESC",
        conn,
        params=(min_rating, max_rating),
    )
    conn.close()
    return df if len(df) > 0 else pd.DataFrame()