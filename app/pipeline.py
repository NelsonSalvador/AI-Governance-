from . import audit, model_client, rag
from .governance import ROLE_CLEARANCE, can_access, redact, route


def handle(query: str, role: str = "advisor", classification: str = "internal") -> dict:
    """The last-mile pipeline:
    access check -> retrieve -> route -> redact -> generate -> audit."""
    if not can_access(role, classification):
        audit.record({"event": "denied", "role": role, "classification": classification})
        return {"error": "access denied for this data classification"}

    clearance = ROLE_CLEARANCE.get(role, {"public"})
    docs = rag.retrieve(query, clearance)
    context = "\n\n".join(d.text for d in docs)

    tier = route(classification)
    # Only redact when sending to an external model tier.
    prompt_query, pii = redact(query) if tier == "external" else (query, [])
    prompt = f"Context:\n{context}\n\nQuestion: {prompt_query}"

    answer = model_client.generate(prompt)

    audit.record(
        {
            "event": "answer",
            "role": role,
            "classification": classification,
            "model_tier": tier,
            "retrieved": [d.id for d in docs],
            "pii_redacted": pii,
        }
    )
    return {"answer": answer, "sources": [d.id for d in docs], "model_tier": tier}
