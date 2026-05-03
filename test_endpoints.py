import pytest
import json
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ✅ TEST 1: Health check works
def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200


# ✅ TEST 2: /describe returns description
def test_describe_success(client):
    with patch("services.groq_client.call_groq_safe", return_value="This is a test description."):
        res = client.post("/describe",
            json={"input": "server crash"},
            content_type="application/json")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert "description" in data
        assert "generated_at" in data


# ✅ TEST 3: /describe with empty input returns 400
def test_describe_empty_input(client):
    res = client.post("/describe",
        json={"input": ""},
        content_type="application/json")
    assert res.status_code == 400


# ✅ TEST 4: /describe with missing input returns 400
def test_describe_missing_input(client):
    res = client.post("/describe",
        json={},
        content_type="application/json")
    assert res.status_code == 400


# ✅ TEST 5: /describe when AI fails returns 503
def test_describe_ai_failure(client):
    with patch("routes.describe.call_groq_safe", return_value=None):
        res = client.post("/describe",
            json={"input": "server crash"},
            content_type="application/json")
        assert res.status_code == 503


# ✅ TEST 6: /recommend returns list
def test_recommend_success(client):
    mock_response = '[{"action_type": "Preventive", "description": "Test", "priority": "High"}]'
    with patch("services.groq_client.call_groq_safe", return_value=mock_response):
        res = client.post("/recommend",
            json={"input": "server crash"},
            content_type="application/json")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert isinstance(data, list)


# ✅ TEST 7: /recommend with empty input returns 400
def test_recommend_empty_input(client):
    res = client.post("/recommend",
        json={"input": ""},
        content_type="application/json")
    assert res.status_code == 400


# ✅ TEST 8: /analyse-document returns findings
def test_analyse_success(client):
    mock_response = '[{"type": "risk", "finding": "Test finding", "severity": "High"}]'
    with patch("services.groq_client.call_groq_safe", return_value=mock_response):
        res = client.post("/analyse-document",
            json={"input": "company data was breached"},
            content_type="application/json")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert "findings" in data


# ✅ TEST 9: /analyse-document with empty input returns 400
def test_analyse_empty_input(client):
    res = client.post("/analyse-document",
        json={"input": ""},
        content_type="application/json")
    assert res.status_code == 400


# ✅ TEST 10: /analyse-document with missing input returns 400
def test_analyse_missing_input(client):
    res = client.post("/analyse-document",
        json={},
        content_type="application/json")
    assert res.status_code == 400