from fastapi import FastAPI
from pydantic import BaseModel

from . import rag
from .pipeline import handle

app = FastAPI(title="Compliant AI - last-mile MVP")

# Seed a couple of documents so /chat returns something on first run.
rag.add_document(
    rag.Doc(id="policy-01", text="Remote work is allowed up to three days per week.", classification="internal")
)
rag.add_document(
    rag.Doc(id="client-42", text="Client Meyer prefers quarterly portfolio reviews.", classification="client")
)


class ChatRequest(BaseModel):
    query: str
    role: str = "advisor"
    classification: str = "internal"


@app.post("/chat")
def chat(req: ChatRequest):
    return handle(req.query, req.role, req.classification)


@app.get("/health")
def health():
    return {"status": "ok"}
