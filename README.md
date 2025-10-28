# Pinchy-GPT (NEPL helper)

Pinchy-GPT is a cheerful lobster who helps New England Pinball League (NEPL) members find schedules, locations, rules, and pointers to official resources.  
This repo is a **simple, public home for Pinchy's instructions and static data** used by a custom ChatGPT—no code, builds, or scrapers.

## What's here
- **/instructions** – The Pinchy system prompt + routing rules for how Pinchy answers.
- **/data** – Static CSV/JSON/MD tables you want Pinchy to reference.
- **/knowledge** – Long-form Markdown summaries you want Pinchy to cite.
- **/docs** – Maintainer docs (how to update, provenance, etc.).
- **/sources** – External resource registry (domains, official pages).

## How Pinchy uses this
You'll upload selected files from this repo to your custom ChatGPT as "knowledge." Pinchy will:
- Prefer official NEPL sources.
- Never fabricate info.
- Cite or point users to source pages when relevant links exist.

## Contributing
Open a PR that:
1) Updates or adds data/knowledge files,
2) Updates `DATA_MANIFEST.yaml` (source + timestamp),
3) Notes changes in `CHANGELOG.md`.

## License
MIT — see `LICENSE`.