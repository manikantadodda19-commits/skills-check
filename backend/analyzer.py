"""
Analysis Engine — Computes ATS scores, skill comparisons, role matching,
risk assessment, and generates learning roadmaps from parsed resume data.
"""

from skills_db import JOB_ROLES


def compute_ats_score(parsed_data):
    """
    Compute overall ATS score as percentage of required ATS keywords found.
    """
    role_data = JOB_ROLES.get(parsed_data["job_role"], {})
    ats_keywords = set(role_data.get("ats_keywords", []))

    if not ats_keywords:
        return 0

    found = set(parsed_data["found_skills"]) & ats_keywords
    score = int((len(found) / len(ats_keywords)) * 100)
    return min(score, 100)


def compute_section_scores(parsed_data):
    """
    Compute ATS compatibility scores per resume section.
    """
    sections = parsed_data["sections"]
    role_data = JOB_ROLES.get(parsed_data["job_role"], {})
    tech_skills = set(role_data.get("technical_skills", []))
    found_skills = set(parsed_data["found_skills"])

    # Skills Section score — based on how many skills are explicitly listed
    skills_content = sections.get("Skills", "").lower()
    skills_mentioned = sum(1 for s in tech_skills if s.lower() in skills_content)
    skills_score = min(int((skills_mentioned / max(len(tech_skills) * 0.4, 1)) * 100), 100) if "Skills" in sections else 30

    # Projects score — based on section presence and skill mentions in it
    projects_content = sections.get("Projects", "").lower()
    if projects_content:
        proj_mentions = sum(1 for s in found_skills if s.lower() in projects_content)
        projects_score = min(int((proj_mentions / max(len(tech_skills) * 0.2, 1)) * 100), 100)
        projects_score = max(projects_score, 40)
    else:
        projects_score = 20

    # Experience score
    exp_content = sections.get("Experience", "").lower()
    if exp_content:
        exp_mentions = sum(1 for s in found_skills if s.lower() in exp_content)
        experience_score = min(int((exp_mentions / max(len(tech_skills) * 0.2, 1)) * 100), 100)
        experience_score = max(experience_score, 35)
    else:
        experience_score = 15

    # Keyword Density score — based on total keyword mentions
    total_mentions = sum(parsed_data["keyword_counts"].values())
    keyword_score = min(int((total_mentions / max(len(tech_skills), 1)) * 50), 100)
    keyword_score = max(keyword_score, 20)

    # Formatting score — based on having proper sections
    section_count = len(sections)
    formatting_score = min(int((section_count / 5) * 100), 100)
    formatting_score = max(formatting_score, 50)

    def status_label(score):
        if score >= 80:
            return "Strong"
        elif score >= 60:
            return "Moderate"
        elif score >= 40:
            return "Needs Improvement"
        else:
            return "Limited"

    def status_color(score):
        if score >= 80:
            return "green"
        elif score >= 50:
            return "yellow"
        else:
            return "red"

    return [
        {"section": "Skills Section", "score": skills_score, "status": status_label(skills_score), "color": status_color(skills_score), "prefix": "+"},
        {"section": "Projects", "score": projects_score, "status": status_label(projects_score), "color": status_color(projects_score), "prefix": "-" if projects_score < 70 else "+"},
        {"section": "Experience", "score": experience_score, "status": status_label(experience_score), "color": status_color(experience_score), "prefix": "-" if experience_score < 70 else "+"},
        {"section": "Keywords Density", "score": keyword_score, "status": status_label(keyword_score), "color": status_color(keyword_score), "prefix": "+" if keyword_score >= 60 else "-"},
        {"section": "Formatting", "score": formatting_score, "status": status_label(formatting_score), "color": status_color(formatting_score), "prefix": "+"},
    ]


