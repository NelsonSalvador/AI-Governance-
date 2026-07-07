import hashlib
import json
import time

from .config import settings


def record(event: dict) -> None:
    """Append-only audit trail. Every request/response is logged with a SHA-256
    over its contents so tampering is detectable. This is the compliance-
    evidence layer an auditor or regulator (DORA / AI Act / FADP) will ask for."""
    event = {"ts": time.time(), **event}
    digest = hashlib.sha256(
        json.dumps(event, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()
    event["hash"] = digest
    with open(settings.AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
