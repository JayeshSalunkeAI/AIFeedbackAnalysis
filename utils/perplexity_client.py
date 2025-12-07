# utils/perplexity_client.py

import os
import requests
import streamlit as st
import json

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


def _get_api_key():
    """Get Perplexity API key from environment"""
    key = os.getenv("PERPLEXITY_API_KEY")
    if not key:
        st.warning("⚠️ PERPLEXITY_API_KEY is not configured. AI features disabled.")
    return key


def call_perplexity(system_prompt: str, user_prompt: str, temperature: float = 0.3, max_tokens: int = 512):
    """
    Call Perplexity API (sonar-pro model)
    
    Args:
        system_prompt: System role message
        user_prompt: User message
        temperature: Creativity level (0.1-1.0)
        max_tokens: Max response length
        
    Returns:
        str: API response or None if error
    """
    api_key = _get_api_key()
    if not api_key:
        return "AI response unavailable - API key not configured."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "sonar-pro",
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    try:
        response = requests.post(
            PERPLEXITY_API_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return content
    except requests.exceptions.Timeout:
        return "⏱️ Request timeout - please try again"
    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_review_sentiment(review_text: str):
    """
    Analyze sentiment of review text
    
    Returns: 'positive', 'negative', or 'neutral'
    """
    system_prompt = (
        "You are a sentiment analysis expert. Analyze the given text and respond with ONLY "
        "one word: positive, negative, or neutral. No explanation needed."
    )

    user_prompt = f"Analyze sentiment:\n{review_text}"

    result = call_perplexity(system_prompt, user_prompt, temperature=0.1, max_tokens=10)

    if result:
        sentiment = result.lower().strip()
        if "positive" in sentiment:
            return "positive"
        elif "negative" in sentiment:
            return "negative"
        else:
            return "neutral"
    return "neutral"


def generate_ai_response(review_text: str, category: str):
    """
    Generate a professional AI response to customer feedback
    """
    system_prompt = (
        "You are a helpful customer service representative. Generate a professional, "
        "empathetic response to the customer feedback. Keep it concise (max 100 words). "
        "Thank them and address their main concern."
    )

    user_prompt = f"Category: {category}\n\nCustomer feedback:\n{review_text}\n\nGenerate a response:"

    result = call_perplexity(system_prompt, user_prompt, temperature=0.5, max_tokens=150)
    return result if result else "Thank you for your feedback!"


def generate_summary(review_text: str):
    """
    Generate a brief AI summary of the review
    """
    system_prompt = (
        "You are a summarization expert. Create a very brief one-sentence summary of the "
        "given customer review. Focus on the main point. Max 20 words."
    )

    user_prompt = f"Review:\n{review_text}\n\nGenerate summary:"

    result = call_perplexity(system_prompt, user_prompt, temperature=0.2, max_tokens=50)
    return result if result else "Customer feedback received"


def generate_recommendations(review_text: str, category: str, sentiment: str):
    """
    Generate recommended actions based on feedback
    """
    system_prompt = (
        "You are a business analyst. Based on the customer feedback, suggest ONE actionable "
        "recommendation for the team. Be specific and practical. Max 30 words."
    )

    user_prompt = (
        f"Category: {category}\nSentiment: {sentiment}\n\nFeedback:\n{review_text}\n\n"
        "Recommend action:"
    )

    result = call_perplexity(system_prompt, user_prompt, temperature=0.4, max_tokens=80)
    return result if result else "Follow up with customer"