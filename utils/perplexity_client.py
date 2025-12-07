# utils/perplexity_client.py

import os
import requests
import json
from typing import Optional, Dict, List, Any

# Get API key from environment variable
api_key = os.getenv('PERPLEXITY_API_KEY')

if not api_key:
    print("⚠️  WARNING: PERPLEXITY_API_KEY environment variable not set")
    print("Please set it before using AI features:")
    print("  - Mac/Linux: export PERPLEXITY_API_KEY='your-key'")
    print("  - Windows: set PERPLEXITY_API_KEY=your-key")


def call_perplexity(
    messages: List[Dict[str, str]],
    temperature: float = 0.5,
    max_tokens: int = 500
) -> Dict[str, Any]:
    """
    Call Perplexity API with error handling
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        temperature: Creativity level (0.0 - 1.0)
        max_tokens: Maximum response length
    
    Returns:
        Response JSON or error dict
    """
    
    if not api_key:
        return {
            "error": "API key not configured. Set PERPLEXITY_API_KEY environment variable."
        }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sonar-pro",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        
        # Handle different status codes
        if response.status_code == 401:
            return {
                "error": "Unauthorized - Invalid API key. Check your PERPLEXITY_API_KEY"
            }
        elif response.status_code == 429:
            return {
                "error": "Rate limit exceeded. Please try again later"
            }
        elif response.status_code == 500:
            return {
                "error": "Perplexity API server error. Try again later"
            }
        elif response.status_code != 200:
            return {
                "error": f"API Error {response.status_code}: {response.text}"
            }
        
        return response.json()
    
    except requests.exceptions.Timeout:
        return {"error": "API request timeout. Please try again"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error. Check your internet"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def analyze_review_sentiment(review_text: str) -> str:
    """
    Analyze sentiment of a review
    
    Args:
        review_text: The review text to analyze
    
    Returns:
        'positive', 'negative', or 'neutral'
    """
    
    if not review_text or len(review_text) < 3:
        return "neutral"
    
    messages = [
        {
            "role": "user",
            "content": f"""Analyze the sentiment of this review and respond with ONLY one word:
            
Review: {review_text}

Respond with ONLY: positive, negative, or neutral"""
        }
    ]
    
    response = call_perplexity(messages, temperature=0.1, max_tokens=10)
    
    if "error" in response:
        print(f"Sentiment analysis error: {response['error']}")
        return "neutral"
    
    try:
        content = response.get('choices', [{}])[0].get('message', {}).get('content', '').lower().strip()
        
        # Clean up response
        content = content.replace('.', '').replace('!', '').replace(',', '')
        
        if 'positive' in content:
            return 'positive'
        elif 'negative' in content:
            return 'negative'
        else:
            return 'neutral'
    
    except (KeyError, IndexError, AttributeError):
        return "neutral"


def generate_ai_response(
    user_message: str,
    category: str,
    sentiment: Optional[str] = None
) -> str:
    """
    Generate a professional AI response to user feedback
    AUTO-DETECTS SENTIMENT if not provided
    
    Args:
        user_message: The user's feedback message
        category: Category of feedback
        sentiment: Detected sentiment (optional - will be auto-detected if not provided)
    
    Returns:
        AI-generated response string
    """
    
    if not user_message or len(user_message) < 5:
        return "Thank you for your feedback!"
    
    # AUTO-DETECT SENTIMENT if not provided
    if sentiment is None:
        sentiment = analyze_review_sentiment(user_message)
    
    tone_map = {
        'positive': 'enthusiastic and grateful',
        'negative': 'empathetic and solution-focused',
        'neutral': 'professional and helpful'
    }
    
    tone = tone_map.get(sentiment, 'professional')
    
    messages = [
        {
            "role": "user",
            "content": f"""Generate a short, professional customer service response (max 2 sentences) to this feedback.
Be {tone}.

Category: {category}
Customer Feedback: {user_message}

Response:"""
        }
    ]
    
    response = call_perplexity(messages, temperature=0.5, max_tokens=150)
    
    if "error" in response:
        print(f"Response generation error: {response['error']}")
        return f"Thank you for your {sentiment} feedback about {category}. We appreciate your input!"
    
    try:
        content = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        # Clean up response
        if content:
            return content[:200]  # Limit to 200 chars
        else:
            return "Thank you for your feedback!"
    
    except (KeyError, IndexError, AttributeError):
        return "Thank you for your feedback!"


def generate_summary(review_text: str) -> str:
    """
    Generate a one-sentence summary of a review
    
    Args:
        review_text: The review text to summarize
    
    Returns:
        One-sentence summary
    """
    
    if not review_text or len(review_text) < 5:
        return "Short feedback received"
    
    messages = [
        {
            "role": "user",
            "content": f"""Summarize this feedback in exactly one sentence (under 15 words):

Feedback: {review_text}

Summary:"""
        }
    ]
    
    response = call_perplexity(messages, temperature=0.2, max_tokens=50)
    
    if "error" in response:
        print(f"Summary generation error: {response['error']}")
        return review_text[:50] + "..." if len(review_text) > 50 else review_text
    
    try:
        content = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        # Clean up response
        content = content.replace('Summary: ', '').replace('Summary:', '')
        
        if content:
            return content[:100]  # Limit to 100 chars
        else:
            return review_text[:50]
    
    except (KeyError, IndexError, AttributeError):
        return review_text[:50]


def generate_recommendations(
    review_text: str,
    category: str,
    sentiment: Optional[str] = None
) -> str:
    """
    Generate actionable recommendations based on feedback
    AUTO-DETECTS SENTIMENT if not provided
    
    Args:
        review_text: The review text
        category: Category of feedback
        sentiment: Detected sentiment (optional - will be auto-detected if not provided)
    
    Returns:
        Recommended action for the team
    """
    
    if not review_text or len(review_text) < 5:
        return "Monitor feedback quality"
    
    # AUTO-DETECT SENTIMENT if not provided
    if sentiment is None:
        sentiment = analyze_review_sentiment(review_text)
    
    action_prompt = {
        'negative': 'What specific action should the team take to address this issue?',
        'positive': 'How can we maintain or build on this positive experience?',
        'neutral': 'How could we improve based on this feedback?'
    }
    
    prompt = action_prompt.get(sentiment, 'How should we respond to this feedback?')
    
    messages = [
        {
            "role": "user",
            "content": f"""Based on this customer feedback, provide ONE actionable recommendation (max 1 sentence).

Category: {category}
Sentiment: {sentiment}
Feedback: {review_text}

{prompt}

Recommendation:"""
        }
    ]
    
    response = call_perplexity(messages, temperature=0.4, max_tokens=80)
    
    if "error" in response:
        print(f"Recommendation generation error: {response['error']}")
        
        # Return smart fallback based on sentiment
        if sentiment == 'negative':
            return "Investigate and resolve the reported issue"
        elif sentiment == 'positive':
            return "Document and replicate this successful approach"
        else:
            return "Analyze feedback for potential improvements"
    
    try:
        content = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        # Clean up response
        content = content.replace('Recommendation: ', '').replace('Recommendation:', '')
        
        if content:
            return content[:150]  # Limit to 150 chars
        else:
            return "Review and act on feedback"
    
    except (KeyError, IndexError, AttributeError):
        return "Review and act on feedback"


def test_api_connection() -> bool:
    """
    Test if API key is valid and working
    
    Returns:
        True if API is reachable, False otherwise
    """
    
    if not api_key:
        print("❌ API key not configured")
        return False
    
    messages = [{"role": "user", "content": "Hello"}]
    response = call_perplexity(messages, temperature=0.1, max_tokens=5)
    
    if "error" in response:
        print(f"❌ API Error: {response['error']}")
        return False
    
    print("✅ API Connection Successful")
    return True