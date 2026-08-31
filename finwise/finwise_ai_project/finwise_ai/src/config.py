"""Central configuration for FinWise AI."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("FINWISE_MODEL", "gpt-4o-mini")
DEFAULT_TEMPERATURE = float(os.getenv("FINWISE_TEMPERATURE", "0.2"))

# The assignment lists nine named categories even though it calls them "ten".
# We preserve the PDF's exact listed category names rather than inventing a
# tenth category that is not present in the source PDF.
EXPENSE_CATEGORIES = [
    "Housing/Rent",
    "Food",
    "Transportation",
    "Utilities",
    "Education",
    "Healthcare",
    "Entertainment",
    "Loan/Debt",
    "Other",
]

FINANCIAL_GOALS = [
    "Save money",
    "Emergency fund",
    "Pay off debt",
    "Vacation",
    "Start a business",
    "Improve budgeting",
]

CURRENCIES = [
    "USD",
    "EUR",
    "GBP",
    "PKR",
    "AED",
    "SAR",
    "CAD",
    "AUD",
]

CACHE_OPTIONS = ["In-memory cache", "SQLite cache"]
