import streamlit as st
import os
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.database import init_db, get_all_feedback, add_feedback
from utils.perplexity_client import (
    analyze_review_sentiment,
    generate_ai_response,
    generate_summary,
    generate_recommendations,
)
from utils.analytics import (
    get_rating_distribution,
    get_sentiment_breakdown,
    calculate_stats,
    get_recent_feedback,
)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="AI Feedback System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database
init_db()

# ═══════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD (USER-FACING)
# ═══════════════════════════════════════════════════════════════════════════

def render_user_dashboard():
    """User-facing dashboard for submitting feedback"""
    st.title("⭐ Share Your Feedback")
    st.markdown(
        "We'd love to hear from you! Please share your experience below."
    )

    with st.form("feedback_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            user_name = st.text_input(
                "Your Name",
                placeholder="John Doe",
                help="Enter your full name",
            )

        with col2:
            user_email = st.text_input(
                "Email (Optional)",
                placeholder="john@example.com",
                help="We may use this to follow up",
            )

        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox(
                "Feedback Category",
                [
                    "General Feedback",
                    "Feature Request",
                    "Bug Report",
                    "Performance",
                    "UI/UX",
                    "Documentation",
                    "Customer Service",
                    "Other",
                ],
                help="What type of feedback is this?",
            )

        with col2:
            rating = st.slider(
                "Rate Your Experience",
                1,
                5,
                3,
                help="1 = Poor, 5 = Excellent",
            )

        # Show rating with emoji
        emoji_map = {1: "😞", 2: "😕", 3: "😐", 4: "🙂", 5: "😄"}
        st.markdown(f"**Your Rating:** {emoji_map[rating]} {rating}/5 Stars")

        message = st.text_area(
            "Your Feedback",
            placeholder="Tell us what you think... (min 10 characters)",
            height=150,
            help="Please be specific and constructive",
        )

        submitted = st.form_submit_button(
            "✉️ Submit Feedback",
            use_container_width=True,
            type="primary",
        )

        if submitted:
            # Validation
            if not user_name or not message:
                st.error("❌ Please fill in all required fields (Name & Feedback).")
            elif len(message) < 10:
                st.error("❌ Feedback must be at least 10 characters long.")
            else:
                with st.spinner("🤖 AI is processing your feedback..."):
                    try:
                        # Generate AI analysis
                        sentiment = analyze_review_sentiment(message)
                        ai_response = generate_ai_response(message, category)
                        summary = generate_summary(message)

                        # Store in database
                        add_feedback(
                            user_name=user_name,
                            email=user_email,
                            category=category,
                            rating=rating,
                            message=message,
                            sentiment=sentiment,
                            ai_response=ai_response,
                            summary=summary,
                        )

                        st.success("✅ Thank you for your feedback!")

                        # Show AI response
                        st.markdown("---")
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("### 🤖 AI Response")
                            st.info(ai_response)

                        with col2:
                            st.markdown("### 📝 AI Summary")
                            st.info(summary)

                        # Show sentiment
                        sentiment_emoji = {
                            "positive": "😊",
                            "negative": "😞",
                            "neutral": "😐",
                        }
                        st.markdown(
                            f"**Sentiment Detected:** {sentiment_emoji.get(sentiment, '🤔')} **{sentiment.upper()}**"
                        )

                    except Exception as e:
                        st.error(f"❌ Error processing feedback: {str(e)}")


