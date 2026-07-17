IMPORTANT_SKILLS = [

    "Python",
    "React",
    "Machine Learning",
    "SQL",
    "DSA",
    "FastAPI",
    "TensorFlow",
    "Git",
    "MongoDB",
    "JavaScript"

]

def analyze_resume(resume_text):

    detected_skills = []

    missing_skills = []

    for skill in IMPORTANT_SKILLS:

        if skill.lower() in resume_text.lower():

            detected_skills.append(skill)

        else:

            missing_skills.append(skill)

    score = int(
        (
            len(detected_skills)
            /
            len(IMPORTANT_SKILLS)
        ) * 100
    )

    suggestions = []

    if "project" not in resume_text.lower():

        suggestions.append(
            "Add strong projects section."
        )

    if "internship" not in resume_text.lower():

        suggestions.append(
            "Add internships or practical experience."
        )

    if score < 50:

        suggestions.append(
            "Improve technical skill diversity."
        )

    return {

        "resume_score": score,

        "detected_skills": detected_skills,

        "missing_skills": missing_skills,

        "suggestions": suggestions

    }