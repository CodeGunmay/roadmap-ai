def get_user_profile():
    print("\n--- Welcome to RoadmapAI ---")
    print("Answer a few questions to generate your personalized roadmap\n")

    name = input("Your name: ")
    branch = input("Your branch (e.g. AI/ML CSE): ")
    year = input("Year completed (e.g. 1): ")
    skills = input("Your current skills (comma separated, e.g. Python, ML basics): ")
    goal = input("Your goal (internship / placement / research): ")
    hours = input("Hours available per day for learning: ")
    months = input("Target timeline in months (e.g. 3): ")

    user_profile = {
        "name": name,
        "branch": branch,
        "year": int(year),
        "current_skills": [s.strip() for s in skills.split(",")],
        "goal": goal,
        "hours_per_day": int(hours),
        "target_months": int(months)
    }

    return user_profile