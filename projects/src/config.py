"""
Configuration for the MediGuide AI application.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model
MODEL_NAME = "gpt-4o-mini"

# Form options
GENDER_OPTIONS = [
    "Male",
    "Female",
    "Other",
    "Prefer not to say"
]

DURATION_OPTIONS = [
    "Less than 1 day",
    "1-3 days",
    "4-7 days",
    "1-2 weeks",
    "More than 2 weeks"
]

LANGUAGE_OPTIONS = [
    "English",
    "Urdu"
]

SYMPTOM_OPTIONS = [
    "Fever",
    "Cough",
    "Headache",
    "Sore throat",
    "Runny nose",
    "Shortness of breath",
    "Chest pain",
    "Fatigue",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Abdominal pain"
]