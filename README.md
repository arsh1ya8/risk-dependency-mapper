# AI Service — Risk Dependency Mapper

The AI microservice for the Risk Dependency Mapper project. Built with Python and Flask, powered by Groq LLaMA model.

---

## Prerequisites

- Python 3.11+
- pip
- Groq API key (free at console.groq.com)

---

## Setup Steps

1. Clone the repository and navigate to the ai-service folder:
cd ai-service

2. Create a virtual environment:
python -m venv venv

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
pip install -r requirements.txt

5. Create a `.env` file in the ai-service folder:
GROQ_API_KEY=your_groq_api_key_here

6. Run the service:
python app.py
Service runs on: `http://localhost:5000`

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| GROQ_API_KEY | Your Groq API key from console.groq.com | Yes |

---

## Run Instructions

Start the service:
python app.py

Run tests:
pytest test_endpoints.py -v

Health check:
GET http://localhost:5000/health

---

## API Reference

### GET /health
Check if the service is running.

**Response:**
```json
{"status": "ok"}
```

---

### POST /describe
Generate a professional description of a risk.

**Request:**
```json
{"input": "server crash during peak hours"}
```

**Response:**
```json
{
  "description": "AI generated risk description...",
  "generated_at": "2026-04-17T10:00:00"
}
```

**Errors:**
- `400` — input is missing or empty
- `503` — AI service unavailable

---

### POST /recommend
Get 3 actionable recommendations for a risk.

**Request:**
```json
{"input": "server crash during peak hours"}
```

**Response:**
```json
[
  {
    "action_type": "Preventive",
    "description": "recommendation here",
    "priority": "High"
  }
]
```

**Errors:**
- `400` — input is missing or empty

---

### POST /generate-report
Stream a full risk report using SSE (Server-Sent Events).

**Request:**
```json
{"input": "server crash during peak hours"}
```

**Response:** Streamed text/event-stream tokens

---

### POST /analyse-document
Analyse a document and return key insights and risks.

**Request:**
```json
{"input": "document text here"}
```

**Response:**
```json
{
  "findings": [
    {
      "type": "risk",
      "finding": "finding description",
      "severity": "High"
    }
  ],
  "generated_at": "2026-04-17T10:00:00"
}
```

**Errors:**
- `400` — input is missing or empty
- `503` — AI service unavailable

---

### POST /batch-process
Process up to 20 risk items in one request.

**Request:**
```json
{"items": ["server crash", "data breach", "employee resignation"]}
```

**Response:**
```json
{
  "results": [
    {
      "input": "server crash",
      "description": "AI generated description...",
      "error": null,
      "processed_at": "2026-04-17T10:00:00"
    }
  ],
  "total": 3,
  "generated_at": "2026-04-17T10:00:00"
}
```

**Errors:**
- `400` — items missing, not a list, empty, or exceeds 20 items