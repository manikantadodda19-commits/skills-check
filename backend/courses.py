"""
Course Recommendation Engine — Suggests courses based on skill gaps.
"""

from skills_db import COURSE_CATALOG, JOB_ROLES


def get_recommended_courses(parsed_data, max_courses=9):
    """
    Returns a list of recommended courses based on missing skills,
    prioritized by relevance to the target job role.
    """
    job_role = parsed_data["job_role"]
    missing_skills = parsed_data["missing_skills"]
    missing_technical = parsed_data["missing_technical"]
    keyword_counts = parsed_data["keyword_counts"]

    role_data = JOB_ROLES.get(job_role, {})
    ats_keywords = set(role_data.get("ats_keywords", []))

    # Priority: missing ATS keywords first, then other missing skills
    priority_missing = []
    other_missing = []

    for skill in missing_technical:
        if skill in ats_keywords:
            priority_missing.append(skill)
        else:
            other_missing.append(skill)

    # Also add any missing ATS keywords not in technical skills
    for skill in missing_skills:
        if skill in ats_keywords and skill not in priority_missing:
            priority_missing.append(skill)

    # Combine: ATS-critical first, then other gaps
    ordered_skills = priority_missing + other_missing

    # Also consider: skills with low mentions (improvement opportunities)
    low_mention_skills = [
        skill for skill in parsed_data["found_skills"]
        if keyword_counts.get(skill, 0) <= 1 and skill in COURSE_CATALOG
    ]

    courses = []
    seen_titles = set()

    # First pass: courses for missing skills
    for skill in ordered_skills:
        if len(courses) >= max_courses:
            break
        if skill in COURSE_CATALOG:
            course = COURSE_CATALOG[skill].copy()
            course["skill"] = skill
            course["priority"] = "high"
            course["reason"] = f"Missing from your resume — critical for {job_role}"
            if course["title"] not in seen_titles:
                courses.append(course)
                seen_titles.add(course["title"])

    # Second pass: courses for low-mention skills
    for skill in low_mention_skills:
        if len(courses) >= max_courses:
            break
        if skill in COURSE_CATALOG:
            course = COURSE_CATALOG[skill].copy()
            course["skill"] = skill
            course["priority"] = "medium"
            course["reason"] = f"Mentioned only {keyword_counts.get(skill, 0)} time(s) — strengthen this skill"
            if course["title"] not in seen_titles:
                courses.append(course)
                seen_titles.add(course["title"])

    return courses
