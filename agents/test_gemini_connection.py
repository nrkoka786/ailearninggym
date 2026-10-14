#!/usr/bin/env python3
"""Minimal authenticated Gemini generateContent connectivity test (no publishing)."""
import json
import os
import sys
import urllib.error
import urllib.request

ALLOWED = {"gemini-3.1-flash-lite", "gemini-3.5-flash-lite"}
model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
if model not in ALLOWED:
    sys.exit("Unsupported test model")
key = os.getenv("GEMINI_API_KEY")
if not key:
    sys.exit("GEMINI_API_KEY secret missing")
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
payload = {"contents": [{"parts": [{"text": "Reply with exactly the word READY."}]}],
           "generationConfig": {"maxOutputTokens": 80}}
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                             headers={"Content-Type": "application/json",
                                      "x-goog-api-key": key}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=35) as response:
        data = json.load(response)
except urllib.error.HTTPError as exc:
    try:
        detail = json.loads(exc.read(4096).decode("utf-8")).get("error", {})
        message = str(detail.get("message", "No details"))[:500]
    except (ValueError, UnicodeDecodeError):
        message = "No structured error details"
    sys.exit(f"Gemini test failed: HTTP {exc.code}: {message}")
except urllib.error.URLError as exc:
    sys.exit(f"Gemini network error: {type(exc.reason).__name__}")
text = "".join(part.get("text", "") for candidate in data.get("candidates", [])
               for part in candidate.get("content", {}).get("parts", []))
if not text.strip():
    sys.exit("Gemini returned no text")
usage = data.get("usageMetadata", {})
print("Gemini connectivity SUCCESS")
print("Model:", model)
print("Response:", text.strip()[:120])
print("Token usage:", json.dumps({k: usage.get(k) for k in
      ("promptTokenCount", "candidatesTokenCount", "totalTokenCount")}))
