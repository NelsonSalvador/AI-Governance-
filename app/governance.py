import re

# --- Access control --------------------------------------------------------
# Minimal role -> allowed data classifications map. Replace with your IdP / RBAC.
ROLE_CLEARANCE = {
    "analyst": {"public", "internal"},
    "advisor": {"public", "internal", "client"},
    "admin": {"public", "internal", "client", "restricted"},
}


def can_access(role: str, classification: str) -> bool:
    return classification in ROLE_CLEARANCE.get(role, {"public"})


# --- PII / client-data redaction ------------------------------------------
# Starter patterns only. For production, use a proper PII/NER model and your
# own client-identifier formats.
_PATTERNS = {
    "EMAIL": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "IBAN": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"),
    "PHONE": re.compile(r"\b(?:\+41|0)\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}\b"),
}


def redact(text: str) -> tuple[str, list[str]]:
    found: list[str] = []
    for label, pat in _PATTERNS.items():
        if pat.search(text):
            found.append(label)
            text = pat.sub(f"[{label}]", text)
    return text, found


# --- Model routing by sensitivity -----------------------------------------
def route(classification: str) -> str:
    """Decide which model tier handles a request. Sensitive data must stay on
    the sovereign / on-prem model and never leave the tenant."""
    if classification in {"client", "restricted"}:
        return "sovereign"
    # Default everything to sovereign for now. Once you add a redacting proxy,
    # you can route low-sensitivity traffic to "external" for a stronger model.
    return "sovereign"
