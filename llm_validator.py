import os
import json
import requests
from dotenv import load_dotenv
from typing import Dict

load_dotenv()


class LLMValidatorError(Exception):
    pass


def build_validation_prompt(article: Dict, analysis: Dict) -> str:
    title = article.get("title", "")
    content = article.get("content", "") or article.get("description", "")

    return f"""
You are an AI validator.

Given the following news article and an AI-generated analysis, determine whether the analysis is correct and reasonable.

Article Title: {title}

Article Content:
{content}

AI Generated Analysis:
Gist: {analysis.get("gist")}
Sentiment: {analysis.get("sentiment")}
Tone: {analysis.get("tone")}

Return ONLY valid JSON in this format:

{{
  "is_valid": true or false,
  "reason": "short explanation of why the analysis is correct or incorrect"
}}

Rules:
- Do not add any text outside JSON
- Be strict but fair in validation
"""


def validate_analysis(article: Dict, analysis: Dict) -> Dict:

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise LLMValidatorError("OPENROUTER_API_KEY not found in environment variables")

    prompt = build_validation_prompt(article, analysis)

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "openrouter/auto",
                "max_tokens": 500,
                "temperature": 0.2,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        if response.status_code != 200:
            raise LLMValidatorError(f"OpenRouter API error: {response.text}")

        data = response.json()

        text = data["choices"][0]["message"]["content"].strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        result = json.loads(text)

        return result

    except json.JSONDecodeError:
        raise LLMValidatorError("Failed to parse validator response as JSON")

    except Exception as e:
        raise LLMValidatorError(f"Error during validation: {str(e)}")
