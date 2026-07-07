import json
import urllib.request

from .config import settings


def generate(prompt: str) -> str:
    """Call the configured sovereign model endpoint (OpenAI-compatible
    /chat/completions assumed). Falls back to a mock so the pipeline runs with
    no endpoint set."""
    if not settings.MODEL_ENDPOINT:
        return f"[mock:{settings.MODEL_NAME}] answering: " + prompt[:300]

    body = json.dumps(
        {
            "model": settings.MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode()
    req = urllib.request.Request(
        settings.MODEL_ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.MODEL_API_KEY}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    return data["choices"][0]["message"]["content"]
