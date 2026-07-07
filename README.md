# Compliant AI — last-mile MVP

A minimal, runnable skeleton of the "last-mile" layer: a governed AI assistant
that sits on top of sovereign infrastructure. It runs out of the box with a mock
model so you can build the pipeline before wiring up a real endpoint.

> 📓 **Doing customer discovery / expert interviews for this project?** See [`RESEARCH.md`](RESEARCH.md)
> — paste a meeting note or describe a call to Claude Code and it files everything into our Notion
> research CRM (People, Organizations, Meetings, Insights, Tasks), all linked. No manual Notion work.

## The idea

You don't build models or infrastructure — you build the governed layer between
a regulated organisation's users and a sovereign model. Each module below maps to
one part of that layer:

| Module | Layer | What it does |
| --- | --- | --- |
| `app/rag.py` | RAG | Retrieval over the org's own documents, filtered by clearance |
| `app/governance.py` | Governance | Access control, PII/client-data redaction, model routing by sensitivity |
| `app/audit.py` | Audit & evidence | Append-only, hash-chained log — the compliance evidence (DORA / AI Act / FADP) |
| `app/model_client.py` | Infra | Calls a sovereign model endpoint (Apertus, Mistral on-prem, Ollama...) |
| `app/pipeline.py` | Orchestration | access → retrieve → route → redact → generate → audit |

## Run it

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then:

```bash
curl -X POST localhost:8000/chat -H "Content-Type: application/json" \
  -d '{"query": "what is the remote work policy?", "role": "advisor", "classification": "internal"}'
```

Run the tests with `pytest`. Each request appends a line to `audit.jsonl`.

## Wire up a real model

Copy `.env.example` to `.env` and set `MODEL_ENDPOINT` to any OpenAI-compatible
`/chat/completions` URL (e.g. a local Ollama, or a sovereign-hosted Apertus/Mistral).
Leave it blank to keep using the mock.

## Build plan (good tasks to hand to Claude Code)

1. **Real retrieval** — replace keyword overlap in `rag.py` with embeddings + a
   vector DB (pgvector or Qdrant) running in your own environment. Keep the
   clearance filter.
2. **Real redaction** — swap the regexes in `governance.py` for a PII/NER model
   and add your client-identifier formats.
3. **A redacting external tier** — implement the `"external"` branch in `route()`
   so low-sensitivity traffic can use a stronger model behind redaction.
4. **Auth** — put real SSO / RBAC in front of `/chat` and derive `role` from the
   token instead of trusting the request body.
5. **A compliance-pack export** — turn `audit.jsonl` into the report format an
   auditor actually wants (per-user activity, retention, model tiers used).
6. **A minimal chat UI** — the assistant surface your users actually see.

## Where this specialises per segment

The core is segment-agnostic; the emphasis shifts with your wedge:
- **Small / mid banks** → the audit layer and banking-secrecy-grade routing.
- **Universities** → cheap turnkey deployment and unpublished-research protection.
- **Software houses** → expose this as a clean embeddable SDK, not an app.
