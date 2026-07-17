from app.services.role_data import ROLE_DATA


def _normalize_role(role: str):
    """
    Returns the correct ROLE_DATA key
    irrespective of case or extra spaces.
    """

    if not role:
        return None

    role = role.strip().lower()

    for existing_role in ROLE_DATA.keys():
        if existing_role.lower() == role:
            return existing_role

    return None


def analyze_profile(profile):
    """
    Analyze the student's profile and compare
    it with the selected target role.
    """

    if not profile:
        return {}

    target_roles = profile.get("target_roles", [])
    user_skills = profile.get("skills", [])
    weaknesses = profile.get("weaknesses", [])

    if not target_roles:
        return {
            "target_role": None,
            "matched_skills": [],
            "missing_skills": [],
            "readiness_score": 0,
            "salary_range": None,
            "demand": None,
            "competition": None,
            "weaknesses": weaknesses,
            "roadmap": []
        }

    # Normalize skills
    user_skill_set = {
        skill.strip().lower()
        for skill in user_skills
    }

    analysis = None

    # Try every target role until a valid one is found
    for role in target_roles:

        normalized_role = _normalize_role(role)

        if not normalized_role:
            continue

        role_info = ROLE_DATA[normalized_role]

        required_skills = role_info.get("skills", [])

        matched_skills = []
        missing_skills = []

        for skill in required_skills:

            if skill.lower() in user_skill_set:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        readiness_score = (
            round(
                (len(matched_skills) / len(required_skills)) * 100
            )
            if required_skills
            else 0
        )

        roadmap = [
            {
                "step": f"Learn {skill}"
            }
            for skill in missing_skills
        ]

        analysis = {
            "target_role": normalized_role,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "readiness_score": readiness_score,
            "salary_range": role_info.get("salary_range"),
            "demand": role_info.get("demand"),
            "competition": role_info.get("competition"),
            "weaknesses": weaknesses,
            "roadmap": roadmap
        }

        break

    if analysis is None:

        return {
            "target_role": None,
            "matched_skills": [],
            "missing_skills": [],
            "readiness_score": 0,
            "salary_range": None,
            "demand": None,
            "competition": None,
            "weaknesses": weaknesses,
            "roadmap": []
        }

    return analysis