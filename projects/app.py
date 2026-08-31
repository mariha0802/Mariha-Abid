"""
MediGuide AI

AI-Powered Medical Symptom Assessment
and Patient Guidance Assistant.
"""

import streamlit as st

from src.config import (
    GENDER_OPTIONS,
    DURATION_OPTIONS,
    LANGUAGE_OPTIONS,
    SYMPTOM_OPTIONS,
    MODEL_NAME
)
# =========================================================
# API KEY GATE
# =========================================================

if "api_key_verified" not in st.session_state:
    st.session_state.api_key_verified = False

if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""


# Show API key screen if user has not entered a key
if not st.session_state.api_key_verified:

    st.title("🩺 MediGuide AI")

    st.subheader("🔐 API Key Required")

    st.info(
        "Please enter your OpenAI API key to access MediGuide AI."
    )

    st.warning(
        "Your API key is used only for your current session "
        "and is not saved by this application."
    )

    api_key = st.text_input(
        "Enter your OpenAI API Key",
        type="password",
        placeholder="sk-..."
    )

    if st.button(
        "Continue to MediGuide AI",
        type="primary"
    ):

        if not api_key.strip():

            st.error(
                "Please enter your OpenAI API key first."
            )

        else:

            st.session_state.user_api_key = api_key.strip()
            st.session_state.api_key_verified = True

            st.rerun()

    st.stop()
    
from src.chains import (
    run_assessment,
    stream_assessment
)
from src.utils import safe_json_parse


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🩺",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🩺 MediGuide AI")

    st.write(
        "AI-Powered Medical Symptom Assessment "
        "and Patient Guidance Assistant"
    )

    st.divider()

    st.subheader("⚙️ Model Configuration")

    st.write(f"Model: `{MODEL_NAME}`")

    st.divider()

    st.subheader("🌐 Language")

    language = st.selectbox(
        "Select answer language",
        LANGUAGE_OPTIONS
    )

    st.divider()

    st.warning(
        """
        ⚠️ Medical Disclaimer

        MediGuide AI is an educational AI prototype.
        It is NOT a doctor and does NOT provide a confirmed
        medical diagnosis or replace professional medical care.

        Always consult a qualified healthcare professional.
        If you have an emergency, seek emergency medical help
        immediately.
        """
    )


# =========================================================
# MAIN PAGE
# =========================================================

st.title("🩺 MediGuide AI")

st.subheader(
    "AI-Powered Medical Symptom Assessment "
    "and Patient Guidance Assistant"
)

st.info(
    "Enter your basic information and symptoms below. "
    "The system will use this information to generate "
    "general educational guidance."
)


# =========================================================
# MEDICAL SAFETY WARNING
# =========================================================

st.warning(
    "⚠️ This application is for educational purposes only. "
    "It does not provide a confirmed diagnosis. "
    "Please consult a qualified healthcare professional "
    "for medical advice."
)


# =========================================================
# PATIENT ASSESSMENT FORM
# =========================================================

st.header("👤 Patient Information")

with st.form("medical_assessment_form"):

    # -----------------------------------------------------
    # Basic information
    # -----------------------------------------------------

    age = st.text_input(
        "Age",
        placeholder="Enter your age"
    )

    gender = st.selectbox(
        "Gender",
        GENDER_OPTIONS
    )

    # -----------------------------------------------------
    # Symptoms
    # -----------------------------------------------------

    st.subheader("🩺 Symptoms")

    symptoms = st.multiselect(
        "Select your symptoms",
        SYMPTOM_OPTIONS
    )

    additional_symptoms = st.text_area(
        "Other symptoms",
        placeholder="Describe any other symptoms..."
    )

    # -----------------------------------------------------
    # Duration and severity
    # -----------------------------------------------------

    duration = st.selectbox(
        "How long have you had these symptoms?",
        DURATION_OPTIONS
    )

    severity = st.slider(
        "How severe are your symptoms?",
        min_value=1,
        max_value=10,
        value=5
    )

    # -----------------------------------------------------
    # Medical history
    # -----------------------------------------------------

    st.subheader("📋 Medical History")

    conditions = st.text_area(
        "Existing medical conditions",
        placeholder=(
            "Example: diabetes, asthma, "
            "high blood pressure..."
        )
    )

    medications = st.text_area(
        "Current medications",
        placeholder=(
            "List any medications you currently take..."
        )
    )

    notes = st.text_area(
        "Additional notes",
        placeholder=(
            "Add any other information you think "
            "is important..."
        )
    )

    # -----------------------------------------------------
    # Submit button
    # -----------------------------------------------------

    submitted = st.form_submit_button(
        "🔍 Assess Symptoms"
    )

    if submitted:


