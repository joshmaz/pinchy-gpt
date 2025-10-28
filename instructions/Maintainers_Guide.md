# Maintainers Guide

## Goals

Keep Pinchy's content minimal, trustworthy, and easy to update.

## Update Steps

1) Edit or add files in `/data` or `/knowledge`.
2) Update `/data/DATA_MANIFEST.yaml` with source, last refresh date, and checksum (optional).
3) Log changes in `CHANGELOG.md`.

## File Types

- Markdown (`.md`) for long-form pages.
- CSV/JSON for tables/lists.
- Keep titles and H1s descriptive; include a "Last updated" line.

## Provenance

For each added/changed dataset, include:

- Source URL/domain
- Capture method (manual copy, export)
- Timestamp of capture
