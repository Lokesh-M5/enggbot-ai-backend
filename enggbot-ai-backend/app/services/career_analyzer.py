from app.services.skill_extractor import (
    extract_information
)

from app.services.role_predictor import (
    predict_role
)

from app.services.skill_gap_engine import (
    analyze_skill_gap
)

from app.services.roadmap_generator import (
    generate_roadmap
)


def analyze_career(resume_text):

    info = extract_information(
    resume_text
)

    skills = info["skills"]

    role = predict_role(
        skills
    )

    gap_analysis = analyze_skill_gap(
        skills,
        role
    )

    roadmap = generate_roadmap(
        role
    )

    return {

        "predicted_role": role,

        "skills_found": skills,

        "readiness_score":
        gap_analysis["readiness_score"],

        "missing_skills":
        gap_analysis["missing_skills"],

        "roadmap":
        roadmap["roadmap"]
    }