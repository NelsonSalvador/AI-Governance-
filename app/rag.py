from dataclasses import dataclass


@dataclass
class Doc:
    id: str
    text: str
    classification: str = "internal"


# In-memory starter store. Swap for a real vector DB (pgvector, Qdrant, ...)
# running inside your sovereign environment.
_DOCS: list[Doc] = []


def add_document(doc: Doc) -> None:
    _DOCS.append(doc)


def retrieve(query: str, clearance: set[str], k: int = 3) -> list[Doc]:
    """Naive keyword-overlap retrieval, filtered by what the caller may see.
    Replace the scoring with embeddings later; keep the clearance filter."""
    terms = {t.lower() for t in query.split()}
    scored: list[tuple[int, Doc]] = []
    for d in _DOCS:
        if d.classification not in clearance:
            continue
        overlap = len(terms & {t.lower() for t in d.text.split()})
        if overlap:
            scored.append((overlap, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:k]]
