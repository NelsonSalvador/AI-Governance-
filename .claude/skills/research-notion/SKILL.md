---
name: research-notion
description: File research conversations into the Compliant AI Notion CRM. Use whenever the user pastes a meeting note (Granola or otherwise), describes a call/conversation with a client, prospect, industry expert, advisor or investor, or shares a research finding to capture. Creates and links People, Organizations, Meetings, Insights, and Tasks in Notion, avoiding duplicates.
---

# Research → Notion CRM

Turn an unstructured meeting note, call recap, or spoken description of a conversation into
clean, linked records in the **Compliant AI Adoption** research workspace in Notion. This is the
shared customer-discovery / expert-interview brain for the project — keep it tidy and de-duplicated.

## When to use this

Trigger on things like:
- "Here are my Granola notes from the call with …" (a pasted block of notes)
- "I just spoke with a CISO at a cantonal bank, she said …"
- "Add this expert to the network: …"
- "Log a follow-up to send the deck to …"
- "We learned that universities won't pay per-seat" (a standalone insight)

If the user is only *asking a question* about the research (not adding to it), don't write — just answer.

## Prerequisites

1. **Notion connector must be enabled** in this Claude Code session. The tools are exposed via MCP.
   Load them on demand with ToolSearch — the tool names are prefixed with a per-connection id, so
   search by keyword rather than guessing the exact name:
   - `ToolSearch` query: `notion search fetch create-pages update-page query-data-sources` — grab
     the search, fetch, create-pages, update-page, and query-data-sources tools.
2. **Access to the workspace.** These records live in *Nelson Salvador's Space*, under the
   **Compliant AI Adoption** page. If you're a teammate, Nelson must share that page (or the whole
   space) with your Notion account, and you must connect that same Notion account in Claude Code.
   If a write returns a permission/not-found error, that sharing step is the likely cause.

## The databases

All five live under the **Compliant AI Adoption** page. IDs are in [`notion_ids.json`](notion_ids.json)
next to this file — read it if you need to confirm an ID. Use the **`data_source_id`** as the parent
when creating pages, and as the table name (`collection://<id>`) when querying.

| Database | data_source_id | Holds |
| --- | --- | --- |
| People | `de9f2065-cf16-455b-81bf-fc1499f67fab` | Individuals in the network |
| Organizations | `16143f80-412f-439c-bfe1-797b082733b2` | Companies & institutions |
| Meetings & Notes | `3a1802a7-9bbe-4af5-88e9-f4fdcb70436a` | Calls, interviews, brainstorms |
| Insights | `0c4ac2ef-37e8-41ad-84cd-d224387d4921` | Distilled learnings |
| Tasks & Follow-ups | `e896632a-631b-4c07-95f5-a9dff285c1ae` | Action items |

There's also a **Regulations** reference database (`da55888a-60c5-472d-aeb9-9a2b4b053db4`) — a read-only
knowledge base on DORA, FADP, EU AI Act, GDPR, NIS2 and Swiss banking secrecy (requirements + sales
hooks). Don't file meeting data into it; read it when you need to ground a regulatory point.

## Property schemas (use these EXACT names and option values)

Select/multi-select values must match exactly or the write is rejected. When something doesn't fit an
existing option, pick the closest and note it to the user — do **not** invent new option values.

**People** — `Name` (title), `Role/Title` (text), `Persona` (select: `Buyer/Decision-maker`,
`Champion`, `End user`, `Industry expert`, `Advisor`, `Investor`, `Partner`, `Other`), `Segment`
(select — see segment list below), `Email` (email), `LinkedIn` (url), `Location` (text), `Status`
(select: `To contact`, `Contacted`, `In conversation`, `Warm`, `Advocate`, `Dormant`), `Notes`
(text), `Organization` (relation → Organizations).

**Organizations** — `Name` (title), `Segment` (select), `Type` (select: `Prospect`, `Customer`,
`Partner`, `Competitor`, `Institution`), `Country` (select: `Switzerland`, `Germany`, `France`,
`EU-other`, `Other`), `Size` (select: `Micro`, `Small`, `Mid`, `Large`), `Reg exposure` (multi-select:
`DORA`, `EU AI Act`, `GDPR`, `FADP`, `Banking secrecy`, `NIS2`), `Status` (select: `Target`,
`Contacted`, `Discovery`, `Piloting`, `Customer`, `Passed`), `Website` (url), `Notes` (text).

