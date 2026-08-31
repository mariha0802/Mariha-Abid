"""
Utility functions for MediGuide AI.
"""

import json


def safe_json_parse(raw_output):
    """
    Safely convert the AI response into a Python dictionary.

    Returns:
        dict: If valid JSON is received.
        None: If the response is not valid JSON.
    """

    try:
        cleaned_output = raw_output.strip()

        # Remove Markdown JSON code fences if the AI adds them
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output[7:]

        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output[:-3]

        cleaned_output = cleaned_output.strip()

        return json.loads(cleaned_output)

    except json.JSONDecodeError:
        return None