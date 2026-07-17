KNOWN_SKILLS = [
    "Python",
    "React",
    "JavaScript",
    "Node.js",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "DSA",
    "SQL",
    "Java",
    "C++",
    "FastAPI",
    "MongoDB",
    "HTML",
    "CSS",
    "Git",
    "APIs"
]

KNOWN_ROLES = [
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "AI Engineer",
    "Data Analyst"
]


def extract_skills(text):
    text = text.lower()

    skills = []

    for skill in KNOWN_SKILLS:
        if skill.lower() in text:
            skills.append(skill)

    return list(set(skills))


def infer_role(skills):
    """
    Infer a target role if the user didn't explicitly mention one.
    """

    skill_set = set(skill.lower() for skill in skills)

    if {"python", "machine learning"} <= skill_set:
        return "AI Engineer"

    if {"html", "css", "javascript"} <= skill_set:
        return "Frontend Developer"

    if {"react", "node.js"} <= skill_set:
        return "Full Stack Developer"

    if {"python", "fastapi"} <= skill_set:
        return "Backend Developer"

    if {"sql"} <= skill_set:
        return "Data Analyst"

    return None


def extract_information(message):

    text = message.lower()

    extracted = {
        "skills": [],
        "target_roles": [],
        "weaknesses": []
    }

    # -------------------------
    # Extract Skills
    # -------------------------

    extracted["skills"] = extract_skills(message)

    # -------------------------
    # Extract Target Role
    # -------------------------

    for role in KNOWN_ROLES:
        if role.lower() in text:
            extracted["target_roles"].append(role)

    # Infer role if none mentioned
    if not extracted["target_roles"]:

        inferred = infer_role(extracted["skills"])

        if inferred:
            extracted["target_roles"].append(inferred)

    # -------------------------
    # Weakness Detection
    # -------------------------

    weakness_keywords = [
        "struggle",
        "weak",
        "poor",
        "bad at",
        "difficulty",
        "can't",
        "cannot"
    ]

    if any(word in text for word in weakness_keywords):

        for skill in KNOWN_SKILLS:

            if skill.lower() in text:
                extracted["weaknesses"].append(skill)

    # Remove duplicates

    extracted["skills"] = list(set(extracted["skills"]))
    extracted["target_roles"] = list(set(extracted["target_roles"]))
    extracted["weaknesses"] = list(set(extracted["weaknesses"]))

    return extracted