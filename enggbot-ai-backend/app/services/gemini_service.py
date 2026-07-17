import warnings
import os
import traceback

warnings.filterwarnings(
    "ignore",
    category=FutureWarning
)

import google.generativeai as genai

from dotenv import load_dotenv

from app.services.recommendation_engine import analyze_profile
from app.services.memory_service import save_message, get_history
from app.services.vector_store import search_memory
from app.services.skill_extractor import extract_information
from app.services.roadmap_generator import generate_roadmap
from app.services.profile_service import update_profile, get_profile

# ==========================================================
# LOAD ENVIRONMENT
# ==========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found inside .env"
    )

genai.configure(api_key=API_KEY)

generation_config = {

    "temperature": 0.7,

    "top_p": 0.95,

    "top_k": 40,

    "max_output_tokens": 1024,

}

model = genai.GenerativeModel(

    model_name="models/gemini-2.5-flash",

    generation_config=generation_config

)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================


def format_history(history):

    """
    Converts chat history into a clean prompt.
    """

    if not history:
        return "No previous conversation."

    history = history[-10:]

    formatted = []

    for msg in history:

        role = msg.get(
            "role",
            "user"
        )

        content = msg.get(
            "content",
            ""
        )

        formatted.append(
            f"{role}: {content}"
        )

    return "\n".join(formatted)


def format_profile(profile):

    if not profile:
        return "No profile available."

    text = []

    skills = profile.get(
        "skills",
        []
    )

    roles = profile.get(
        "target_roles",
        []
    )

    weaknesses = profile.get(
        "weaknesses",
        []
    )

    text.append(
        f"Skills: {', '.join(skills) if skills else 'None'}"
    )

    text.append(
        f"Target Roles: {', '.join(roles) if roles else 'None'}"
    )

    text.append(
        f"Weaknesses: {', '.join(weaknesses) if weaknesses else 'None'}"
    )

    return "\n".join(text)


def format_analysis(analysis):

    if not analysis:
        return "No career analysis."

    return f"""
Target Role: {analysis.get('target_role')}

Readiness Score:
{analysis.get('readiness_score')}%

Matched Skills:
{', '.join(analysis.get('matched_skills', []))}

Missing Skills:
{', '.join(analysis.get('missing_skills', []))}

Salary:
{analysis.get('salary_range')}

Demand:
{analysis.get('demand')}

Competition:
{analysis.get('competition')}
"""


def format_roadmap(roadmap):

    if not roadmap:
        return "No roadmap generated."

    lines = []

    for item in roadmap:

        title = item.get(
            "title",
            ""
        )

        description = item.get(
            "description",
            ""
        )

        lines.append(
            f"- {title}: {description}"
        )

    return "\n".join(lines)


def build_prompt(

    user_message,

    profile,

    analysis,

    roadmap,

    history,

    memory

):

    return f"""
You are EnggBot.

You are an AI Career Mentor specialized in helping engineering students.

Your personality:

- Professional
- Friendly
- Motivating
- Honest
- Practical

Always answer according to the student's profile.

==============================

Student Profile

{format_profile(profile)}

==============================

Career Analysis

{format_analysis(analysis)}

==============================

Learning Roadmap

{format_roadmap(roadmap)}

==============================

Relevant Memory

{memory}

==============================

Conversation History

{format_history(history)}

==============================

Current User Question

{user_message}

==============================

Instructions

- Answer naturally.
- Do NOT repeat information.
- Give actionable advice.
- Keep responses concise.
- If the student asks career questions,
  use Career Analysis.
- If they ask technical questions,
  explain clearly.
- If they ask roadmap questions,
  use the generated roadmap.
"""
# ==========================================================
# MAIN CHATBOT FUNCTION
# ==========================================================

def generate_response(
    user_id,
    user_message
):
    """
    Main chatbot response generator.
    """

    try:

        # -----------------------------
        # Validate Input
        # -----------------------------

        if not user_message or not user_message.strip():
            return "Please enter a valid message."

        # -----------------------------
        # Load Conversation History
        # -----------------------------

        history = get_history(user_id)

        # -----------------------------
        # Extract User Information
        # -----------------------------

        extracted_data = extract_information(
            user_message
        )

        update_profile(
            user_id,
            extracted_data
        )

        # -----------------------------
        # Load Updated Profile
        # -----------------------------

        profile = get_profile(user_id)

        # -----------------------------
        # Career Analysis
        # -----------------------------

        analysis = analyze_profile(profile)

        roadmap = generate_roadmap(
            analysis
        )

        # -----------------------------
        # Vector Search
        # -----------------------------

        try:

            memory_results = search_memory(
                user_message
            )

            if memory_results:

                memory_text = "\n".join(
                    str(item)
                    for item in memory_results
                )

            else:

                memory_text = "No relevant memory."

        except Exception:

            memory_text = "Memory unavailable."

        # -----------------------------
        # Prompt
        # -----------------------------

        prompt = build_prompt(

            user_message=user_message,

            profile=profile,

            analysis=analysis,

            roadmap=roadmap,

            history=history,

            memory=memory_text

        )

        # -----------------------------
        # Gemini Response
        # -----------------------------

        response = model.generate_content(
            prompt
        )

        if (
            hasattr(response, "text")
            and
            response.text
        ):

            ai_text = response.text.strip()

        else:

            ai_text = (
                "I couldn't generate a response."
            )

        # -----------------------------
        # Save Conversation
        # -----------------------------

        save_message(
            user_id,
            "user",
            user_message
        )

        save_message(
            user_id,
            "assistant",
            ai_text
        )

        return ai_text

    except Exception as e:

        print("\n" + "=" * 80)
        print("FULL GEMINI ERROR")
        traceback.print_exc()
        print("=" * 80 + "\n")

        return f"Gemini Error: {str(e)}"


# ==========================================================
# SIMPLE GEMINI FUNCTION
# Used by Resume Analyzer,
# ATS Scanner,
# Interview,
# Market Analysis
# ==========================================================

def generate_simple_response(
    prompt
):

    try:

        if not prompt:

            return "Prompt is empty."

        response = model.generate_content(
            prompt
        )

        if (
            hasattr(response, "text")
            and
            response.text
        ):

            return response.text.strip()

        return "No response generated."

    except Exception as e:

        print("\n" + "=" * 80)
        print("FULL GEMINI ERROR")
        traceback.print_exc()
        print("=" * 80 + "\n")

        return f"Gemini Error: {str(e)}"