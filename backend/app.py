"""
Resume Skill Gap Analyzer — Flask Backend
Serves the frontend and provides API endpoints for resume analysis.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import uuid

# Ensure backend modules are importable regardless of working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from resume_parser import parse_resume
from analyzer import run_full_analysis
from courses import get_recommended_courses

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join("/tmp", "uploads") if os.environ.get("VERCEL") else os.path.join(BASE_DIR, "uploads")
FRONTEND_FOLDER = os.path.join(BASE_DIR, "..", "frontend")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory session store: session_id -> analysis results
sessions = {}


# ============================================================
#  Static File Serving
# ============================================================

@app.route("/")
def home():
    return send_from_directory(FRONTEND_FOLDER, "page.html")


@app.route("/<path:filename>")
def serve_file(filename):
    """Serve HTML, CSS, JS, and image files from the frontend folder."""
    allowed_extensions = (".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".gif", ".webp")
    if filename.endswith(allowed_extensions):
        return send_from_directory(FRONTEND_FOLDER, filename)
    return "File not found", 404


# ============================================================
#  Resume Upload API
# ============================================================

@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    """
    Upload a resume file and job role.
    Parses the resume, runs full analysis, stores results in session.
    Returns a session_id for subsequent API calls.
    """
    if "resume" not in request.files:
        return jsonify({"error": "Resume file is required"}), 400

    job_role = request.form.get("jobRole", "")
    if not job_role:
        return jsonify({"error": "Job role is required"}), 400

    file = request.files["resume"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file
    safe_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, safe_name)
    file.save(file_path)

    try:
        # Parse the resume
        parsed_data = parse_resume(file_path, job_role)

        # ── Validate: does this look like a resume? ──
        resume_indicators = [
            "education", "experience", "skills", "projects", "work",
            "university", "college", "degree", "certifications",
            "summary", "objective", "qualification", "employment",
            "intern", "professional", "achievements", "responsibilities",
            "bachelor", "master", "gpa", "resume", "curriculum vitae"
        ]
        text_lower = parsed_data.get("raw_text", "").lower()
        matches = sum(1 for kw in resume_indicators if kw in text_lower)

        if matches < 2:
            return jsonify({
                "error": "This file does not appear to be a resume. Please upload a valid resume (PDF or DOCX) containing sections like Education, Experience, Skills, etc."
            }), 400

        # Run full analysis
        analysis = run_full_analysis(parsed_data)

        # Get course recommendations
        courses = get_recommended_courses(parsed_data)
        analysis["courses"] = courses

        # Store in session
        session_id = uuid.uuid4().hex
        sessions[session_id] = analysis

        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Resume analyzed successfully"
        })

    except Exception as e:
        return jsonify({"error": f"Failed to analyze resume: {str(e)}"}), 500

    finally:
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except OSError:
            pass


# ============================================================
#  Analysis API Endpoints
# ============================================================

def get_session(session_id):
    """Helper to retrieve session data."""
    if not session_id or session_id not in sessions:
        return None
    return sessions[session_id]


@app.route("/api/resume-summary")
def api_resume_summary():
    """Return resume summary and skill comparison data."""
    session = get_session(request.args.get("session_id"))
    if not session:
        return jsonify({"error": "Session not found. Please upload a resume first."}), 404

    comparison = session["skill_comparison"]
    parsed = session["parsed_data"]

    return jsonify({
        "profile": comparison["profile"],
        "experience_level": comparison["experience_level"],
        "strengths": comparison["strengths"],
        "weaknesses": comparison["weaknesses"],
        "technical": comparison["technical"],
        "soft": comparison["soft"],
        "projects": comparison["projects"],
        "found_technical": parsed["found_technical"],
        "found_soft": parsed["found_soft"],
        "missing_technical": parsed["missing_technical"],
        "missing_soft": parsed["missing_soft"],
    })


@app.route("/api/ats-analysis")
def api_ats_analysis():
    """Return ATS analysis data."""
    session = get_session(request.args.get("session_id"))
    if not session:
        return jsonify({"error": "Session not found. Please upload a resume first."}), 404

    ats_score = session["ats_score"]
    if ats_score >= 80:
        match_label = "Strong Match"
    elif ats_score >= 60:
        match_label = "Moderate Match"
    else:
        match_label = "Weak Match"

    return jsonify({
        "ats_score": ats_score,
        "match_label": match_label,
        "risk_assessment": session["risk_assessment"],
        "section_scores": session["section_scores"],
        "keyword_density": session["keyword_density"],
        "missing_keywords": session["missing_keywords"],
        "role_matches": session["role_matches"],
        "simulator": session["simulator"],
        "ai_insight": session["ai_insight"],
    })


@app.route("/api/recommended-roles")
def api_recommended_roles():
    """Return recommended job roles."""
    session = get_session(request.args.get("session_id"))
    if not session:
        return jsonify({"error": "Session not found. Please upload a resume first."}), 404

    return jsonify(session["recommended_role"])


@app.route("/api/suggested-courses")
def api_suggested_courses():
    """Return suggested courses based on skill gaps."""
    session = get_session(request.args.get("session_id"))
    if not session:
        return jsonify({"error": "Session not found. Please upload a resume first."}), 404

    return jsonify({"courses": session["courses"]})


@app.route("/api/learning-roadmap")
def api_learning_roadmap():
    """Return the 90-day learning roadmap."""
    session = get_session(request.args.get("session_id"))
    if not session:
        return jsonify({"error": "Session not found. Please upload a resume first."}), 404

    return jsonify(session["learning_roadmap"])


# ============================================================
#  Run Server
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(debug=debug, host="0.0.0.0", port=port)
