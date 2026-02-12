"""
Resume Parser — Extracts text, skills, sections, experience level, and keyword counts from resumes.
"""

import re
import os
from collections import Counter
from skills_db import JOB_ROLES, SKILL_ALIASES


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    import PyPDF2
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    import docx
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def extract_text(file_path):
    """Extract text from a resume file (PDF or DOCX)."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def normalize_text(text):
    """Lowercase and clean text for matching."""
    text = text.lower()
    text = re.sub(r'[^\w\s/#+\-.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def detect_skills(text, job_role):
    """
    Detect skills present in the resume text.
    Returns found_skills (set), missing_skills (set), and keyword_counts (dict).
    """
    normalized = normalize_text(text)
    role_data = JOB_ROLES.get(job_role, {})
    all_required = set(role_data.get("technical_skills", []) + role_data.get("soft_skills", []))
    ats_keywords = set(role_data.get("ats_keywords", []))

    # Build a combined set of all skills to search for
    all_skills_to_check = all_required | ats_keywords

    found_skills = set()
    keyword_counts = Counter()

    for skill in all_skills_to_check:
        skill_lower = skill.lower()
        # Create search patterns
        raw_patterns = [skill_lower]

        # Add alias patterns
        for alias, canonical in SKILL_ALIASES.items():
            if canonical == skill:
                raw_patterns.append(alias)

        for raw in raw_patterns:
            escaped = re.escape(raw)
            # Use lookaround boundaries that work with special chars
            # (?<!\w) = not preceded by a word char, (?!\w) = not followed by a word char
            # For patterns starting/ending with non-word chars, use (?<!\S) / (?!\S) as fallback
            first_char = raw[0] if raw else ''
            last_char = raw[-1] if raw else ''

            # Choose left boundary
            if first_char.isalnum() or first_char == '_':
                left = r'(?<!\w)'
            else:
                left = r'(?:(?<=\s)|(?<=^)|(?<=\n))'

            # Choose right boundary
            if last_char.isalnum() or last_char == '_':
                right = r'(?!\w)'
            else:
                right = r'(?:(?=\s)|(?=$)|(?=\n)|(?=[,;.\)\]]))'

            try:
                regex = left + escaped + right
                matches = re.findall(regex, normalized)
                if matches:
                    found_skills.add(skill)
                    keyword_counts[skill] += len(matches)
            except re.error:
                # Fallback: simple substring search
                count = normalized.count(raw)
                if count > 0:
                    found_skills.add(skill)
                    keyword_counts[skill] += count

    missing_skills = all_skills_to_check - found_skills

    return found_skills, missing_skills, dict(keyword_counts)


def detect_sections(text):
    """
    Detect resume sections and return a dict of section_name -> content.
    """
    section_patterns = {
        "Skills": r'(?i)\b(skills|technical skills|core competencies|technologies|tech stack)\b',
        "Experience": r'(?i)\b(experience|work experience|employment|professional experience|work history)\b',
        "Projects": r'(?i)\b(projects|personal projects|academic projects|project experience)\b',
        "Education": r'(?i)\b(education|academic|qualification|degree|university|college)\b',
        "Certifications": r'(?i)\b(certifications?|certificates?|licensed?|accreditation)\b',
        "Summary": r'(?i)\b(summary|objective|about|profile|professional summary)\b',
    }

    sections_found = {}
    lines = text.split('\n')

    for section_name, pattern in section_patterns.items():
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                # Grab section content (next 20 lines max or until next section)
                content_lines = []
                for j in range(i + 1, min(i + 20, len(lines))):
                    # Stop if we hit another section header
                    is_next_section = False
                    for _, p in section_patterns.items():
                        if re.search(p, lines[j]) and j != i:
                            is_next_section = True
                            break
                    if is_next_section:
                        break
                    content_lines.append(lines[j])

                sections_found[section_name] = '\n'.join(content_lines).strip()
                break

    return sections_found


def detect_experience_level(text):
    """
    Detect experience level from the resume text.
    Returns: 'Fresher', 'Junior (1-2 years)', 'Mid (3-5 years)', or 'Senior (5+ years)'
    """
    normalized = text.lower()

    # Look for year patterns like "3+ years", "5 years of experience"
    year_patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
        r'(?:experience|exp)\s*(?:of)?\s*(\d+)\+?\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:in|of|working)',
    ]

    max_years = 0
    for pattern in year_patterns:
        matches = re.findall(pattern, normalized)
        for match in matches:
            try:
                years = int(match)
                max_years = max(max_years, years)
            except ValueError:
                pass

    # Check for fresher keywords
    fresher_keywords = ['fresher', 'fresh graduate', 'entry level', 'entry-level', 'intern', 'internship', 'recent graduate']
    is_fresher = any(kw in normalized for kw in fresher_keywords)

    if max_years == 0 and is_fresher:
        return "Fresher"
    elif max_years == 0:
        return "Fresher"
    elif max_years <= 2:
        return "Junior (1-2 years)"
    elif max_years <= 5:
        return "Mid (3-5 years)"
    else:
        return "Senior (5+ years)"


def parse_resume(file_path, job_role):
    """
    Full resume parsing pipeline.
    Returns a dict with all extracted information.
    """
    text = extract_text(file_path)
    found_skills, missing_skills, keyword_counts = detect_skills(text, job_role)
    sections = detect_sections(text)
    experience_level = detect_experience_level(text)

    # Separate technical and soft skills
    role_data = JOB_ROLES.get(job_role, {})
    tech_skills_set = set(role_data.get("technical_skills", []))
    soft_skills_set = set(role_data.get("soft_skills", []))

    found_technical = found_skills & tech_skills_set
    found_soft = found_skills & soft_skills_set
    missing_technical = tech_skills_set - found_skills
    missing_soft = soft_skills_set - found_skills

    return {
        "raw_text": text,
        "found_skills": sorted(list(found_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "found_technical": sorted(list(found_technical)),
        "found_soft": sorted(list(found_soft)),
        "missing_technical": sorted(list(missing_technical)),
        "missing_soft": sorted(list(missing_soft)),
        "keyword_counts": keyword_counts,
        "sections": sections,
        "experience_level": experience_level,
        "job_role": job_role,
    }
