import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"), override=True)

# Pre-load client at startup
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            _client = Groq(api_key=api_key)
    return _client

# Simple in-memory cache
_cache = {}

def call_groq_safe(prompt):
    # Check cache first
    if prompt in _cache:
        return _cache[prompt]

    client = get_client()

    if not client:
        return None

    retries = 3

    for _ in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=300
            )
            result = response.choices[0].message.content
            # Save to cache
            _cache[prompt] = result
            return result

        except Exception:
            time.sleep(2)

    return None


def stream_groq(prompt):
    client = get_client()

    if not client:
        yield "Service unavailable"
        return

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300,
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception:
        yield "Service unavailable"