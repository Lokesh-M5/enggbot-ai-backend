from app.data.role_data import ROLE_SKILLS


def analyze_skill_gap(user_skills, target_role):
    """
    Compare user skills with required skills
    for the selected career role.
    """

    required_skills = ROLE_SKILLS.get(
        target_role,
        []
    )

    if not required_skills:

        return {
            "target_role": target_role,
            "readiness_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "total_required": 0
        }

    user_skills = {
        skill.lower().strip()
        for skill in user_skills
        if skill
    }

    matched = []
    missing = []

    for skill in required_skills:

        if skill.lower() in user_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    readiness = round(
        (len(matched) / len(required_skills)) * 100
    )

    return {

        "target_role": target_role,

        "readiness_score": readiness,

        "matched_skills": matched,

        "missing_skills": missing,

        "total_required": len(required_skills)

    }