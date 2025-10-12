# Contributing to Pinchy-GPT

Please read this before contributing.

Branching and commits
- Create a feature branch from `main`: `git checkout -b feat/short-description`
- Make small, focused commits. Use conventional commit-style messages when possible.

Pre-commit and local checks
- Install pre-commit: `pipx install pre-commit` (or `pip install pre-commit`).
- Install hooks: `pre-commit install`.
- Run all hooks locally: `pre-commit run --all-files`.

Running CI locally
- The repository includes `scripts/validate.sh` that runs linting and basic checks.
- To run the same checks locally: `./scripts/validate.sh`.

Opening PRs
- Fork or branch from `main` and open a PR against `main`.
- Use the PR template and ensure all checks pass before requesting review.
