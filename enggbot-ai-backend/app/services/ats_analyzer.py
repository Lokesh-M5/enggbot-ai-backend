def ats_check(text):

    score = 50

    feedback = []

    if "skills" in text.lower():
        score += 10

    if "education" in text.lower():
        score += 10

    if "experience" in text.lower():
        score += 10

    if len(text) > 1000:
        score += 20

    if score > 100:
        score = 100

    if score < 80:

        feedback.append(
            "Add more keywords."
        )

    return {

        "ats_score": score,

        "feedback": feedback

    }