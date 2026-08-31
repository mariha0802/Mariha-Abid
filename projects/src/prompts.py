"""
Prompt templates for MediGuide AI.
"""

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate


# System instructions for the AI
SYSTEM_PROMPT = """
You are MediGuide AI, an educational medical guidance assistant.

Important safety rules:
- You are NOT a doctor.
- Do not provide a confirmed diagnosis.
- Provide general educational information only.
- Encourage the user to consult a qualified healthcare professional.
- If symptoms suggest an emergency, clearly advise the user
  to seek emergency medical help immediately.
"""


# Instructions for the JSON response
JSON_SCHEMA_INSTRUCTION = """
Return ONLY valid JSON using this structure:

{
    "summary": "",
    "possible_conditions": [
        {
            "name": "",
            "reason": ""
        }
    ],
    "urgency_level": "",
    "recommended_next_steps": [],
    "questions_for_doctor": [],
    "warning_signs": []
}
"""


# PromptTemplate
ASSESSMENT_PROMPT = PromptTemplate(
    input_variables=[
        "age",
        "gender",
        "symptoms",
        "duration",
        "severity",
        "conditions",
        "medications",
        "notes",
        "language",
        "json_schema"
    ],
    template="""
Patient information:

Age: {age}
Gender: {gender}
Symptoms: {symptoms}
Duration: {duration}
Severity: {severity}/10
Existing medical conditions: {conditions}
Current medications: {medications}
Additional notes: {notes}
Answer language: {language}

Provide educational medical guidance based on this information.

{json_schema}
"""
)


# ChatPromptTemplate
CHAT_ASSESSMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    (
        "human",
        """
Patient information:

Age: {age}
Gender: {gender}
Symptoms: {symptoms}
Duration: {duration}
Severity: {severity}/10
Existing medical conditions: {conditions}
Current medications: {medications}
Additional notes: {notes}
Answer language: {language}

{json_schema}
"""
    )
])