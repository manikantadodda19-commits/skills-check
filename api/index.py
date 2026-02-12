"""
Vercel Serverless Function Entry Point
Wraps the Flask app for Vercel's Python runtime.
"""

import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend")
sys.path.insert(0, backend_dir)

from app import app

# Vercel expects the handler to be named 'app' or 'handler'
# Flask app is already named 'app', so it's auto-detected