def render_admin_dashboard():
    """Admin-facing dashboard showing all submissions"""
    st.title("📊 Admin Dashboard - Feedback Management")
    st.markdown("View and manage all customer feedback submissions.")

    # Get all feedback
    df = get_all_feedback()

    if len(df) == 0:
        st.info("📭 No feedback submissions yet.")
        return

    # ─────────────────────────────────────────────────────────────
    # KEY METRICS
    # ─────────────────────────────────────────────────────────────

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Submissions", len(df))

    with col2:
        avg_rating = df["rating"].mean()
        st.metric("Avg Rating", f"{avg_rating:.1f}⭐")

    with col3:
        positive = len(df[df["sentiment"] == "positive"])
        st.metric("Positive Reviews", f"{positive}/{len(df)}")

    with col4:
        satisfaction = (len(df[df["rating"] >= 4]) / len(df)) * 100
        st.metric("Satisfaction Rate", f"{satisfaction:.0f}%")

    st.markdown("---")

    # ─────────────────────────────────────────────────────────────
    # ANALYTICS SECTION
    # ─────────────────────────────────────────────────────────────

    st.subheader("📈 Analytics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Rating Distribution")
        rating_dist = get_rating_distribution(df)
        st.bar_chart(rating_dist)

    with col2:
        st.markdown("### Sentiment Breakdown")
        sentiment_dist = get_sentiment_breakdown(df)
        st.bar_chart(sentiment_dist)

    with col3:
        st.markdown("### Feedback by Category")
        category_dist = df["category"].value_counts()
        st.bar_chart(category_dist)

    st.markdown("---")

    # ─────────────────────────────────────────────────────────────
    # FILTERS
    # ─────────────────────────────────────────────────────────────

    st.subheader("🔍 Filter Feedback")
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_category = st.multiselect(
            "Category",
            df["category"].unique(),
            default=df["category"].unique(),
        )

    with col2:
        selected_sentiment = st.multiselect(
            "Sentiment",
            df["sentiment"].unique(),
            default=df["sentiment"].unique(),
        )

    with col3:
        min_rating, max_rating = st.slider(
            "Rating Range",
            1,
            5,
            (1, 5),
        )

    # Apply filters
    filtered_df = df[
        (df["category"].isin(selected_category))
        & (df["sentiment"].isin(selected_sentiment))
        & (df["rating"] >= min_rating)
        & (df["rating"] <= max_rating)
    ]

    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} submissions**")
    st.markdown("---")

    # ─────────────────────────────────────────────────────────────
    # DETAILED FEEDBACK LIST
    # ─────────────────────────────────────────────────────────────

    st.subheader("📋 Detailed Feedback List")

    if len(filtered_df) == 0:
        st.warning("No feedback matches the selected filters.")
    else:
        for idx, row in filtered_df.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    # Header
                    rating_emoji = "⭐" * row["rating"]
                    st.markdown(
                        f"**{row['user_name']}** — {row['category']} | {rating_emoji} ({row['rating']}/5)"
                    )

                    # Content
                    st.markdown(f"__{row['created_at'][:10]}__")
                    st.markdown(f"📝 **Review:** {row['message'][:200]}...")

                    # AI Analysis
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**Summary:** {row['summary'][:150]}...")
                    with col_b:
                        sentiment_emoji = {
                            "positive": "😊",
                            "negative": "😞",
                            "neutral": "😐",
                        }
                        st.markdown(
                            f"**Sentiment:** {sentiment_emoji.get(row['sentiment'], '🤔')} {row['sentiment'].upper()}"
                        )

                    # Recommendations (if available)
                    if pd.notna(row.get("recommendations")):
                        st.markdown(f"💡 **Actions:** {row['recommendations'][:150]}...")

                with col2:
                    # Action buttons
                    if st.button("👁️ View Full", key=f"view_{idx}"):
                        st.markdown("### Full Details")
                        st.json(
                            {
                                "Name": row["user_name"],
                                "Email": row.get("email", "N/A"),
                                "Category": row["category"],
                                "Rating": row["rating"],
                                "Review": row["message"],
                                "Sentiment": row["sentiment"],
                                "Summary": row["summary"],
                                "AI Response": row.get("ai_response", "N/A"),
                                "Recommendations": row.get("recommendations", "N/A"),
                                "Date": row["created_at"],
                            }
                        )

                st.markdown("---")

    # ─────────────────────────────────────────────────────────────
    # EXPORT DATA
    # ─────────────────────────────────────────────────────────────

    st.subheader("💾 Export Data")
    col1, col2 = st.columns(2)

    with col1:
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name="feedback_export.csv",
            mime="text/csv",
        )

    with col2:
        json_data = filtered_df.to_json(orient="records", indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_data,
            file_name="feedback_export.json",
            mime="application/json",
        )


# ═══════════════════════════════════════════════════════════════════════════
# MAIN APP LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main application"""
    import pandas as pd

    # Sidebar Navigation
    with st.sidebar:
        st.title("🎯 AI Feedback System")
        st.markdown("---")

        page = st.radio(
            "Select Dashboard",
            ["⭐ User Dashboard", "📊 Admin Dashboard"],
            help="Choose which dashboard to view",
        )

        st.markdown("---")
        st.markdown(
            """
            ### ℹ️ About
            
            AI-powered feedback system using Perplexity API.
            
            **Features:**
            - Star rating (1-5)
            - AI response generation
            - Sentiment analysis
            - Analytics dashboard
            - Admin management
            """
        )

    # Render selected dashboard
    if page == "⭐ User Dashboard":
        render_user_dashboard()
    else:
        render_admin_dashboard()


if __name__ == "__main__":
    main()
