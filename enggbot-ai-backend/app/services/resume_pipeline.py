from app.services.pdf_service import (
    extract_text_from_pdf
)

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

from app.services.ats_analyzer import (
    analyze_ats
)

def analyze_resume_pdf(file_path):

    text = extract_text_from_pdf(
        file_path
    )

    info = extract_information(text)

    skills = info["skills"]

    role = predict_role(skills)

    gap = analyze_skill_gap(
        skills,
        role
    )

    ats = analyze_ats(
        text,
        role
    )

    roadmap = generate_roadmap(
        role
    )

    return {

        "predicted_role": role,

        "skills_found": skills,

        "ats_score":
        ats["ats_score"],

        "matched_skills":
        ats["matched_skills"],

        "missing_skills":
        gap["missing_skills"],

        "readiness_score":
        gap["readiness_score"],

        "roadmap":
        roadmap["roadmap"]
    }