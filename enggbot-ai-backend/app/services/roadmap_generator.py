"""
Roadmap Generator

Generates a structured learning roadmap
based on the recommendation engine output.
"""


def generate_roadmap(analysis):
    """
    Creates a roadmap from the career analysis.

    Parameters
    ----------
    analysis : dict

    Returns
    -------
    list
    """

    if not analysis:
        return []

    missing_skills = analysis.get("missing_skills", [])
    target_role = analysis.get("target_role")

    if not target_role:
        return []

    roadmap = []

    roadmap.append({
        "phase": "Foundation",
        "title": f"Become a {target_role}",
        "description": f"Follow this roadmap to become a successful {target_role}."
    })

    for index, skill in enumerate(missing_skills, start=1):

        roadmap.append({
            "phase": f"Step {index}",
            "title": f"Learn {skill}",
            "description": (
                f"Master {skill} through structured courses, "
                "practice projects, and coding exercises."
            )
        })

    roadmap.append({
        "phase": "Projects",
        "title": "Build Portfolio Projects",
        "description": (
            "Apply your skills by building real-world projects "
            "and uploading them to GitHub."
        )
    })

    roadmap.append({
        "phase": "Interview Preparation",
        "title": "Prepare for Interviews",
        "description": (
            "Practice DSA, aptitude, behavioral questions, "
            "resume building, and mock interviews."
        )
    })

    roadmap.append({
        "phase": "Job Applications",
        "title": "Apply for Jobs",
        "description": (
            "Apply through LinkedIn, Naukri, Wellfound, "
            "company career pages, and referrals."
        )
    })

    return roadmap