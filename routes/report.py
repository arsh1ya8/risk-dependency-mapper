from flask import Blueprint, request, Response
from services.groq_client import stream_groq

report_bp = Blueprint("report", __name__)


def load_prompt(user_input):
    with open("prompts/report_prompt.txt", "r") as f:
        template = f.read()
    return template.replace("{input}", user_input)


@report_bp.route("/generate-report", methods=["POST"])
def generate_report():

    data = request.get_json()
    user_input = data.get("input", "").strip()

    if not user_input:
        return Response("data: Input required\n\n", mimetype="text/event-stream")

    prompt = load_prompt(user_input)

    def event_stream():
        for chunk in stream_groq(prompt):
            yield f"data: {chunk}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")