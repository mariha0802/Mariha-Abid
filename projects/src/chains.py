"""
LangChain logic for MediGuide AI.
"""

from langchain_openai import ChatOpenAI
from langchain_classic.chains import LLMChain

from .config import MODEL_NAME
from .prompts import CHAT_ASSESSMENT_PROMPT


# =========================================================
# CREATE LANGUAGE MODEL
# =========================================================

def create_llm(api_key=None):
    """
    Create the OpenAI chat model.

    If the user provides an API key, use that key.
    Otherwise, ChatOpenAI can use the key from the
    environment/.env file.
    """

    if api_key:
        llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0,
            api_key=api_key
        )
    else:
        llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0
        )

    return llm


# =========================================================
# CREATE ASSESSMENT CHAIN
# =========================================================

def create_assessment_chain():
    """
    Create and return the reusable medical assessment chain.
    """

    llm = create_llm()

    chain = LLMChain(
        llm=llm,
        prompt=CHAT_ASSESSMENT_PROMPT
    )

    return chain


# =========================================================
# RUN NORMAL ASSESSMENT
# =========================================================


def run_assessment(
    age,
    gender,
    symptoms,
    duration,
    severity,
    conditions,
    medications,
    notes,
    language,
    api_key=None
):
    """
    Send patient information to the AI assessment chain.
    """

    llm = create_llm(api_key)

    chain = LLMChain( 
    llm=llm,
    prompt=CHAT_ASSESSMENT_PROMPT
)

    # Convert the symptom list into readable text
    symptoms_text = ", ".join(symptoms)

    response = chain.invoke(
        {
            "age": age,
            "gender": gender,
            "symptoms": symptoms_text,
            "duration": duration,
            "severity": severity,
            "conditions": conditions,
            "medications": medications,
            "notes": notes,
            "language": language,
            "json_schema": """
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
        }
    )

    return response


# =========================================================
# STREAM AI RESPONSE
# =========================================================

def stream_assessment(
    age,
    gender,
    symptoms,
    duration,
    severity,
    conditions,
    medications,
    notes,
    language,
    api_key = None

):
    """
    Stream the AI response piece by piece.

    Instead of waiting for the complete response,
    this function receives smaller chunks from the AI.
    """

    # Create the language model
    llm = create_llm(api_key)

    # Convert symptoms list into text
    symptoms_text = ", ".join(symptoms)

    # Prepare information for the prompt
    inputs = {
        "age": age,
        "gender": gender,
        "symptoms": symptoms_text,
        "duration": duration,
        "severity": severity,
        "conditions": conditions,
        "medications": medications,
        "notes": notes,
        "language": language,
        "json_schema": """
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
    }

    # Create System + Human messages
    messages = CHAT_ASSESSMENT_PROMPT.format_messages(
        **inputs
    )

    # Stream the response
    for chunk in llm.stream(messages):

        if chunk.content:
            yield chunk.content