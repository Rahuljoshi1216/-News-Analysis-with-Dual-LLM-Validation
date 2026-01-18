# Development Process

## 1. Problem Statement

Build a news analysis pipeline that fetches recent articles about Indian politics, analyzes them using an LLM, validates the analysis using a second LLM, and generates a final structured report.

The goal is to demonstrate an AI-assisted workflow with proper engineering discipline.

---

## 2. Understanding Requirements

From the assignment, the system must:

- Fetch 10–15 recent news articles using NewsAPI  
- Analyze each article using Gemini LLM to extract:
  - Gist (1–2 sentence summary)
  - Sentiment (positive / negative / neutral)
  - Tone (analytical / urgent / etc.)

- Validate the Gemini output using a second LLM (Mistral via OpenRouter)
- Save results as:
  - raw JSON
  - processed JSON
  - human-readable Markdown report

Constraints:

- Use free APIs only  
- No API keys in code  
- Must include tests  
- Must document AI prompts and iterations  

---

## 3. Chosen Tools and APIs

I decided to use:

- NewsAPI → for fetching articles  
- Google Gemini → primary analysis LLM  
- OpenRouter (Mistral-7B) → validation LLM  

Reasons:

- All are available on free tier  
- Easy integration with Python  
- Good documentation  
- Fits the assignment guidelines  

---

## 4. Planned Architecture

The project is divided into small modules:

1. news_fetcher.py – Fetch articles  
2. llm_analyzer.py – Analyze articles using Gemini  
3. llm_validator.py – Validate results using Mistral  
4. main.py – Orchestrate full workflow  

This modular structure keeps the system clean and testable.

---

## 5. Task Breakdown

I divided the project into the following steps:

1. Setup project structure  
2. Implement NewsAPI fetcher  
3. Implement Gemini analyzer  
4. Implement OpenRouter validator  
5. Connect modules in main.py  
6. Save outputs to JSON  
7. Generate Markdown report  
8. Add error handling  
9. Write unit tests  
10. Final cleanup and documentation  

---

## 6. AI-Assisted Workflow Plan

For each module I will follow this process:

- Write a clear prompt for AI  
- Generate small focused functions  
- Review the generated code  
- Improve error handling  
- Add logging and tests  
- Iterate if output quality is poor  

---

## 7. Expected Output

At the end the system should generate:

- output/raw_articles.json  
- output/analysis_results.json  
- output/final_report.md  

---

This document will be updated continuously as development progresses.


## Task 1: Implement News Fetcher

**Goal:**  
Create a module to fetch recent news articles using NewsAPI.

**AI Prompt Used:**

"Write a Python module named news_fetcher.py that fetches recent news articles from NewsAPI. Read API key from environment variable, handle errors, return list of cleaned articles with fields: title, description, content, url, publishedAt, source."

**My Review:**

The generated code was reviewed carefully for:

- Proper error handling  
- Security of API key usage  
- Handling network timeouts  
- Cleaning and structuring returned data  

**Improvements Made:**

- Added a custom exception class for better clarity  
- Implemented request timeout handling  
- Added validation for missing API key  
- Limited returned fields to only required ones  
- Ensured the function contains no print statements  

**Result:**

A clean, reusable function `fetch_articles()` that safely returns structured article data ready for further processing.

---

## Task 2: Initial Attempt – LLM Analyzer Using Gemini

**Goal:**  
Use Google Gemini as the primary LLM to analyze each article and extract structured insights including gist, sentiment, and tone.

**Planned Approach:**

- Use Gemini API for text analysis  
- Send a structured prompt requesting JSON output  
- Parse and validate the response  
- Return standardized analysis results  

**Issue Encountered:**

During implementation and testing, repeated API calls resulted in:

- HTTP 429 quota exceeded errors  
- Free-tier limits being reached immediately  
- No available quota even after generating new API keys  

Despite multiple attempts, the Gemini API could not be used reliably due to persistent account-level quota restrictions.

---

## Change in Implementation Due to Quota Constraints

While the original design planned to use Gemini as the primary analyzer, I encountered persistent free-tier quota limits on the Google AI Studio API.

Even after generating new API keys, the quota remained exhausted, indicating account-level restrictions.

To ensure the project remains fully functional and demonstrable, I switched the primary LLM to OpenRouter using the free model:

**mistralai/mistral-7b-instruct**

This change is fully compliant with the assignment guidelines, which explicitly allow OpenRouter models.

The overall architecture (dual-LLM validation pipeline) remains unchanged.

This decision ensured that development could continue without dependency on unstable external quotas while maintaining all functional requirements.

---

## Task 2 – Revised Implementation Using OpenRouter

After deciding to switch from Gemini to OpenRouter, I updated the `llm_analyzer` module to:

- Use OpenRouter API instead of Google Gemini  
- Call the free model `mistralai/mistral-7b-instruct`  
- Maintain the same structured JSON output format  
- Keep the same prompt design and parsing logic  
- Implement proper error handling for API responses  

**Benefits of the Revised Approach:**

- No dependency on Google API quotas  
- More stable and predictable execution  
- Fully free-tier compatible  
- Consistent output quality  