# =========================================================
# FORM SUBMISSION
# =========================================================


    # -----------------------------------------------------
    # Validate symptoms
    # -----------------------------------------------------

     if not symptoms and not additional_symptoms.strip():

        st.error(
            "Please provide at least one symptom before "
            "submitting the assessment."
        )

    else:

        # -------------------------------------------------
        # Combine selected and additional symptoms
        # -------------------------------------------------

        all_symptoms = list(symptoms)

        if additional_symptoms.strip():

            all_symptoms.append(
                additional_symptoms.strip()
            )

        # -------------------------------------------------
        # Show loading message
        # -------------------------------------------------

        with st.spinner(
            "🤖 Analyzing your information..."
        ):

            try:

                # -----------------------------------------
                # Send information to LangChain
                # -----------------------------------------

                response = run_assessment(
                    age=age,
                    gender=gender,
                    symptoms=all_symptoms,
                    duration=duration,
                    severity=severity,
                    conditions=conditions,
                    medications=medications,
                    notes=notes,
                    language=language
                )

                # -----------------------------------------
                # Get AI response
                # -----------------------------------------

                raw_output = response["text"]

                # -----------------------------------------
                # Convert JSON text to Python dictionary
                # -----------------------------------------

                result = safe_json_parse(
                    raw_output
                )

                # -----------------------------------------
                # Check JSON
                # -----------------------------------------

                if result is None:

                    st.error(
                        "The AI returned an unexpected "
                        "response. Please try again."
                    )

                else:

                    st.success(
                        "Assessment completed successfully."
                    )

                    # =====================================
                    # ASSESSMENT RESULTS
                    # =====================================

                    st.header("📋 Assessment Results")

                    # -------------------------------------
                    # Summary
                    # -------------------------------------

                    st.subheader("📝 Summary")

                    st.write(
                        result.get(
                            "summary",
                            "No summary available."
                        )
                    )

                    # -------------------------------------
                    # Urgency
                    # -------------------------------------

                    st.subheader("🚦 Urgency Level")

                    st.write(
                        result.get(
                            "urgency_level",
                            "Not specified"
                        )
                    )

                    # -------------------------------------
                    # Possible conditions
                    # -------------------------------------

                    st.subheader(
                        "🔎 Possible Conditions"
                    )

                    possible_conditions = result.get(
                        "possible_conditions",
                        []
                    )

                    if possible_conditions:

                        for condition in possible_conditions:

                            st.write(
                                f"**{condition.get('name', 'Unknown')}**"
                            )

                            st.write(
                                condition.get(
                                    "reason",
                                    "No explanation provided."
                                )
                            )

                    else:

                        st.write(
                            "No possible conditions were provided."
                        )

                    # -------------------------------------
                    # Recommended next steps
                    # -------------------------------------

                    st.subheader(
                        "✅ Recommended Next Steps"
                    )

                    next_steps = result.get(
                        "recommended_next_steps",
                        []
                    )

                    if next_steps:

                        for step in next_steps:

                            st.write(
                                f"• {step}"
                            )

                    else:

                        st.write(
                            "No next steps were provided."
                        )

                    # -------------------------------------
                    # Questions for doctor
                    # -------------------------------------

                    st.subheader(
                        "👨‍⚕️ Questions to Ask Your Doctor"
                    )

                    doctor_questions = result.get(
                        "questions_for_doctor",
                        []
                    )

                    if doctor_questions:

                        for question in doctor_questions:

                            st.write(
                                f"• {question}"
                            )

                    else:

                        st.write(
                            "No questions were provided."
                        )

                    # -------------------------------------
                    # Warning signs
                    # -------------------------------------

                    st.subheader(
                        "⚠️ Warning Signs"
                    )

                    warning_signs = result.get(
                        "warning_signs",
                        []
                    )

                    if warning_signs:

                        for warning in warning_signs:

                            st.write(
                                f"• {warning}"
                            )

                    else:

                        st.write(
                            "No warning signs were provided."
                        )

            except Exception as e:

                st.error(
                    "Something went wrong while generating "
                    "the assessment. Please try again."
                )

                st.caption(
                    f"Technical details: {str(e)}"
                )