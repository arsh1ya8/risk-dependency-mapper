from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import call_groq_safe
import os

describe_bp = Blueprint("describe", __name__)


def load_prompt(user_input):
    with open("prompts/describe_prompt.txt", "r") as f:
        template = f.read()
    return template.replace("{input}", user_input)


@describe_bp.route("/describe", methods=["POST"])
def describe():

    data = request.get_json()

    # Input validation
    if not data or "input" not in data:
        return jsonify({"error": "Input is required"}), 400

    user_input = data["input"].strip()

    if not user_input:
        return jsonify({"error": "Input cannot be empty"}), 400

    # 🔐 Check API key FIRST (IMPORTANT FIX)
    if not os.getenv("GROQ_API_KEY"):
        return jsonify({
            "error": "Service temporarily unavailable"
        }), 503

    # Load prompt
    prompt = load_prompt(user_input)

    # Safe AI call
    result = call_groq_safe(prompt)

    # Handle failure safely (no debug info exposed)
    if not result:
        return jsonify({
            "description": "AI service unavailable",
            "generated_at": datetime.utcnow().isoformat()
        }), 503

    return jsonify({
        "description": result.strip(),
        "generated_at": datetime.utcnow().isoformat()
    })