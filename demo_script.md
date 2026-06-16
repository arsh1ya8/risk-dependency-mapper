# AI Demo Script — Risk Dependency Mapper
**Duration:** 8 minutes  
**Role:** AI Developer 1  
**Base URL:** http://localhost:5000

---

## 1. Health Check (30 sec)
**What to say:** "Let's start by confirming the AI service is live."

**Request:**
GET /health

**Expected Output:**
```json
{ "status": "ok" }
```

---

## 2. /describe (1.5 min)
**What to say:** "We pass a risk scenario and the AI returns a plain-English description of it."

**Input:**
```json
{ "input": "Payment gateway dependency failure during peak checkout hours" }
```

**Expected Output:**
```json
{
  "description": "A critical dependency failure in the payment gateway...",
  "generated_at": "2026-05-05T10:00:00"
}
```

---

## 3. /recommend (1.5 min)
**What to say:** "Now the AI recommends mitigation strategies for that risk."

**Input:**
```json
{ "input": "Payment gateway dependency failure during peak checkout hours" }
```

**Expected Output:**
```json
[
  { "recommendation": "Implement fallback payment provider", "priority": "High" },
  { "recommendation": "Add circuit breaker pattern", "priority": "High" }
]
```

---

## 4. /analyse-document (1.5 min)
**What to say:** "Here we analyse a full risk document and get structured findings back."

**Input:**
```json
{ "input": "Our system depends on 3 external APIs: Stripe, SendGrid, and AWS S3. Any outage causes full service disruption." }
```

**Expected Output:**
```json
{
  "findings": [
    { "risk": "Stripe outage", "severity": "Critical", "impact": "Payments fail" },
    { "risk": "SendGrid outage", "severity": "High", "impact": "No email notifications" }
  ],
  "generated_at": "2026-05-05T10:00:00"
}
```

---

## 5. /generate-report (1.5 min)
**What to say:** "This endpoint streams a full risk report in real time using SSE."

**Input:**
```json
{ "input": "Analyse risks for an e-commerce platform dependent on Stripe, AWS, and SendGrid" }
```

**Expected Output:**  
Streaming text chunks arriving live — a full markdown risk report.

---

## 6. /batch-process (1 min)
**What to say:** "Finally, batch mode — we send multiple risks at once and get descriptions for all of them."

**Input:**
```json
{
  "items": [
    "Database connection pool exhaustion",
    "Third-party auth provider downtime",
    "CDN failure causing static asset loss"
  ]
}
```

**Expected Output:**
```json
{
  "results": [
    { "input": "Database connection pool exhaustion", "description": "...", "error": null },
    { "input": "Third-party auth provider downtime", "description": "...", "error": null },
    { "input": "CDN failure causing static asset loss", "description": "...", "error": null }
  ],
  "total": 3,
  "generated_at": "2026-05-05T10:00:00"
}
```

---

## Closing (30 sec)
**What to say:** "All 6 endpoints are live, tested, and handling real AI responses with proper error handling and security in place."