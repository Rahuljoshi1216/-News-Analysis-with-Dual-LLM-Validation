# AI News Analyzer

## Overview

This project implements an AI-assisted news analysis pipeline that:

- Fetches recent news articles about Indian politics
- Analyzes each article using a Large Language Model
- Validates the analysis using a second LLM
- Generates structured JSON outputs
- Produces a human-readable Markdown report

The project demonstrates a real-world AI workflow with modular design, error handling, and dual-LLM validation.

---

## Project Structure

```
news-analyzer/
├── main.py
├── news_fetcher.py
├── llm_analyzer.py
├── llm_validator.py
├── DEVELOPMENT_PROCESS.md
├── requirements.txt
├── .env
├── .gitignore
├── output/
│   ├── raw_articles.json
│   ├── analysis_results.json
│   └── final_report.md
└── tests/
    └── test_analyzer.py
```


## Features

- News fetching using NewsAPI  
- AI-powered analysis using OpenRouter  
- Independent validation using a second LLM  
- Robust error handling  
- Modular architecture  
- Automated report generation  

---

## Setup Instructions

### 1. Clone the repository

git clone <your-repo-url>
cd news-analyzer


### 2. Create virtual environment

python -m venv venv


Activate:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate


### 3. Install dependencies

pip install -r requirements.txt


### 4. Configure API Keys

Create a `.env` file:

OPENROUTER_API_KEY=your_key
NEWSAPI_KEY=your_key


---

## Run the Project

python main.py


Outputs will be generated in the `output/` folder.

---

## Testing

Run unit tests using:

pytest


---

## Design Philosophy

This project follows an AI-assisted development workflow with:

- Clear module separation  
- Reproducible pipeline  
- Documented reasoning  
- Dual-LLM validation  

Full development details are available in:

DEVELOPMENT_PROCESS.md