**Result:**

A fully working analyzer module that reliably converts raw news articles into structured analysis containing:

- Gist  
- Sentiment  
- Tone  

This ensured that the project pipeline could continue smoothly without further external API limitations.


## Task 3: Implement LLM Validator

**Goal:**  
Add a second independent LLM step to verify the correctness of the initial article analysis.

**Purpose of This Module:**

The validator acts as a quality control layer. Instead of trusting the first LLM blindly, a second model is used to:

- Review the generated gist  
- Check whether the detected sentiment is reasonable  
- Verify whether the assigned tone matches the article  
- Provide an independent judgment  

This ensures the pipeline follows a true dual-LLM validation approach.

---

### Planned Design

The validator module (`llm_validator.py`) was designed to:

- Take the original article as input  
- Take the structured analysis from `llm_analyzer.py`  
- Use a second OpenRouter model to evaluate the result  
- Return a structured JSON response in this format:

{
  "is_valid": true or false,
  "reason": "explanation of decision"
}

---

### AI Prompt Strategy

A dedicated validation prompt was crafted with the following goals:

- Provide both the article and the generated analysis  
- Ask the model to judge accuracy and reasonableness  
- Force the output to be strictly valid JSON  
- Prevent any extra text outside the required format  

This ensured that validation results could be parsed programmatically.

---

### Model Selection

Since the analyzer already used:

mistralai/mistral-7b-instruct

a different model was required for independent validation to maintain separation of reasoning.

OpenRouter was used again for the validator step, ensuring:

- Free-tier compatibility  
- No dependency on Google Gemini quotas  
- True two-model architecture  

---

### Issues Encountered

During implementation, several real-world challenges appeared:

#### 1. Model Availability Problems

Initial validator models such as:

- meta-llama/llama-2-7b-chat  
- google/gemma-7b-it  

were unavailable on my OpenRouter account and resulted in “invalid model ID” or “no endpoints found” errors.

**Resolution:**

To avoid hardcoding unavailable models, the validator was switched to:

openrouter/auto

This automatically selects an available free model and keeps the system stable.

---

#### 2. Token Limit Issue

After switching to a working model, requests failed with the error:

"This request requires more credits, or fewer max_tokens."

This happened because OpenRouter assumed a very high default token limit.

**Fix Applied:**

Explicit limits were added to the API request:

- max_tokens: 500  
- temperature: 0.2  

This ensured that all requests stayed within free-tier limits and executed successfully.

---

### Final Implementation

The completed `validate_analysis()` function now:

- Accepts article + analysis as input  
- Sends a structured validation prompt  
- Returns machine-readable JSON  
- Handles API errors gracefully  
- Works reliably within free-tier constraints  

---

### Result

A fully functional validation layer was added to the pipeline that:

- Critically reviews AI-generated insights  
- Prevents blindly trusting a single LLM  
- Produces structured validation output  
- Strengthens the overall reliability of the system  

This completed the dual-LLM architecture required for the assignment.


## Task 4: Build Main Pipeline and Reporting System

**Goal:**  
Integrate all previously developed modules into a single automated workflow and generate the required output artifacts.

---

### Purpose of This Task

After completing individual components (fetcher, analyzer, and validator), the final step was to combine them into a complete end-to-end system that can:

- Fetch real-world data  
- Process it through multiple AI steps  
- Validate the results  
- Save structured outputs  
- Produce a human-readable report  

This orchestration was implemented in the `main.py` script.

---

### Responsibilities of main.py

The main script was designed to perform the following operations:

1. Retrieve recent news articles using `fetch_articles()`  
2. Save raw articles to `output/raw_articles.json`  
3. For each article:
   - Generate AI analysis using `analyze_article()`  
   - Validate the analysis using `validate_analysis()`  
4. Combine all data into a structured result  
5. Save combined results to `output/analysis_results.json`  
6. Generate a formatted Markdown report at `output/final_report.md`  

---

### Implementation Strategy

The orchestration script follows a clear and modular workflow:

- Each module is called independently  
- Errors in processing one article do not stop the entire pipeline  
- Results are saved incrementally  
- Output directory is created automatically if missing  
- Final report is generated dynamically from processed results  

This ensures the system is robust and user-friendly.

---

### Outputs Generated

Running the pipeline using:

python main.py

produces the following required files:

- **raw_articles.json** – original data fetched from NewsAPI  
- **analysis_results.json** – structured analysis + validation results  
- **final_report.md** – readable summary of all articles  

These outputs match exactly what was required in the assignment.

---

### Error Handling Approach

To make the pipeline production-ready:

- All major steps are wrapped in try/except blocks  
- API failures are handled gracefully  
- Processing continues even if one article fails  
- Clear status messages are printed to the console  
- Output files are written safely using UTF-8 encoding  

---

### Result

With the completion of `main.py`, the project achieved:

- A fully automated AI-powered workflow  
- Integration of multiple external APIs  
- Dual-LLM reasoning and validation  
- Proper data storage and reporting  
- A professional, repeatable execution process  

This completed the full implementation of the take-home assignment, demonstrating real-world AI engineering practices from start to finish.
