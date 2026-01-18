import json
import os
from datetime import datetime

from news_fetcher import fetch_articles
from llm_analyzer import analyze_article
from llm_validator import validate_analysis


def save_json(data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def generate_report(results):
    lines = []
    lines.append("# News Analysis Report\n")
    lines.append(f"Generated on: {datetime.now()}\n")
    lines.append("---\n")

    for idx, item in enumerate(results, 1):
        article = item["article"]
        analysis = item["analysis"]
        validation = item["validation"]

        lines.append(f"## Article {idx}\n")
        lines.append(f"**Title:** {article.get('title')}\n")
        lines.append(f"**Source:** {article.get('source')}\n")
        lines.append(f"**Published At:** {article.get('publishedAt')}\n")
        lines.append(f"**URL:** {article.get('url')}\n")

        lines.append("\n### Analysis\n")
        lines.append(f"- **Gist:** {analysis.get('gist')}\n")
        lines.append(f"- **Sentiment:** {analysis.get('sentiment')}\n")
        lines.append(f"- **Tone:** {analysis.get('tone')}\n")

        lines.append("\n### Validation\n")
        lines.append(f"- **Is Valid:** {validation.get('is_valid')}\n")
        lines.append(f"- **Reason:** {validation.get('reason')}\n")

        lines.append("---\n")

    return "\n".join(lines)


def main():
    print("Starting News Analyzer Pipeline...\n")

    os.makedirs("output", exist_ok=True)

    try:
        print("Fetching articles...")
        articles = fetch_articles(limit=10)

        save_json(articles, "output/raw_articles.json")
        print(f"Fetched {len(articles)} articles.\n")

        results = []

        for i, article in enumerate(articles, 1):
            print(f"Processing article {i}...")

            try:
                analysis = analyze_article(article)
                validation = validate_analysis(article, analysis)

                results.append({
                    "article": article,
                    "analysis": analysis,
                    "validation": validation
                })

            except Exception as e:
                print(f"Error processing article {i}: {str(e)}")

        save_json(results, "output/analysis_results.json")
        print("\nSaved analysis results.")

        report = generate_report(results)

        with open("output/final_report.md", "w", encoding="utf-8") as f:
            f.write(report)

        print("Generated final report at output/final_report.md")

        print("\nPipeline completed successfully!")

    except Exception as e:
        print(f"Pipeline failed: {str(e)}")


if __name__ == "__main__":
    main()