def compute_risk_assessment(ats_score):
    """
    Compute ATS rejection risk based on overall score.
    """
    rejection_pct = 100 - ats_score

    if rejection_pct <= 20:
        level = "Low"
        message = "Your resume has a good chance of passing ATS filters."
    elif rejection_pct <= 40:
        level = "Moderate"
        message = "Your resume has a moderate chance of rejection due to missing keywords."
    else:
        level = "High"
        message = "Your resume is at high risk of ATS rejection. Consider adding more relevant keywords."

    # Pointer position for the scale (0-100, where 0=left/low, 100=right/high)
    pointer_position = rejection_pct

    return {
        "rejection_pct": rejection_pct,
        "level": level,
        "message": message,
        "pointer_position": pointer_position
    }


def compute_keyword_density(parsed_data):
    """
    Compute keyword density for top ATS keywords.
    """
    role_data = JOB_ROLES.get(parsed_data["job_role"], {})
    ats_keywords = role_data.get("ats_keywords", [])
    keyword_counts = parsed_data["keyword_counts"]

    results = []
    for keyword in ats_keywords[:15]:  # Top 15 keywords
        count = keyword_counts.get(keyword, 0)
        if count > 0:
            status = "Good"
            color = "green"
            bar_class = "good"
        else:
            status = "Missing"
            color = "red"
            bar_class = "bad"

        results.append({
            "keyword": keyword,
            "count": count,
            "status": status,
            "color": color,
            "bar_class": bar_class
        })

    # Sort: found keywords first, then missing
    results.sort(key=lambda x: (x["count"] == 0, x["keyword"]))

    # Keywords to include (missing ones)
    missing_keywords = [r["keyword"] for r in results if r["count"] == 0]

    return results, missing_keywords[:6]


