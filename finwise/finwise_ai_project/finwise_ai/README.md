# FinWise AI

**AI-Powered Personal Financial Analysis and Smart Budget Assistant**

FinWise AI is an educational FinTech prototype built with Python, Streamlit,
LangChain, and OpenAI's ChatOpenAI. Users enter monthly income, expenses,
savings, and a financial goal. Python performs deterministic calculations and
a LangChain-powered model produces structured educational budgeting insights.

> **Educational Disclaimer:** FinWise AI is an educational prototype for
> informational purposes only. It does not provide professional financial or
> investment advice, does not guarantee financial outcomes, and does not execute
> financial transactions. Consult a qualified financial professional for advice
> specific to your situation.

## Features

- Deterministic Python financial calculations
- Educational 0–100 preliminary score
- LangChain `ChatOpenAI`
- Required `PromptTemplate`
- Required `ChatPromptTemplate`
- `SystemMessage`, `HumanMessage`, and `AIMessage` demonstration
- Reusable `LLMChain`
- Exact structured JSON schema
- Safe JSON parsing and fallback behavior
- Live `llm.stream()` + `st.write_stream()`
- `InMemoryCache`
- `SQLiteCache`
- Streamlit dashboard with metrics, tabs, expanders, progress bars, warnings,
  and reset-session control
- No bank-account or transaction connectivity

## Technologies

- Python 3.10+
- Streamlit
- LangChain
- langchain-openai
- langchain-community
- langchain-core
- OpenAI
- python-dotenv

## Folder Structure

```text
finwise_ai/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── prompts.py
│   ├── financial_calculator.py
│   ├── chains.py
│   ├── cache_manager.py
│   └── utils.py
│
└── docs/
    └── FinTech_AI_Assignment.pdf
```

## Installation on Windows

Open PowerShell or Command Prompt.

### 1. Open the project

```powershell
cd path\to\finwise_ai
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate it

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure the API key

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Open `.env` and replace the placeholder with your own OpenAI API key:

```text
OPENAI_API_KEY=sk-your-real-key
```

Never commit `.env` to GitHub.

## Run the Application

```bash
streamlit run app.py
```

Streamlit will show a local address in the terminal. Open that address in your
browser.

## Python Calculations vs AI Analysis

Python is responsible for:

- Total expenses
- Remaining income
- Savings ratio
- Expense ratio
- Debt burden
- Preliminary educational score

These calculations are deterministic and do not depend on the LLM.

The LLM is responsible for:

- Spending observations
- Educational recommendations
- Risk-pattern discussion
- Budget suggestions
- Goal-aligned savings ideas
- Next-month action plan

This separation makes the financial arithmetic reproducible and easier to
explain during a viva.

## Prompt Engineering

`src/prompts.py` contains:

1. A reusable `PromptTemplate` with the required variables:
   - `monthly_income`
   - `total_expenses`
   - `remaining_income`
   - `savings`
   - `savings_ratio`
   - `expense_ratio`
   - `financial_goal`
   - `expense_breakdown`

2. A `ChatPromptTemplate` containing system safety instructions and dynamic
   financial data.

## LangChain Components

`src/chains.py` demonstrates:

- `ChatOpenAI`
- `LLMChain`
- `SystemMessage`
- `HumanMessage`
- `AIMessage`
- `llm.stream()`

## Structured JSON

The model is instructed to return exactly:

```json
{
  "financial_summary": "",
  "financial_health_score": 0,
  "spending_analysis": [
    {
      "category": "",
      "observation": "",
      "recommendation": ""
    }
  ],
  "risk_level": "",
  "top_priorities": [],
  "budget_recommendations": [],
  "savings_strategy": [],
  "next_month_action_plan": []
}
```

`src/utils.py` safely parses the response and prevents malformed JSON from
crashing the application.

## Streaming

The final recommendation is generated using:

```python
llm.stream(...)
```

and rendered using:

```python
st.write_stream(...)
```

The app does not fake streaming by printing an already-completed response
character by character.

## Caching

The sidebar provides two options.

### InMemoryCache

- Stored in RAM
- Fastest
- Does not survive restart
- Useful for one session

### SQLiteCache

- Stored on disk
- Slightly slower
- Survives restart
- Useful for reusing identical results across sessions

LangChain's `set_llm_cache(...)` registers the selected cache globally. When an
identical prompt is requested, LangChain can reuse the cached model response.

## Testing Scenarios

### Scenario 1 — Strong positive balance

Income: `8000`

Set expenses to approximately `2000`.

Expected:

- Large positive remaining income
- High retention/savings potential
- Generally healthy/strong educational score
- LOW risk
- Growth-oriented budgeting suggestions

### Scenario 2 — Expenses exceed income

Income: `2000`

Set expenses to approximately `2600`.

Expected:

- Negative remaining income
- Expense ratio above 100%
- Low score
- HIGH risk
- Urgent cost-cutting and stabilization suggestions

### Scenario 3 — High debt burden

Income: `5000`

Set Loan/Debt to `2500`.

Expected:

- High debt share of income
- MEDIUM/HIGH risk
- Debt-reduction priorities

### Scenario 4 — Strong savings

Income: `4000`

Set current monthly savings to `1200`.

Expected:

- Savings ratio approximately 30%
- Stronger educational score
- LOW risk when expenses are otherwise controlled
- Reinforcement of good habits

### Scenario 5 — No remaining balance

Income: `3000`

Set total expenses to `3000`.

Expected:

- Remaining income = 0
- MEDIUM/HIGH risk
- Recommendations to create room for savings

## Important Note About Expense Categories

The assignment PDF says "ten expense categories" but the actual listed input
categories are:

1. Housing/Rent
2. Food
3. Transportation
4. Utilities
5. Education
6. Healthcare
7. Entertainment
8. Loan/Debt
9. Other

The implementation preserves these exact names rather than inventing a tenth
category that does not appear in the PDF.

## Educational Score

The PDF specifies a weighted 0–100 heuristic using savings, leftover income,
expense ratio, and debt burden, but it does not provide numeric weights. This
implementation documents its educational heuristic in
`financial_calculator.py`:

- Savings: 35%
- Leftover income: 30%
- Expense ratio: 20%
- Debt burden: 15%

These are prototype scoring rules, not professional financial standards.

## GitHub Submission

Before pushing:

1. Confirm `.env` is ignored.
2. Confirm no API key appears in source code.
3. Include every project file.
4. Include the assignment PDF under `docs/`.
5. Run:

```bash
streamlit run app.py
```

6. Demonstrate:
   - form submission
   - deterministic calculations
   - AI JSON dashboard
   - streamed recommendation
   - cache selection
   - reset session
   - educational disclaimer

7. Record a short demo or screen recording if required by the course.

## Safety

FinWise AI must not be used as professional financial advice. It is an
educational programming assignment and cannot guarantee financial outcomes,
execute financial transactions, or access real bank accounts.