**Meetings & Notes** — `Name` (title, e.g. "Discovery call: Cantonal Bank AG"), `Date` (date —
set via `date:Date:start`), `Type` (select: `Discovery call`, `Expert interview`, `Demo`,
`Brainstorm`, `Internal`, `Follow-up`), `Source` (select: `Granola`, `Manual note`, `Call`, `Email`,
`Other`), `Owner` (person — the teammate who ran it; usually leave empty unless known), `Summary`
(text — a 1–3 sentence recap), `Sentiment` (select: `Positive`, `Neutral`, `Negative`, `Mixed`),
`Attendees` (relation → People), `Organization` (relation → Organizations). **Put the full raw note
in the page body**, not in a property.

**Insights** — `Name` (title — the learning stated as one crisp sentence), `Category` (select: `Pain`,
`Objection`, `Feature request`, `Willingness to pay`, `Buying process`, `Regulatory`, `Competitor`,
`Market`, `Positioning`), `Segment` (select, or `Cross-segment`), `Confidence` (select: `Hypothesis`,
`Emerging`, `Validated`, `Strong`), `Impact` (select: `High`, `Medium`, `Low`), `Status` (select:
`Open`, `Exploring`, `Confirmed`, `Invalidated`), `Source meetings` (relation → Meetings), `People`
(relation → People).

**Tasks & Follow-ups** — `Name` (title, action phrased as a verb), `Status` (select: `To do`,
`In progress`, `Blocked`, `Done`), `Priority` (select: `High`, `Medium`, `Low`), `Due` (date — set
via `date:Due:start`), `Assignee` (person), `Meeting` (relation → Meetings), `Organization`
(relation → Organizations).

**Segment** (shared across People / Organizations / Insights): `Small/Mid Bank`, `Cantonal Bank`,
`Wealth/Asset Manager`, `Insurer`, `University/Research`, `Municipal/Gov`, `Software House`,
`Regulator`, `Other` (Insights also allow `Cross-segment`).

## Workflow

Do this in order. Prefer batching independent reads/writes in a single step.

1. **Parse** the input into: the organization(s), the person/people, the meeting itself, any
   insights (learnings), and any follow-up tasks. If the note is a transcript, read the whole thing
   before deciding — insights are often buried mid-conversation.

2. **De-duplicate before creating.** For each Organization and Person, first search Notion to see if
   they already exist:
   - Query the data source, e.g. `SELECT url, "Name" FROM "collection://<data_source_id>" WHERE
     "Name" LIKE ?` with `%name%`, or use notion search scoped to the database.
   - If a match exists, **reuse its page URL** (and update it if you have new info). Only create a new
     record when there's no reasonable match. Never create a second "Cantonal Bank AG".

3. **Create/reuse the Organization**, then the **Person(s)**, setting `Organization` on each person to
   the org's page URL.

4. **Create the Meeting.** Set the properties; put the raw/verbatim note in the page `content`
   (a "## Raw notes" section, plus "## Key takeaways" and "## Follow-ups" if useful). Link
   `Attendees` (people) and `Organization`. If no date was given, use today's date.

5. **Create Insights** — one row per atomic learning (don't cram three learnings into one). Link each
   to the meeting via `Source meetings` and to the relevant `People`. Set `Confidence` honestly:
   a single anecdote is `Emerging` at best, not `Validated`. Before creating, glance at existing
   Insights for the same segment — if this restates one that exists, strengthen that one's
   `Confidence`/`Status` instead of adding a duplicate.

6. **Create Tasks** for any follow-ups, linked to the `Meeting` and `Organization`.

7. **Update statuses** when the conversation implies movement (e.g. a first call → set the Person to
   `In conversation` and the Org to `Discovery`).

8. **Report back** concisely: list what you created vs. reused, with clickable Notion URLs, and the
   insights extracted. Flag anything you guessed (segment, persona, confidence) and ask the user to
   confirm or correct — one short question, not an interrogation.

## Setting relation properties

Relation values are a **JSON array of page URLs** passed as a string, e.g.:

```
"Attendees": "[\"https://app.notion.com/p/<person-page-id>\"]"
"Organization": "[\"https://app.notion.com/p/<org-page-id>\"]"
```

Dates use the expanded key: `"date:Date:start": "2026-07-07"` (and `date:Due:start` for Tasks).
Multi-select (`Reg exposure`) is a JSON array string: `"[\"DORA\", \"FADP\"]"`.

## Guardrails

- **Never invent select options.** Map to the closest existing value and tell the user.
- **De-dupe is the whole point.** Always search before creating a Person or Organization.
- **Don't fabricate contact details.** Leave `Email`/`LinkedIn` empty if not provided.
- **Keep insights atomic and honestly rated.** One learning per row; confidence reflects evidence.
- **Ask when genuinely ambiguous** (e.g. you can't tell the segment or whether two names are the same
  person). Otherwise pick sensible defaults and proceed — note what you assumed.
- The `🧪 Example —` records are a template; ignore them for de-dup and don't link real data to them.
