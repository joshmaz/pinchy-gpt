#!/usr/bin/env python3
"""Command-line interface for scraping NEPL season results.

This script fetches the season results page, parses both the standings and the
score sheets sections, and writes two JSON files to the specified output
directory. Each output includes metadata for provenance and a log of any
warnings encountered during parsing.

Example usage::

    python scripts/nepl_scraper.py --season 35 --outdir data

The script prints the paths of the generated JSON files on success and exits
with status 0. If no data could be parsed, the exit status is non-zero.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pinchy_scraper.fetch import fetch_html
from pinchy_scraper.standings import parse_standings
from pinchy_scraper.scoresheets import parse_score_sheets
from pinchy_scraper.io import make_metadata, write_json
from pinchy_scraper import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download and parse NEPL season results into JSON")
    parser.add_argument("--season", type=int, required=True, help="Season number to scrape (e.g. 35)")
    parser.add_argument("--outdir", type=str, default=".", help="Directory to write output JSON files")
    parser.add_argument("--user-agent", type=str, default=None, help="Custom User-Agent header for HTTP requests")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging to stderr")
    args = parser.parse_args(argv)

    season = args.season
    outdir = Path(args.outdir)
    url = f"https://nepl.org/results/season-{season}"
    try:
        html = fetch_html(url, ua=args.user_agent)
    except Exception as exc:
        print(f"Error: failed to fetch {url}: {exc}", file=sys.stderr)
        return 1
    # Collect warnings during parsing
    log: list[str] = []
    standings = parse_standings(html, log=log)
    score_sheets = parse_score_sheets(html, log=log)
    # Build metadata and file names
    generator_version = f"pinchy-scraper/{__version__}"
    metadata = make_metadata(season_number=season, source_url=url, generator_version=generator_version)
    date_str = metadata["capture_timestamp"][:10]  # YYYY-MM-DD
    # Prepare outputs
    standings_data = {
        "metadata": metadata,
        "standings": standings,
        "log": log,
    }
    standings_fname = f"nepl_standings_season_{season}_{date_str}.json"
    standings_path = outdir / standings_fname
    scores_data = {
        "metadata": metadata,
        "score_sheets": score_sheets,
        "log": log,
    }
    scores_fname = f"nepl_scoresheets_season_{season}_{date_str}.json"
    scores_path = outdir / scores_fname
    # Write files
    write_json(standings_data, str(standings_path))
    write_json(scores_data, str(scores_path))
    # Print output paths for user visibility
    print(str(standings_path))
    print(str(scores_path))
    # Determine exit status: non-zero if no data was scraped
    if not standings and not score_sheets:
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())