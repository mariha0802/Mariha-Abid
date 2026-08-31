from __future__ import annotations
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Check .env first, or ask user for API key in the sidebar
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    with st.sidebar:
        st.header("🔑 Authentication")
        api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password",
            help="Get your API key from platform.openai.com",
        )

# Block main interface rendering if no API key is present
if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to access the assistant.")
    st.stop()

# Set the environment variable for OpenAI / LangChain
os.environ["OPENAI_API_KEY"] = api_key

# --- Rest of your app interface code below ---
"""FinWise AI - Streamlit entry point."""


import json
from typing import Dict

import streamlit as st

from src.cache_manager import cache_description, configure_cache
from src.chains import (
    build_financial_chain,
    build_llm,
    demonstrate_messages,
    stream_recommendations,
)
from src.config import (
    CACHE_OPTIONS,
    CURRENCIES,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    EXPENSE_CATEGORIES,
    FINANCIAL_GOALS,
    OPENAI_API_KEY,
)
from src.financial_calculator import (
    calculate_financial_metrics,
    educational_risk_level,
)
from src.utils import currency_value, parse_financial_json, score_band

DISCLAIMER = """
**Educational Disclaimer:** FinWise AI is an educational prototype for
informational purposes only. It does not provide professional financial or
investment advice, does not guarantee financial outcomes, and does not execute
financial transactions. Consult a qualified financial professional for advice
specific to your situation.
"""


st.set_page_config(
    page_title="FinWise AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


def reset_session() -> None:
    """Reset only Streamlit session state."""
    st.session_state.clear()
    st.rerun()


def format_expense_breakdown(expenses: Dict[str, float]) -> str:
    """Create a stable, readable prompt representation."""
    return "\n".join(
        f"- {category}: {amount:,.2f}"
        for category, amount in expenses.items()
    )


def render_sidebar() -> tuple[str, float, str]:
    """Render sidebar controls and return model/cache settings."""
    with st.sidebar:
        st.title("💰 FinWise AI")
        st.caption("AI-Powered Personal Financial Analysis & Smart Budget Assistant")
        st.info(DISCLAIMER)

        st.subheader("Model settings")
        model_name = st.text_input("OpenAI model", value=DEFAULT_MODEL)
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_TEMPERATURE,
            step=0.1,
        )

        st.subheader("Caching")
        cache_type = st.radio("Cache mode", CACHE_OPTIONS)
        configure_cache(cache_type)
        st.caption(cache_description(cache_type))

        if st.button("🔄 Reset Session", use_container_width=True):
            reset_session()

        st.caption(
            "No bank accounts, transactions, or real financial execution are connected."
        )

    return model_name, temperature, cache_type


def render_overview(metrics: dict, currency: str) -> None:
    """Display deterministic Python calculations."""
    st.subheader("1. Financial Overview")
    st.caption("These values are calculated by deterministic Python code — not the LLM.")

    cols = st.columns(4)
    cols[0].metric("Monthly Income", currency_value(metrics["monthly_income"], currency))
    cols[1].metric("Total Expenses", currency_value(metrics["total_expenses"], currency))
    cols[2].metric("Remaining Balance", currency_value(metrics["remaining_income"], currency))
    cols[3].metric("Current Savings", currency_value(metrics["savings"], currency))

    ratio_cols = st.columns(3)
    ratio_cols[0].metric("Savings Ratio", f'{metrics["savings_ratio"]:.2f}%')
    ratio_cols[1].metric("Expense Ratio", f'{metrics["expense_ratio"]:.2f}%')
    ratio_cols[2].metric("Debt Burden", f'{metrics["debt_burden"]:.2f}%')

    st.write("### Educational Financial Health Score — Python")
    st.progress(metrics["preliminary_score"] / 100)
    st.write(
        f'**{metrics["preliminary_score"]}/100 — '
        f'{score_band(metrics["preliminary_score"])}**'
    )

    if metrics["remaining_income"] < 0:
        st.error("Your calculated expenses exceed monthly income.")
    elif metrics["remaining_income"] == 0:
        st.warning("Your calculated remaining income is zero.")
    else:
        st.success("Your calculated budget currently has a positive remaining balance.")

    with st.expander("See the expense breakdown"):
        st.json(metrics["expense_breakdown"])


def render_ai_dashboard(ai_data: dict) -> None:
    """Render the structured LLM response."""
    st.subheader("2. AI Analysis Dashboard")
    st.caption(
        "The following insights are generated by the LLM and are educational only."
    )

    score = ai_data["financial_health_score"]
    risk = ai_data["risk_level"]

    top_cols = st.columns(2)
    with top_cols[0]:
        st.metric("AI Educational Financial Health Score", f"{score}/100")
        st.progress(score / 100)
        st.caption(score_band(score))

    with top_cols[1]:
        st.metric("Risk Level", risk)
        if risk == "HIGH":
            st.error("HIGH — review spending and risk patterns carefully.")
        elif risk == "MEDIUM":
            st.warning("MEDIUM — consider improving the highlighted areas.")
        else:
            st.success("LOW — continue reinforcing sustainable budgeting habits.")

    st.info(ai_data["financial_summary"])

    tabs = st.tabs(
        [
            "Spending Analysis",
            "Priorities",
            "Budget",
            "Savings Strategy",
            "Next Month",
        ]
    )

    with tabs[0]:
        if not ai_data["spending_analysis"]:
            st.info("No spending analysis items were returned.")
        for item in ai_data["spending_analysis"]:
            with st.expander(item.get("category", "Category")):
                st.write("**Observation:**", item.get("observation", ""))
                st.write("**Recommendation:**", item.get("recommendation", ""))

    with tabs[1]:
        for item in ai_data["top_priorities"]:
            st.write(f"• {item}")

    with tabs[2]:
        for item in ai_data["budget_recommendations"]:
            st.write(f"• {item}")

    with tabs[3]:
        for item in ai_data["savings_strategy"]:
            st.write(f"• {item}")

    with tabs[4]:
        for item in ai_data["next_month_action_plan"]:
            st.write(f"• {item}")


