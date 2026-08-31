"""Centralized PromptTemplate and ChatPromptTemplate definitions."""

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# JSON schema example with double-escaped braces for LangChain templates
JSON_SCHEMA_TEXT = """{{
  "financial_summary": "",
  "financial_health_score": 0,
  "spending_analysis": [
    {{
      "category": "",
      "observation": "",
      "recommendation": ""
    }}
  ],
  "risk_level": "",
  "top_priorities": [],
  "budget_recommendations": [],
  "savings_strategy": [],
  "next_month_action_plan": []
}}"""

SYSTEM_INSTRUCTIONS = f"""
You are FinWise AI, an educational personal financial analysis assistant.
Your job is to analyze only the financial information supplied by the user and produce understandable, educational budgeting insights.

SAFETY RULES:
- This is an educational prototype for informational purposes only.
- Do not present yourself as a licensed financial advisor.
- Do not guarantee financial or investment outcomes.
- Do not promise returns.
- Do not instruct the user to execute specific financial transactions.
- Do not claim to access bank accounts, credit reports, markets, or other data that was not provided.
- Do not invent missing financial facts.
- Treat the financial health score as an educational prototype score, not a professional financial assessment.
- Always reinforce that users should consult a qualified financial professional for advice specific to their circumstances.
- Keep recommendations practical and budget-focused.

Return ONLY valid JSON matching this exact schema:
{JSON_SCHEMA_TEXT}
"""

# Required PromptTemplate variables from the assignment.
FINANCIAL_PROMPT = PromptTemplate(
    input_variables=[
        "monthly_income",
        "total_expenses",
        "remaining_income",
        "savings",
        "savings_ratio",
        "expense_ratio",
        "financial_goal",
        "expense_breakdown",
    ],
    template="""
Analyze this user's monthly financial information for educational budgeting purposes.

Monthly income: {{monthly_income}}
Total expenses: {{total_expenses}}
Remaining income: {{remaining_income}}
Current monthly savings: {{savings}}
Savings ratio: {{savings_ratio}}%
Expense ratio: {{expense_ratio}}%
Financial goal: {{financial_goal}}
Expense breakdown:
{{expense_breakdown}}

Identify spending patterns, high-expense categories, possible savings opportunities, potential risk patterns, and budgeting improvements.

Return only the exact JSON schema requested by the system instructions.
""".strip(),
)

CHAT_FINANCIAL_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_INSTRUCTIONS),
        (
            "human",
            """
Analyze this user's monthly financial information for educational budgeting purposes.

Monthly income: {monthly_income}
Total expenses: {total_expenses}
Remaining income: {remaining_income}
Current monthly savings: {savings}
Savings ratio: {savings_ratio}%
Expense ratio: {expense_ratio}%
Financial goal: {financial_goal}
Expense breakdown:
{expense_breakdown}

Identify spending patterns, high-expense categories, possible savings opportunities, potential risk patterns, and budgeting improvements.

Return only the exact JSON schema requested by the system instructions.
""".strip(),
        ),
    ]
)

NARRATIVE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are FinWise AI, an educational personal financial analysis assistant.
Write a concise, practical narrative recommendation based only on the supplied financial numbers. Do not guarantee outcomes, provide professional investment advice, claim bank access, or instruct users to execute transactions.
Mention that this is educational information and recommend consulting a qualified financial professional for situation-specific advice.
""".strip(),
        ),
        (
            "human",
            """
Income: {monthly_income}
Total expenses: {total_expenses}
Remaining income: {remaining_income}
Savings: {savings}
Savings ratio: {savings_ratio}%
Expense ratio: {expense_ratio}%
Financial goal: {financial_goal}
Expense breakdown:
{expense_breakdown}

Give a short narrative covering the most important spending pattern, one or two budgeting opportunities, and a next-month focus.
""".strip(),
        ),
    ]
)