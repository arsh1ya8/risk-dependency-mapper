from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import call_groq_safe
import time

batch_bp = Blueprint("batch", __name__)

def load_prompt(user_input):
    with open("prompts/describe_prompt.txt", "r") as f:
        template = f.read()
    return template.replace("{input}", user_input)

@batch_bp.route("/batch-process", methods=["POST"])
def batch_process():
    data = request.get_json()

    if not data or "items" not in data:
        return jsonify({"error": "items array is required"}), 400

    items = data["items"]

    if not isinstance(items, list):
        return jsonify({"error": "items must be a list"}), 400

    if len(items) == 0:
        return jsonify({"error": "items cannot be empty"}), 400

    if len(items) > 20:
        return jsonify({"error": "maximum 20 items allowed"}), 400

    results = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            results.append({
                "input": item,
                "description": None,
                "error": "Invalid input",
                "processed_at": datetime.utcnow().isoformat()
            })
            time.sleep(0.1)
            continue

        prompt = load_prompt(item.strip())
        result = call_groq_safe(prompt)

        results.append({
            "input": item,
            "description": result if result else "AI service unavailable",
            "error": None if result else "AI service unavailable",
            "processed_at": datetime.utcnow().isoformat()
        })

        time.sleep(0.1)

    return jsonify({
        "results": results,
        "total": len(results),
        "generated_at": datetime.utcnow().isoformat()
    })