def compute_role_matches(parsed_data):
    """
    Compute ATS match scores against all available job roles.
    """
    found_skills = set(parsed_data["found_skills"])
    results = []

    for role_name, role_data in JOB_ROLES.items():
        ats_keywords = set(role_data.get("ats_keywords", []))
        if not ats_keywords:
            continue

        matched = found_skills & ats_keywords
        score = int((len(matched) / len(ats_keywords)) * 100)
        score = min(score, 100)

        if score >= 75:
            icon = "✔"
        elif score >= 50:
            icon = "⚠"
        else:
            icon = "✖"

        results.append({
            "role": role_name,
            "score": score,
            "icon": icon
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def compute_ats_simulator(ats_score, missing_keywords):
    """
    Simulate ATS score improvement if top missing keywords are added.
    """
    # Each missing keyword could add ~3-5% improvement
    simulated_boost = min(len(missing_keywords[:3]) * 5, 20)
    simulated_score = min(ats_score + simulated_boost, 98)

    keywords_text = " + ".join(missing_keywords[:3]) if missing_keywords else "N/A"

    return {
        "original_score": ats_score,
        "simulated_score": simulated_score,
        "keywords_added": keywords_text,
        "insight": f"Incorporating missing keywords and highlighting a project related to {keywords_text} will increase your ATS score."
    }


def compute_skill_comparison(parsed_data):
    """
    Compute skill breakdown comparing resume to industry averages.
    """
    role_data = JOB_ROLES.get(parsed_data["job_role"], {})
    industry_avg = role_data.get("industry_avg", {"technical": 75, "soft": 70, "projects": 72})

    tech_skills = set(role_data.get("technical_skills", []))
    soft_skills = set(role_data.get("soft_skills", []))
    found_tech = set(parsed_data["found_technical"])
    found_soft = set(parsed_data["found_soft"])

    tech_score = int((len(found_tech) / max(len(tech_skills), 1)) * 100)
    soft_score = int((len(found_soft) / max(len(soft_skills), 1)) * 100)

    # Projects score — based on project section and skills referenced
    sections = parsed_data["sections"]
    if "Projects" in sections:
        projects_content = sections["Projects"].lower()
        proj_skills = sum(1 for s in found_tech if s.lower() in projects_content)
        projects_score = min(int((proj_skills / max(len(tech_skills) * 0.15, 1)) * 100), 100)
        projects_score = max(projects_score, 40)
    else:
        projects_score = 25

    # Determine strengths and weaknesses
    strengths = []
    weaknesses = []

    if tech_score >= industry_avg["technical"]:
        strengths.append(", ".join(list(found_tech)[:3]))
    else:
        weaknesses.append("Technical Skills")

    if soft_score >= industry_avg["soft"]:
        if found_soft:
            strengths.append(", ".join(list(found_soft)[:2]))
    else:
        weaknesses.append("Soft Skills")

    missing_areas = parsed_data["missing_technical"][:3]
    if missing_areas:
        weaknesses.extend([s for s in missing_areas if s not in weaknesses])

    # Profile detection
    if tech_score > 70:
        profile = parsed_data["job_role"].replace("Engineer", "").replace("Scientist", "/ Data Science").strip()
        if not profile:
            profile = "Technology"
    else:
        profile = "General"

    return {
        "technical": {"resume": tech_score, "industry": industry_avg["technical"]},
        "soft": {"resume": soft_score, "industry": industry_avg["soft"]},
        "projects": {"resume": projects_score, "industry": industry_avg["projects"]},
        "profile": profile,
        "experience_level": parsed_data["experience_level"],
        "strengths": ", ".join(strengths[:3]) if strengths else "N/A",
        "weaknesses": ", ".join(weaknesses[:3]) if weaknesses else "N/A",
    }


def compute_recommended_role(parsed_data):
    """
    Determine the best-fit job role and provide reasons.
    """
    role_matches = compute_role_matches(parsed_data)
    if not role_matches:
        return None

    best_role = role_matches[0]
    role_name = best_role["role"]
    role_data = JOB_ROLES.get(role_name, {})

    found_skills = set(parsed_data["found_skills"])
    tech_skills = set(role_data.get("technical_skills", []))
    ats_keywords = set(role_data.get("ats_keywords", []))

    found_tech = found_skills & tech_skills
    missing_from_ats = ats_keywords - found_skills

    # Generate reasons
    reasons = []
    top_found = sorted(list(found_tech))[:4]
    for skill in top_found:
        reasons.append(f"Good {skill} proficiency")

    if len(found_tech) >= len(tech_skills) * 0.3:
        reasons.insert(0, f"You have strong skills in {', '.join(top_found[:2])}, aligning well with this role")

    if "Projects" in parsed_data["sections"]:
        reasons.append("Projects involving relevant experience")

    if not reasons:
        reasons.append("Your skill profile shows potential for this role")

    # Missing skill tags
    missing_tags = sorted(list(missing_from_ats))[:6]

    return {
        "role": role_name,
        "description": role_data.get("description", ""),
        "score": best_role["score"],
        "reasons": reasons[:5],
        "missing_tags": missing_tags,
        "sample_jobs": role_data.get("sample_jobs", []),
        "all_matches": role_matches
    }


def compute_learning_roadmap(parsed_data):
    """
    Generate a 90-day learning roadmap based on skill gaps.
    """
    found_skills = set(parsed_data["found_skills"])
    missing_technical = list(parsed_data["missing_technical"])
    missing_soft = list(parsed_data["missing_soft"])
    keyword_counts = parsed_data["keyword_counts"]

    # Prioritize: skills with 0 mentions first, then low mentions
    def priority_sort(skill):
        return keyword_counts.get(skill, 0)

    missing_technical.sort(key=priority_sort)

    # Split into 3 phases
    phase_1_skills = missing_technical[:3]  # Most critical gaps
    phase_2_skills = missing_technical[3:6]
    phase_3_skills = missing_technical[6:9]

    # Compute progress for found skills in each category
    role_data = JOB_ROLES.get(parsed_data["job_role"], {})
    all_tech = set(role_data.get("technical_skills", []))

    # Classify found skills into proficiency levels based on mention count
    def skill_progress(skill):
        count = keyword_counts.get(skill, 0)
        if count >= 5:
            return 90
        elif count >= 3:
            return 70
        elif count >= 1:
            return 50
        else:
            return 0

    # Phase 1: Core Skills (Days 1-30) — focus on strengthening existing + top gaps
    phase1_items = []
    strong_skills = [s for s in found_skills if keyword_counts.get(s, 0) >= 3 and s in all_tech][:2]
    for s in strong_skills:
        phase1_items.append({"skill": s, "status": "done", "progress": skill_progress(s)})
    for s in phase_1_skills[:2]:
        phase1_items.append({"skill": s, "status": "pending", "progress": max(skill_progress(s), 10)})

    phase1_overall = int(sum(item["progress"] for item in phase1_items) / max(len(phase1_items), 1))

    # Phase 2: Intermediate (Days 31-60)
    phase2_items = []
    for s in phase_2_skills[:3]:
        phase2_items.append({"skill": s, "status": "pending", "progress": max(skill_progress(s), 5)})

    if not phase2_items:
        # Use some missing soft skills
        for s in missing_soft[:2]:
            phase2_items.append({"skill": s, "status": "pending", "progress": 10})

    phase2_overall = int(sum(item["progress"] for item in phase2_items) / max(len(phase2_items), 1))

    # Phase 3: Advanced (Days 61-90)
    phase3_items = []
    for s in phase_3_skills[:3]:
        phase3_items.append({"skill": s, "status": "pending", "progress": 0})

    if not phase3_items:
        phase3_items.append({"skill": "Build Portfolio Project", "status": "pending", "progress": 0})
        phase3_items.append({"skill": "Get Certified", "status": "pending", "progress": 0})

    phase3_overall = int(sum(item["progress"] for item in phase3_items) / max(len(phase3_items), 1))

    return {
        "phase_1": {
            "title": "30 Days",
            "subtitle": "Core Skills",
            "items": phase1_items,
            "overall_progress": phase1_overall
        },
        "phase_2": {
            "title": "31–60 Days",
            "subtitle": "Intermediate",
            "items": phase2_items,
            "overall_progress": phase2_overall
        },
        "phase_3": {
            "title": "61–90 Days",
            "subtitle": "Advanced",
            "items": phase3_items,
            "overall_progress": phase3_overall
        }
    }


def generate_ai_insight(parsed_data, ats_score):
    """
    Generate a context-aware AI insight message.
    """
    missing = parsed_data["missing_technical"][:3]
    found = parsed_data["found_technical"][:3]

    if ats_score >= 80:
        insight = f"Your resume is well-aligned with the target role. Focus on strengthening {', '.join(missing[:2])} to reach a top-tier score."
    elif ats_score >= 60:
        top_missing = ', '.join(missing[:2]) if missing else 'relevant certifications'
        insight = f"Incorporating {top_missing} and highlighting related projects will significantly boost your ATS compatibility."
    else:
        top_missing = ', '.join(missing[:3]) if missing else 'key industry skills'
        insight = f"Your resume needs significant improvements. Prioritize learning {top_missing} and adding relevant project experience."

    return insight


def run_full_analysis(parsed_data):
    """
    Run the complete analysis pipeline and return all results.
    """
    ats_score = compute_ats_score(parsed_data)
    section_scores = compute_section_scores(parsed_data)
    risk = compute_risk_assessment(ats_score)
    keyword_density, missing_keywords = compute_keyword_density(parsed_data)
    role_matches = compute_role_matches(parsed_data)
    simulator = compute_ats_simulator(ats_score, missing_keywords)
    skill_comparison = compute_skill_comparison(parsed_data)
    recommended_role = compute_recommended_role(parsed_data)
    roadmap = compute_learning_roadmap(parsed_data)
    insight = generate_ai_insight(parsed_data, ats_score)

    return {
        "ats_score": ats_score,
        "section_scores": section_scores,
        "risk_assessment": risk,
        "keyword_density": keyword_density,
        "missing_keywords": missing_keywords,
        "role_matches": role_matches,
        "simulator": simulator,
        "skill_comparison": skill_comparison,
        "recommended_role": recommended_role,
        "learning_roadmap": roadmap,
        "ai_insight": insight,
        "parsed_data": {
            "found_skills": parsed_data["found_skills"],
            "missing_skills": parsed_data["missing_skills"],
            "found_technical": parsed_data["found_technical"],
            "found_soft": parsed_data["found_soft"],
            "missing_technical": parsed_data["missing_technical"],
            "missing_soft": parsed_data["missing_soft"],
            "experience_level": parsed_data["experience_level"],
            "job_role": parsed_data["job_role"],
            "sections_detected": list(parsed_data["sections"].keys()),
        }
    }
