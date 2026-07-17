from app.services.gemini_service import (
    generate_simple_response
)


def review_resume(resume_text):

    if not resume_text.strip():

        return "Resume text is empty."

    prompt = f"""
You are an expert Resume Reviewer,
ATS Specialist,
Career Coach,
and Hiring Manager.

Analyze the following resume professionally.

Return the response using Markdown.

# Resume Score
Give a score out of 100.

# ATS Score
Give a score out of 100.

# Strengths
List strong points.

# Weaknesses
Mention weaknesses honestly.

# Missing Skills
Mention skills missing for better placements.

# Recommended Projects
Suggest 3 practical projects.

# Certifications
Suggest useful certifications.

# Resume Improvements
Suggest formatting and content improvements.

# Suggested Career Roles
Recommend suitable job roles.

# Final Verdict
Summarize the resume in 3-4 sentences.

Resume:

-----------------------

{resume_text}

-----------------------

Keep the response concise,
professional,
and practical.
"""

    return generate_simple_response(
        prompt
    )