# Pinchy-GPT

Pinchy-GPT: a cheerful lobster assistant for the New England Pinball League (NEPL). Centralized instructions, data sources, and CI to keep content fresh and consistent.

## Pinchy-GPT in 60 seconds

- Purpose: Provide friendly, accurate answers about NEPL events, standings, locations, and rules.
- Add canonical source docs under `/data/sources` and narrative docs under `/docs`.
- Use the `scripts/validate.sh` and pre-commit hooks to keep content consistent.

## Quickstart

1. Clone the repo and change into it:

   git clone <repo-url>
   cd pinchy-gpt

2. Install pre-commit and run hooks locally (recommended):

   pipx install pre-commit  # or: pip install pre-commit
   pre-commit install
   pre-commit run --all-files

3. Run the full validation suite:

   ./scripts/validate.sh

## Repo layout

See the repository tree for where to add docs, data sources, and prompts. Important folders:

- `docs/` - Human-facing instructions and system prompt notes
- `data/sources/` - Canonical NEPL sources, news, schedules, locations, and rules references
- `gpt/` - Prompts and packaging info for Pinchy-GPT
- `scripts/` - Local validation and formatting scripts

See `docs/pinchy/` for the current system-prompt and contributor guidance, and `docs/nepl/` for NEPL-specific notes.

## Where to add new NEPL source docs

- Put short, evergreen article summaries in `data/sources/news/` using the `_template.md` file.
- Add CSV source data to `data/sources/locations/` and `data/sources/schedules/`.

## Contributing

Please read `CONTRIBUTING.md` before opening a PR. Keep changes focused, include tests or examples where possible, and ensure `pre-commit` hooks pass.
