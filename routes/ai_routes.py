from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from datetime import datetime, timezone
import os

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/describe", methods=["POST"])
def describe():
    data = request.get_json()

    title = data.get("title", "").strip()
    details = data.get("details", "").strip()

    if not title or not details:
        return jsonify({"error": "title and details are required"}), 400

    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/describe_prompt.txt")
    with open(prompt_path, "r") as f:
        template = f.read()

    prompt = template.replace("{title}", title).replace("{details}", details)

    result = call_groq(prompt)

    return jsonify({
        "description": result,
        "generated_at": datetime.now(timezone.utc).isoformat()
    })