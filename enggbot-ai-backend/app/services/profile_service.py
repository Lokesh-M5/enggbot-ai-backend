"""
Profile Service

Maintains a student's profile during the current backend session.
This can later be replaced by PostgreSQL without changing the API.
"""

student_profiles = {}

DEFAULT_PROFILE = {
    "skills": [],
    "interests": [],
    "weaknesses": [],
    "target_roles": []
}


def _clean_values(values):
    """
    Converts incoming values into a clean list.
    Removes duplicates, empty strings and whitespace.
    """

    if values is None:
        return []

    # Convert single string into list
    if isinstance(values, str):
        values = [values]

    cleaned = []
    seen = set()

    for value in values:

        if value is None:
            continue

        value = str(value).strip()

        if value == "":
            continue

        key = value.lower()

        if key not in seen:
            cleaned.append(value)
            seen.add(key)

    return cleaned


def update_profile(user_id, extracted_data):
    """
    Merge newly extracted information into
    the user's existing profile.
    """

    if user_id not in student_profiles:

        student_profiles[user_id] = {
            "skills": [],
            "interests": [],
            "weaknesses": [],
            "target_roles": []
        }

    profile = student_profiles[user_id]

    for field in DEFAULT_PROFILE.keys():

        incoming_values = extracted_data.get(field, [])

        incoming_values = _clean_values(incoming_values)

        existing = {
            item.lower(): item
            for item in profile[field]
        }

        for value in incoming_values:

            if value.lower() not in existing:
                profile[field].append(value)
                existing[value.lower()] = value


def get_profile(user_id):
    """
    Returns a complete profile.
    Even a new user always gets
    the same structure.
    """

    profile = student_profiles.get(user_id)

    if profile is None:
        return DEFAULT_PROFILE.copy()

    return {
        "skills": list(profile["skills"]),
        "interests": list(profile["interests"]),
        "weaknesses": list(profile["weaknesses"]),
        "target_roles": list(profile["target_roles"])
    }


def reset_profile(user_id):
    """
    Clears a user's profile.
    Useful for testing or future account reset.
    """

    if user_id in student_profiles:
        del student_profiles[user_id]