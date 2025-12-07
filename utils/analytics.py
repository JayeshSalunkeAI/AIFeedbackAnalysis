# utils/analytics.py

import pandas as pd
from datetime import datetime, timedelta


def get_rating_distribution(df):
    """Get count of each rating (1-5)"""
    if len(df) == 0:
        return pd.Series()
    return df['rating'].value_counts().sort_index()


def get_sentiment_breakdown(df):
    """Get count of each sentiment type"""
    if len(df) == 0:
        return pd.Series()
    return df['sentiment'].value_counts()


def calculate_stats(df):
    """Calculate key statistics"""
    if len(df) == 0:
        return {
            'total': 0,
            'avg_rating': 0,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
        }

    return {
        'total': len(df),
        'avg_rating': df['rating'].mean(),
        'positive_count': len(df[df['sentiment'] == 'positive']),
        'negative_count': len(df[df['sentiment'] == 'negative']),
        'neutral_count': len(df[df['sentiment'] == 'neutral']),
    }


def get_recent_feedback(df, n=10):
    """Get most recent n feedback items"""
    if len(df) == 0:
        return pd.DataFrame()
    return df.head(n)


def get_feedback_by_date_range(df, days=30):
    """Get feedback from last N days"""
    if len(df) == 0:
        return pd.DataFrame()
    
    df['created_at'] = pd.to_datetime(df['created_at'])
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    return df[df['created_at'] >= cutoff_date]


def get_category_breakdown(df):
    """Get feedback count by category"""
    if len(df) == 0:
        return pd.Series()
    return df['category'].value_counts()


def calculate_satisfaction_rate(df):
    """Calculate satisfaction (4-5 stars) percentage"""
    if len(df) == 0:
        return 0
    satisfied = len(df[df['rating'] >= 4])
    return (satisfied / len(df)) * 100


def get_top_categories(df, n=5):
    """Get top N categories by feedback count"""
    if len(df) == 0:
        return []
    return df['category'].value_counts().head(n).to_dict()


def get_average_rating_by_category(df):
    """Get average rating per category"""
    if len(df) == 0:
        return pd.Series()
    return df.groupby('category')['rating'].mean()


def get_sentiment_by_rating(df):
    """Analyze sentiment distribution by rating"""
    if len(df) == 0:
        return pd.DataFrame()
    return pd.crosstab(df['rating'], df['sentiment'])