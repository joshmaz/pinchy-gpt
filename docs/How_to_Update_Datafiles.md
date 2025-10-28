# How to Update Datafiles

1) Add or edit files in `/data` or `/knowledge`.
2) Update `/data/DATA_MANIFEST.yaml` with source + date.
3) Add an entry to `docs/Data_Provenance_Log.md` describing what changed and why.
4) Commit with a clear message (e.g., `data: refresh locations_by_night for current season`).

Tips:
- Prefer compact CSV for tabular data.
- Include a "Last updated" line at the top of Markdown files.