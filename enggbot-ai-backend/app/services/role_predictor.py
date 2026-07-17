from app.data.role_data import ROLE_SKILLS


def predict_role(skills):
    """
    Predict the most suitable role based on the user's skills.
    """

    if not skills:
        return "General Software Engineer"

    user_skills = {
        skill.strip().lower()
        for skill in skills
        if skill
    }

    best_role = None
    best_score = -1

    for role, required_skills in ROLE_SKILLS.items():

        required = {
            skill.lower()
            for skill in required_skills
        }

        score = len(
            user_skills.intersection(required)
        )

        if score > best_score:
            best_score = score
            best_role = role

    if best_score == 0:
        return "General Software Engineer"

    return best_role