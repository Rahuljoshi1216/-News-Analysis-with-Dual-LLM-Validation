import os
import json
import requests
from dotenv import load_dotenv
from typing import Dict

load_dotenv()


class LLMAnalyzerError(Exception):
    pass


def build_prompt(article: Dict) -> str:
    title = article.get("title", "")
    content = article.get("content", "") or article.get("description", "")

    return f"""
Analyze the following news article and return ONLY valid JSON with this structure:

{{
  "gist": "1-2 sentence summary",
  "sentiment": "positive | negative | neutral",
  "tone": "analytical | urgent | balanced | satirical | optimistic | critical"
}}

Article Title: {title}

Article Content:
{content}

Important:
- Respond ONLY with JSON
- Do not add any extra text
"""


def analyze_article(article: Dict) -> Dict:

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise LLMAnalyzerError("OPENROUTER_API_KEY not found in environment variables")

    prompt = build_prompt(article)

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        if response.status_code != 200:
            raise LLMAnalyzerError(f"OpenRouter API error: {response.text}")

        data = response.json()

        text = data["choices"][0]["message"]["content"].strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        result = json.loads(text)

        return result

    except json.JSONDecodeError:
        raise LLMAnalyzerError("Failed to parse OpenRouter response as JSON")

    except Exception as e:
        raise LLMAnalyzerError(f"Error during LLM analysis: {str(e)}")
