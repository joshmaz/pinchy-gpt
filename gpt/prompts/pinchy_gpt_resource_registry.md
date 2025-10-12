# Pinchy‑GPT Resource Registry

A living catalog of external pinball resources Pinchy‑GPT can reference. Keep this document current; the prompt will include a *Routing Rules* summary derived from here.

---

## Sources

### NEPL Official
- **Domain**: nepl.org
- **Purpose**: Canonical schedules, rules, weekly/season results, standings, locations.
- **When to use**: Any NEPL‑specific question. Treat as source of truth over all others.
- **Key paths**: `/schedule`, `/rules`, `/results`, `/locations`
- **Notes**: Prefer freshest “current season” pages; fall back to season‑NN archives.

### Pinball Map (PBM)
- **Domain**: pinballmap.com
- **Purpose**: On‑location machine listings, nearby locations, latest machines per venue.
- **When to use**: “What machines are at X?”, “What’s near me (zip/city)?”, machine availability.
- **Key paths**: `/map`, `/region/*`, venue pages
- **Priority**: Use PBM for public location machine lists (never guess).

### IFPA Rankings
- **Domain**: ifpapinball.com
- **Purpose**: Player rankings, tournament results, player IDs.
- **When to use**: “What’s Josh’s IFPA rank?”, “Show top N in MA/NE,” etc.
- **Key paths**: `/rankings`, `/player/ID`, `/tournaments`

### Match Play Events
- **Domain**: matchplay.events
- **Purpose**: Event pages, standings, round‑by‑round results for tournaments.
- **When to use**: Questions about specific events run on Match Play.

### IPDB (Internet Pinball Database)
- **Domain**: ipdb.org
- **Purpose**: Machine reference data (year, manufacturer, rule cards, flyers).
- **When to use**: Machine history/specs; not location availability.

### Pinside
- **Domain**: pinside.com
- **Purpose**: Community discussions, shop logs, marketplace; secondary machine info.
- **When to use**: Context/opinions or parts discussions when official docs lack details.
- **Caution**: Treat as community info; avoid as sole source for factual claims.

### PinWiki
- **Domain**: pinwiki.com
- **Purpose**: Technical repair/maintenance guides.
- **When to use**: Repair/tech guidance references.

### Tilt Forums
- **Domain**: tiltforums.com
- **Purpose**: Competitive rules clarifications, rulings examples.
- **When to use**: Rules nuance beyond NEPL rules; cite clearly.

### Kineticist
- **Domain**: kineticist.co
- **Purpose**: Pinball news, media releases, manufacturer announcements, interviews, and community insights.
- **When to use**: Questions about new machine reveals, media coverage, or general pinball news.
- **Notes**: Treat as a journalism source—helpful for commentary or summaries, but verify against manufacturer sites for specifications.

### Scorbit
- **Domain**: scorbit.io / app.scorbit.io
- **Purpose**: Live/archived scores for connected games.
- **When to use**: Score lookups if a venue/game is Scorbit‑enabled.

### Stern Insider Connected
- **Domain**: insider.sternpinball.com
- **Purpose**: Achievements, leaderboards for IC‑enabled Stern machines.
- **When to use**: Feature/leaderboard references if public pages available.

### Jersey Jack Pinball (JJP)
- **Domain**: jerseyjackpinball.com
- **Purpose**: Code updates, manuals, game info (JJP titles).
- **When to use**: Official JJP references.

### Boston Pinball Repair Stats
- **Domain**: (varies; often mirrored)
- **Purpose**: eBay price guides and reliability stats.
- **When to use**: Historical pricing context; cite cautiously.

### Vendors (Parts & Docs)
- **Domains**: marco-specialties.com, pinballlife.com, cometpinball.com
- **Purpose**: Parts availability/spec sheets.
- **When to use**: Parts sourcing references.

---

## Routing Rules (to mirror in the prompt)
1. **NEPL** overrides all other sources for league matters (schedule, rules, standings, locations).
2. **Pinball Map** is the *only* allowed source for public on‑location machine lists.
3. **IFPA** is authoritative for global/regional player rankings and IFPA event results.
4. **Match Play** is authoritative for events hosted on Match Play.
5. **Kineticist** may be referenced for pinball news, interviews, or release coverage.
6. **IPDB/PinWiki** for machine facts and repair; clearly distinguish fact vs. community opinion (Pinside/Tilt Forums).
7. When sources disagree, report the discrepancy and prefer the higher‑authority source per rules 1–5.
8. Always include links/citations to the exact referenced page when answering.

---

## Answer Patterns (snippets to reuse)
- **Venue machines**: “According to Pinball Map (updated <date>), <Venue> lists: …”
- **League rules**: “Per NEPL Rules <version/date>, …”
- **Player rank**: “IFPA shows <Player> at rank <#> (as of <date>).”
- **News**: “As covered by Kineticist on <date>, …”

---

## Open Questions / To‑Do
- Add NEPL JSON endpoints if any become available.
- Define supported geographies/regions for PBM queries (default: New England).
- Add caching notes and freshness thresholds per source.

---

*Maintainers*: Josh (owner), Pinchy‑GPT (editor)
*Changelog*: v0.2 — added Kineticist as a news/media source.

