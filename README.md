# AI Governance — Market Research & Product Discovery System

> **This is not a product. There is no app or MVP here.** It's a *research operating system*:
> a way to turn scattered conversations into a structured, queryable market-research base — just by
> talking to Claude Code, which files everything into Notion for you.

We're investigating a question, not shipping software (yet):

> **Do regulated organisations in the EU & Switzerland — banks, insurers, universities, software
> houses — have a real, painful, fundable problem using AI on sensitive data?**
> (They can't put client data in public tools like ChatGPT because of DORA, the revised FADP, GDPR
> and Swiss banking secrecy.) Before building anything, we're verifying that with real people.

This repo is the connective tissue that makes that research compound instead of scattering across
notebooks, inboxes, and memory.

## What it is (and isn't)

- ✅ A system for capturing and structuring **customer discovery + market research**.
- ✅ A shared brain your whole team updates **just by talking to Claude Code** — paste a Granola note,
  describe a call, and it's filed, linked, and de-duplicated.
- ❌ **Not** a product, app, or MVP. Nothing to install or run. No source code to build.

## The research lives in Notion

Everything is captured in **six linked databases** under the **Compliant AI Adoption** page:

| Database | What it holds |
| --- | --- |
| **People** | Everyone we talk to — prospects, buyers, champions, industry experts, advisors, investors |
| **Organizations** | Banks, insurers, universities, software houses, regulators |
| **Meetings & Notes** | Discovery calls, expert interviews, brainstorms — raw notes in the page body |
| **Insights** | The distilled learnings: pains, objections, willingness-to-pay, competitor & regulatory signals |
| **Tasks & Follow-ups** | Action items from conversations |
| **Regulations** | Reference: DORA, FADP, EU AI Act, GDPR, NIS2, banking secrecy — and how each is a sales hook |

People ↔ Organizations ↔ Meetings ↔ Insights ↔ Tasks are all cross-linked, so you can open any
person and see every meeting, insight, and follow-up attached to them.

## How it works

```
You  ──"here's my call note / I just spoke with…"──▶  Claude Code
                                                        │  (research-notion skill)
                                                        ▼
                        Notion:  People · Organizations · Meetings · Insights · Tasks
                                 (found-or-created, linked, de-duplicated)
```

You never touch Notion's structure by hand. You talk; Claude files.

## Setup (one-time, ~5 minutes)

1. **Install [Claude Code](https://claude.com/claude-code)** and open it in this repo folder.
2. **Connect Notion.** In Claude Code, add the Notion connector and sign in with the Notion account
   that can see the *Compliant AI Adoption* page.
3. **Get access.** If you can't see that page, ask Nelson to share it (or the workspace) with your
   Notion email.

That's it. The skill in `.claude/skills/research-notion/` loads automatically when it's relevant.

## How to use it

Just tell Claude what happened:

> **Paste raw notes:** "File this Granola note: *[paste]*"

> **Describe a call:** "I spoke with a Head of IT Risk at a mid-size cantonal bank in Zurich. Public
> ChatGPT is banned, they want AI over internal policies but client data can't leave the country. She
> loved the audit-trail idea. Follow up: send the one-pager."

> **Add a contact:** "Add Marc, a compliance consultant for Swiss banks, as an industry expert."

> **Log a standalone insight:** "Learned that universities won't pay per-seat — they buy at the
> institution level."

Claude finds-or-creates the People and Organizations (checking for duplicates), creates the Meeting
with your notes, extracts and tags the Insights, creates any Tasks, links it all together, and replies
with the Notion links — flagging anything it guessed so you can correct it.

## Good habits

- **Dump first, tidy later.** Even a messy paste is worth filing.
- **Say who + where** if you can (name, org, segment) — it helps Claude link things and avoid dupes.
- **Review the Insights** — they're the real asset. Correct the confidence levels: one conversation is
  a *hypothesis*, not a validated fact.
- The `🧪 Example —` records show how a filed conversation looks. Delete them once you're comfortable.

## What's in this repo

- **[`.claude/skills/research-notion/SKILL.md`](.claude/skills/research-notion/SKILL.md)** — the
  instructions Claude Code follows to file research into Notion.
- **[`.claude/skills/research-notion/notion_ids.json`](.claude/skills/research-notion/notion_ids.json)** —
  the Notion database IDs the skill writes to.
- **`README.md`** — this file.

No API keys live in this repo; it talks to Notion through the Notion MCP connector you authorise in
Claude Code.
