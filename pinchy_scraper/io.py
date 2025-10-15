"""Input/output utilities for writing JSON with metadata and timestamps."""
import json
import os
from datetime import datetime
from typing import Any, Dict


def current_timestamp() -> str:
    """Return the current UTC timestamp in ISO 8601 format (no microseconds)."""
    # Use Z suffix to indicate UTC
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def make_metadata(season_number: int, source_url: str, generator_version: str) -> Dict[str, Any]:
    """Construct a metadata dictionary for a scraped season.

    Args:
        season_number: The NEPL season number.
        source_url: The URL from which data was fetched.
        generator_version: A version string identifying this scraper.

    Returns:
        A dict containing the basic metadata fields expected in the JSON outputs.
    """
    return {
        "season_number": season_number,
        "source_url": source_url,
        "capture_timestamp": current_timestamp(),
        "generator_version": generator_version,
    }


def write_json(data: Dict[str, Any], path: str) -> None:
    """Write a Python object to a file in JSON format.

    Args:
        data: The data to serialise. Must be JSON serialisable.
        path: Path to the output file.
    """
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)