def main() -> None:
    model_name, temperature, _cache_type = render_sidebar()

    st.title("FinWise AI")
    st.subheader("AI-Powered Personal Financial Analysis and Smart Budget Assistant")
    st.warning(DISCLAIMER)

    if not OPENAI_API_KEY:
        st.error(
            "OPENAI_API_KEY is not configured. Create a .env file from .env.example "
            "and add your API key before submitting the form."
        )

    st.markdown(
        "Enter your monthly numbers below. Python calculates the core metrics first; "
        "LangChain then turns those results into structured educational insights."
    )

    with st.form("financial_form"):
        st.subheader("Financial Information")

        income_col, savings_col, currency_col = st.columns(3)
        with income_col:
            monthly_income = st.number_input(
                "Monthly income",
                min_value=0.0,
                value=5000.0,
                step=100.0,
            )
        with savings_col:
            savings = st.number_input(
                "Current monthly savings",
                min_value=0.0,
                value=500.0,
                step=50.0,
            )
        with currency_col:
            currency = st.selectbox("Currency", CURRENCIES, index=CURRENCIES.index("USD"))

        financial_goal = st.selectbox("Financial goal", FINANCIAL_GOALS)

        st.subheader("Monthly Expenses")
        st.caption(
            "The PDF labels these as ten expense categories but explicitly lists "
            "nine names. This implementation preserves the nine exact names listed "
            "in the PDF instead of inventing an extra category."
        )

        expenses: Dict[str, float] = {}
        expense_columns = st.columns(3)

        for index, category in enumerate(EXPENSE_CATEGORIES):
            with expense_columns[index % 3]:
                expenses[category] = st.number_input(
                    category,
                    min_value=0.0,
                    value=0.0,
                    step=50.0,
                    key=f"expense_{category}",
                )

        submitted = st.form_submit_button(
            "📊 Analyze My Finances",
            use_container_width=True,
            type="primary",
        )

    if not submitted:
        st.info("Complete the form and click **Analyze My Finances** to generate the dashboard.")
        st.caption(DISCLAIMER)
        return

    metrics = calculate_financial_metrics(
        monthly_income=monthly_income,
        expenses=expenses,
        savings=savings,
    )
    metrics["monthly_income"] = monthly_income
    metrics["savings"] = savings

    render_overview(metrics, currency)

    if not OPENAI_API_KEY:
        return

    inputs = {
        "monthly_income": currency_value(monthly_income, currency),
        "total_expenses": currency_value(metrics["total_expenses"], currency),
        "remaining_income": currency_value(metrics["remaining_income"], currency),
        "savings": currency_value(savings, currency),
        "savings_ratio": metrics["savings_ratio"],
        "expense_ratio": metrics["expense_ratio"],
        "financial_goal": financial_goal,
        "expense_breakdown": format_expense_breakdown(expenses),
    }

    with st.spinner("Building LangChain financial analysis..."):
        try:
            llm = build_llm(
                api_key=OPENAI_API_KEY,
                model_name=model_name,
                temperature=temperature,
            )
            chain = build_financial_chain(llm)
            raw_response = chain.invoke(inputs)
            raw_text = str(raw_response.get("text", raw_response))
        except Exception as exc:
            st.error(f"AI analysis failed: {exc}")
            st.info(
                "The deterministic Python calculations above are still valid. "
                "Check your API key, model name, internet connection, and installed packages."
            )
            return

    ai_data, parse_error = parse_financial_json(raw_text)

    if parse_error:
        st.error(
            "The model response was not valid enough for the required JSON schema. "
            "The app used a safe fallback instead of crashing."
        )

    render_ai_dashboard(ai_data)

    st.subheader("3. Streamed Recommendation")
    st.caption(
        "This section uses llm.stream() and Streamlit's st.write_stream(). "
        "It is live model streaming, not simulated character-by-character output."
    )

    try:
        streamed = st.write_stream(stream_recommendations(llm, inputs))
        st.session_state["last_streamed_recommendation"] = streamed
    except Exception as exc:
        st.error(f"Streaming failed: {exc}")

    with st.expander("LangChain message demonstration"):
        messages = demonstrate_messages()
        for message in messages:
            st.write(f"**{message.__class__.__name__}:** {message.content}")

    with st.expander("Raw structured JSON response"):
        st.code(json.dumps(ai_data, indent=2), language="json")

    st.warning(DISCLAIMER)


if __name__ == "__main__":
    main()
