---
name: market-analysis
description: Research a company and add it to the Compliant AI "Market Analysis" database in Notion. Use whenever the user names a company or pastes a company URL and wants it tracked / analyzed / added to the market map — e.g. "add Vanta to market analysis", "research cohere.com and log it", "add these competitors". Researches funding, size, business model, and regulation-dependence, then creates or updates one linked row with deep notes.
---

# Company → Market Analysis (Notion)

Turn a company name or URL into a clean, researched row in the **Market Analysis** database in the
Compliant AI research workspace. This is the competitor / adjacent / benchmark map for the project.

## When to use this

- "Add {company} to market analysis" / "log {company}" / "research {url} and add it"
- The user pastes one or more company names/URLs to track.
- Any time a new competitor, adjacent, or reference company comes up and should be captured.

If the user is just *asking about* a company (not tracking it), answer — don't write — unless they say to add it.

## Prerequisites

- **Notion connector** enabled (load via ToolSearch: `notion search fetch create-pages update-page query-data-sources`).
- **Web access** — load `WebSearch` and `WebFetch` via ToolSearch. Always research live; do not rely on
  memory for funding/valuation/headcount, which go stale fast.

## The target database

**Market Analysis** — `data_source_id`: `0f8dda5c-1eb0-49e6-bc9c-797b56786a11`
(also in [`../research-notion/notion_ids.json`](../research-notion/notion_ids.json)).

### Property schema (use exact names + option values)

- `Name` (title) · `Website` (url) · `Founded` (number, year) · `Key investors` (text) · `Notes` (text)
- `Category` (select): `Foundation model`, `Sovereign cloud/infra`, `Compliance/GRC platform`,
  `App / last-mile AI`, `Confidential computing`, `AI security`, `Other`
- `HQ country` (select): `USA`, `Canada`, `Germany`, `France`, `Switzerland`, `UK`, `Other`
- `Headcount` (select): `1-50`, `51-200`, `201-500`, `501-1000`, `1000+`
- `Latest funding` (text) — round + amount + lead + date, e.g. "$150M Series D, Jul 2025, led by Wellington"
- `Total raised` (text) · `Valuation` (text) · `ARR` (text) — keep these as text so you can add "~" and dates
- `Latest round` (select): `Seed`, `Series A`, `Series B`, `Series C`, `Series D`, `Series E+`,
  `Public`, `Acquired`, `Bootstrapped`
- `Business model` (text) — how they make money + deployment model, one or two sentences
- `Regulation-driven?` (select): `Core to the business` (they exist because of regulation, e.g. a GRC
  platform), `Strong tailwind` (regulation is a major sales driver), `Some tailwind`, `Neutral`
- `Relevance to us` (select): `Direct competitor`, `Adjacent`, `Reference/benchmark`,
  `Potential partner`, `Context`
- `Target segment` (multi-select, JSON array string): `Banks`, `Insurers`, `Enterprise`,
  `Startups/SMB`, `Public sector`, `Healthcare`, `All regulated`

## Workflow

1. **De-dupe first.** Query the DB for the company name
   (`SELECT url, "Name" FROM "collection://0f8dda5c-1eb0-49e6-bc9c-797b56786a11" WHERE "Name" LIKE ?`).
   If it exists, **update** that row instead of creating a duplicate.
2. **Research live** (keep it proportionate — a "small research" ask = 1–2 searches + a homepage fetch):
   - `WebSearch`: "{company} funding valuation latest round employees business model {current year}".
   - `WebFetch` the company homepage: core product, business model, target customers, and any
     emphasis on **security / privacy / data residency / sovereignty / regulation**.
3. **Fill the row.** Set every field you can confidently source; **leave unknowns blank** rather than
   guessing. Prefix soft numbers with "~" and add the date/quarter (funding data ages fast).
4. **Judge the two opinion fields yourself** — they're the point of the table:
   - `Regulation-driven?` — is regulation the reason they exist, a tailwind, or irrelevant?
   - `Relevance to us` — competitor / adjacent / benchmark / partner, from the Compliant-AI-wedge POV.
5. **Write a short page body** (see structure below) with the detail behind the columns.
6. **Report back**: the Notion link, a 2–3 line summary, and flag any figures you're unsure about or
   couldn't find. If the user gave several companies, do them all, then summarize as a list.

### Page body structure

```
## Snapshot
One or two lines: what they are, where, size, headline valuation.

## Funding timeline
Bulleted rounds (amount · date · lead · valuation). ARR/margin if known.

## Product & model
What they sell and how they make money. Notable customers.

## Regulation angle → {the tag you chose}
Why regulation does or doesn't drive their business.

## Why it matters to us
Competitor / adjacent / benchmark — the honest read from our wedge.
```

## Guardrails

- **Research before writing.** Never fill funding/valuation/headcount from memory — verify each run.
- **Cite uncertainty.** If sources conflict (common for valuations), pick the best-sourced and note it.
- **Never invent select options.** Map to the closest existing value.
- **De-dupe** — one row per company; update, don't duplicate.
- Keep it **proportionate** to the ask — "quick look" ≠ a 10-search deep dive.
