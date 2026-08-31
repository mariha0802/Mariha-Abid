"""Safe JSON parsing and Streamlit-friendly helper functions."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Tuple

REQUIRED_FIELDS = [
    "financial_summary",
    "financial_health_score",
    "spending_analysis",
    "risk_level",
    "top_priorities",
    "budget_recommendations",
    "savings_strategy",
    "next_month_action_plan",
]


def _extract_json_text(raw_text: str) -> str:
    """Extract JSON from plain output or a fenced markdown block."""
    text = raw_text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:
        return text[start : end + 1]

    return text


def _fallback_result(error_message: str) -> Dict[str, Any]:
    """Return a safe schema-compatible fallback."""
    return {
        "financial_summary": (
            "The AI response could not be safely parsed. Review the Python "
            "financial metrics above and try the analysis again."
        ),
        "financial_health_score": 0,
        "spending_analysis": [],
        "risk_level": "HIGH",
        "top_priorities": ["Review the deterministic financial metrics."],
        "budget_recommendations": [
            "Retry the educational AI analysis after checking the model connection."
        ],
        "savings_strategy": [],
        "next_month_action_plan": [],
        "_parse_error": error_message,
    }


def parse_financial_json(raw_text: str) -> Tuple[Dict[str, Any], str | None]:
    """Parse and validate the required FinWise JSON schema without crashing."""
    try:
        cleaned = _extract_json_text(raw_text)
        data = json.loads(cleaned)

        if not isinstance(data, dict):
            raise ValueError("The model returned JSON, but it was not an object.")

        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        data["financial_summary"] = str(data["financial_summary"])
        data["financial_health_score"] = max(
            0, min(100, int(float(data["financial_health_score"])))
        )
        data["risk_level"] = str(data["risk_level"]).upper()

        if data["risk_level"] not in {"LOW", "MEDIUM", "HIGH"}:
            data["risk_level"] = "MEDIUM"

        for field in [
            "spending_analysis",
            "top_priorities",
            "budget_recommendations",
            "savings_strategy",
            "next_month_action_plan",
        ]:
            if not isinstance(data[field], list):
                data[field] = []

        for item in data["spending_analysis"]:
            if not isinstance(item, dict):
                continue
            item.setdefault("category", "")
            item.setdefault("observation", "")
            item.setdefault("recommendation", "")

        return data, None

    except (json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
        return _fallback_result(str(exc)), str(exc)


def score_band(score: int) -> str:
    """Return the assignment's educational score band."""
    if score >= 80:
        return "Strong"
    if score >= 60:
        return "Generally Healthy"
    if score >= 40:
        return "Needs Improvement"
    return "High Attention"


def currency_value(amount: float, currency: str) -> str:
    """Format an amount without making currency conversion claims."""
    return f"{currency} {amount:,.2f}"
