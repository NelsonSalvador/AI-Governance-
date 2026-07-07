# Research workflow — talk to Claude, it updates Notion

This repo doubles as the home for our **Compliant AI market-research CRM**. All the people we talk to,
the meetings we run, and what we learn live in Notion — and you update them just by *talking to Claude
Code*. Paste a Granola note or describe a call, and Claude files everything for you, linked together.

You don't need to touch Notion by hand. You don't need to remember the structure. You just talk.

## What's in the Notion CRM

Five linked databases under the **Compliant AI Adoption** page in Nelson's Notion space:

| Database | What it's for |
| --- | --- |
| **People** | Everyone in the network — prospects, buyers, champions, industry experts, advisors, investors |
| **Organizations** | Banks, insurers, universities, software houses, regulators |
| **Meetings & Notes** | Discovery calls, expert interviews, brainstorms — raw notes included |
| **Insights** | The distilled learnings: pains, objections, willingness-to-pay, competitor & regulatory signals |
| **Tasks & Follow-ups** | Action items coming out of conversations |

People ↔ Organizations ↔ Meetings ↔ Insights ↔ Tasks are all cross-linked, so you can open any
person and see every meeting, insight, and follow-up attached to them.

## One-time setup

1. **Install Claude Code** and open it in this repo folder.
2. **Connect Notion.** In Claude Code, add the Notion connector and log in with the Notion account that
   has access to the *Compliant AI Adoption* page. (Ask Nelson to share the page or the workspace with
   your Notion email if you can't see it yet.)
3. That's it. The skill in `.claude/skills/research-notion/` loads automatically when it's relevant.

## How to use it

Just tell Claude what happened. Some examples:

> **Paste raw notes:**
> "File this Granola note: *[paste]*"

> **Describe a call:**
> "I just spoke with Anna Meyer, Head of IT Risk at a mid-size cantonal bank in Zurich. Public
> ChatGPT is banned there, they want AI over internal policies but client data can't leave the country
> because of banking secrecy. She loved the audit-trail idea. Follow up: send her the one-pager."

> **Add a person to the network:**
> "Add Marc, a compliance consultant for Swiss banks, as an industry expert — met him at a conference,
> haven't spoken properly yet."

> **Log a standalone insight:**
> "Learned that universities basically won't pay per-seat — they buy at the institution level."

Claude will:
1. Find or create the **Organization** and **People** (it checks for duplicates first).
2. Create the **Meeting** with your notes in the body.
3. Pull out the **Insights** and tag them (pain / objection / willingness-to-pay / …).
4. Create any **Tasks / follow-ups**.
5. Link it all together and reply with the Notion links, flagging anything it guessed.

You can always correct it — "no, she's a Champion not the Buyer", "that org is an Insurer" — and it'll fix the records.

## Good habits

- **Dump first, tidy later.** Even a messy paste is worth filing; the structure comes for free.
- **Say who and where** if you can — a name + org + segment helps Claude link things and avoid dupes.
- **Review the Insights.** They're the real asset. Skim what Claude extracted and correct the
  confidence levels — one conversation is a *hypothesis*, not a validated fact.
- The `🧪 Example —` records show how a filed conversation looks. Delete them once you've got the hang of it.

## Under the hood (for the curious)

- The skill lives in [`.claude/skills/research-notion/SKILL.md`](.claude/skills/research-notion/SKILL.md).
- The Notion database IDs are in [`.claude/skills/research-notion/notion_ids.json`](.claude/skills/research-notion/notion_ids.json).
- It talks to Notion through the Notion MCP connector — no API keys in this repo.
