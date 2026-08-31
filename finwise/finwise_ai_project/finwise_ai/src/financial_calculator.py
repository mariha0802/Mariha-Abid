"""Deterministic financial calculations.

No LLM calls belong in this module. For identical inputs, the outputs are
identical and reproducible.
"""

from __future__ import annotations

from typing import Mapping


def _safe_ratio(numerator: float, denominator: float) -> float:
    """Return numerator/denominator, or 0 when the denominator is zero."""
    if denominator == 0:
        return 0.0
    return numerator / denominator


def calculate_financial_metrics(
    monthly_income: float,
    expenses: Mapping[str, float],
    savings: float,
) -> dict:
    """Calculate the assignment's core financial metrics."""
    income = max(float(monthly_income), 0.0)
    savings_value = max(float(savings), 0.0)

    cleaned_expenses = {
        str(category): max(float(amount), 0.0)
        for category, amount in expenses.items()
    }

    total_expenses = sum(cleaned_expenses.values())
    remaining_income = income - total_expenses
    savings_ratio = _safe_ratio(savings_value, income) * 100
    expense_ratio = _safe_ratio(total_expenses, income) * 100

    debt = cleaned_expenses.get("Loan/Debt", 0.0)
    debt_burden = _safe_ratio(debt, income) * 100

    preliminary_score = calculate_preliminary_score(
        monthly_income=income,
        total_expenses=total_expenses,
        remaining_income=remaining_income,
        savings=savings_value,
        debt=debt,
    )

    return {
        "total_expenses": round(total_expenses, 2),
        "remaining_income": round(remaining_income, 2),
        "savings_ratio": round(savings_ratio, 2),
        "expense_ratio": round(expense_ratio, 2),
        "debt_burden": round(debt_burden, 2),
        "preliminary_score": preliminary_score,
        "expense_breakdown": cleaned_expenses,
    }


def calculate_preliminary_score(
    monthly_income: float,
    total_expenses: float,
    remaining_income: float,
    savings: float,
    debt: float,
) -> int:
    """Return a transparent educational 0-100 heuristic.

    The PDF specifies the factors but does not specify numeric weights.
    This implementation uses:
      - 35% savings
      - 30% leftover income
      - 20% expense ratio
      - 15% debt burden

    Savings is normalized against a 30% monthly savings target and leftover
    income against a 75% positive-balance ceiling. These are educational
    scoring rules, not professional financial standards.
    """
    if monthly_income <= 0:
        return 0

    savings_ratio = _safe_ratio(savings, monthly_income)
    leftover_ratio = _safe_ratio(max(remaining_income, 0.0), monthly_income)
    expense_ratio = _safe_ratio(total_expenses, monthly_income)
    debt_ratio = _safe_ratio(debt, monthly_income)

    savings_component = min(max(savings_ratio, 0.0) / 0.30, 1.0) * 35
    leftover_component = min(max(leftover_ratio, 0.0) / 0.75, 1.0) * 30
    expense_component = max(0.0, 1.0 - expense_ratio) * 20
    debt_component = max(0.0, 1.0 - debt_ratio) * 15

    score = savings_component + leftover_component + expense_component + debt_component
    return max(0, min(100, round(score)))


def educational_risk_level(
    monthly_income: float,
    total_expenses: float,
    debt: float,
    remaining_income: float,
) -> str:
    """Give a deterministic educational risk signal used as a prompt hint."""
    if monthly_income <= 0:
        return "HIGH"

    expense_ratio = total_expenses / monthly_income
    debt_ratio = debt / monthly_income

    if expense_ratio > 1 or remaining_income < 0:
        return "HIGH"
    if debt_ratio >= 0.40 or remaining_income <= 0:
        return "MEDIUM"
    return "LOW"
