from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import call_groq_safe
import json
import re

analyse_bp = Blueprint("analyse", __name__)

def load_prompt(user_input):
    with open("prompts/analyse_prompt.txt", "r") as f:
        template = f.read()
    return template.replace("{input}", user_input)

def extract_json(text):
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        return match.group(0)
    return None

@analyse_bp.route("/analyse-document", methods=["POST"])
def analyse_document():
    data = request.get_json()

    if not data or "input" not in data:
        return jsonify({"error": "Input is required"}), 400

    user_input = data["input"].strip()

    if not user_input:
        return jsonify({"error": "Input cannot be empty"}), 400

    prompt = load_prompt(user_input)
    result = call_groq_safe(prompt)

    if not result:
        return jsonify({"error": "AI service unavailable"}), 503

    json_part = extract_json(result)

    if not json_part:
        return jsonify({"error": "Could not parse AI response"}), 500

    try:
        findings = json.loads(json_part)
    except:
        return jsonify({"error": "Invalid AI response format"}), 500

    return jsonify({
        "findings": findings,
        "generated_at": datetime.utcnow().isoformat()
    })