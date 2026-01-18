import os
import requests
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

NEWSAPI_URL = "https://newsapi.org/v2/everything"


class NewsAPIError(Exception):
    """Custom exception for NewsAPI related errors"""
    pass


def fetch_articles(query: str = "India politics", limit: int = 10) -> List[Dict]:
    """
    Fetch recent news articles from NewsAPI.

    Args:
        query (str): Search query for news articles
        limit (int): Number of articles to fetch

    Returns:
        List[Dict]: List of article dictionaries

    Raises:
        NewsAPIError: If any error occurs during fetching
    """

    api_key = os.getenv("NEWSAPI_KEY")

    if not api_key:
        raise NewsAPIError("NEWSAPI_KEY not found in environment variables")

    params = {
        "q": query,
        "apiKey": api_key,
        "pageSize": limit,
        "language": "en",
        "sortBy": "publishedAt"
    }

    try:
        response = requests.get(NEWSAPI_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise NewsAPIError("Request to NewsAPI timed out")
    except requests.exceptions.RequestException as e:
        raise NewsAPIError(f"Error fetching articles: {str(e)}")

    data = response.json()

    if data.get("status") != "ok":
        raise NewsAPIError("Invalid response from NewsAPI")

    articles = data.get("articles", [])

    cleaned_articles = []

    for article in articles:
        cleaned_articles.append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "url": article.get("url", ""),
            "publishedAt": article.get("publishedAt", ""),
            "source": article.get("source", {}).get("name", "")
        })

    return cleaned_articles
