from app.services.gemini_service import (
    generate_simple_response
)

QUESTIONS = {

    "Python": [
        "What is a Python decorator?",
        "Explain list comprehension in Python.",
        "Difference between list and tuple?"
    ],

    "React": [
        "What is Virtual DOM?",
        "Difference between State and Props?",
        "Explain React Hooks."
    ],

    "Machine Learning": [
        "What is Overfitting?",
        "Difference between Supervised and Unsupervised Learning?",
        "Explain Bias vs Variance."
    ]

}


def get_questions(skill):
    """
    Return interview questions for a skill.
    """

    return QUESTIONS.get(
        skill,
        [
            "Tell me about yourself."
        ]
    )


def evaluate_answer(answer):
    """
    Evaluate a candidate's interview answer.
    """

    if not answer or not answer.strip():

        return {
            "evaluation": "No answer provided."
        }

    prompt = f"""
You are a Senior Software Engineer conducting a technical interview.

Evaluate the candidate's answer professionally.

Candidate Answer:

{answer}

Return your response using Markdown.

# Score
Give a score out of 100.

# Strengths

# Weaknesses

# Missing Concepts

# Improvement Suggestions

# Ideal Answer Summary

Be constructive, concise and interview-focused.
"""

    try:

        evaluation = generate_simple_response(
            prompt
        )

        return {
            "evaluation": evaluation
        }

    except Exception as e:

        return {
            "evaluation": "Unable to evaluate answer.",
            "error": str(e)
        }