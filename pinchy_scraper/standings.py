"""Parser for NEPL season standings tables."""
from __future__ import annotations

import re
from typing import List, Dict, Optional

from bs4 import BeautifulSoup

from .log import warn

# Recognised header labels for key columns
RANK_HEADERS = {"rk", "rank"}
PLAYER_HEADERS = {"player", "player name", "name"}
ADJ_HEADERS = {"adj.", "adj", "adjusted"}
TOTAL_HEADERS = {"total", "points", "grand total"}


def _parse_table_headers(header_cells: List[str], log: Optional[List[str]] = None) -> Dict[str, int]:
    """Inspect header cells and return a mapping of column types to indices.

    Recognises rank, player, week numbers, adjusted and total columns. Unknown
    headers are ignored but a warning is logged.

    Args:
        header_cells: The list of header cell text strings in order of appearance.
        log: Optional list to append warning messages to.

    Returns:
        A mapping from keys (e.g. 'rank', 'player', 'adjusted', 'total', 'weeks') to
        their start index in the row. The 'weeks' key maps to a list of indices for
        each week column.
    """
    mapping: Dict[str, Any] = {}
    week_indices: List[int] = []
    for idx, cell in enumerate(header_cells):
        label = cell.strip().lower()
        # Remove common prefixes like 'wk ' or 'week '
        m = re.match(r"(?:wk|week)\s*(\d+)", label)
        if m:
            week_indices.append(idx)
            continue
        # Pure numeric column (e.g. '1', '2', ...) also treated as week
        if label.isdigit():
            week_indices.append(idx)
            continue
        # Identify rank column
        if label in RANK_HEADERS:
            mapping["rank"] = idx
            continue
        # Identify player column
        if label in PLAYER_HEADERS:
            mapping["player"] = idx
            continue
        # Identify adjusted column
        if label in ADJ_HEADERS:
            mapping["adjusted"] = idx
            continue
        # Identify total column
        if label in TOTAL_HEADERS:
            mapping["total"] = idx
            continue
        # Unknown column: log a warning
        warn(log, f"Unknown standings header '{cell}' ignored")
    mapping["weeks"] = week_indices
    return mapping


def parse_standings(html: str, log: Optional[List[str]] = None) -> List[Dict[str, Optional[str]]]:
    """Parse the NEPL season standings from the given HTML.

    Handles both pre-split (single overall table) and post-split (division
    sections with headings) formats, dynamically determining how many week
    columns are present and padding the output to eight weeks.

    Args:
        html: The raw HTML string of the season results page.
        log: Optional list to append warning messages to.

    Returns:
        A list of dictionaries, one per player row, containing the keys
        ``division``, ``rank``, ``player_name``, ``week1`` through ``week8``,
        ``adjusted``, and ``total``. Missing week values are ``None``.
    """
    soup = BeautifulSoup(html, "html.parser")
    standings: List[Dict[str, Optional[str]]] = []
    # Find all tables that appear to be standings tables
    for table in soup.find_all("table"):
        # Inspect header cells
        thead = table.find("thead")
        if not thead:
            continue
        header_cells = [th.get_text(strip=True) for th in thead.find_all(["th", "td"])]
        if not header_cells:
            continue
        # Check if this table resembles a standings table by presence of known columns
        header_map = _parse_table_headers(header_cells, log)
        # Require at least player and total columns
        if "player" not in header_map or "total" not in header_map:
            continue
        week_indices = header_map.get("weeks", [])
        # Determine division name by looking at preceding heading elements
        division = "Overall"
        # Walk backwards through siblings until we find a heading-like tag with text
        prev = table.find_previous(string=True)
        # Attempt to detect division heading between 'Standings' and the table
        current = table
        while current:
            prev_sibling = current.find_previous_sibling()
            if not prev_sibling:
                break
            # Only consider tags with visible text
            if getattr(prev_sibling, "name", None) and prev_sibling.get_text(strip=True):
                text = prev_sibling.get_text(strip=True)
                # If we find a heading containing 'division' then use it
                if re.search(r"division", text, re.IGNORECASE):
                    division = text
                    break
                # If we hit a generic 'standings' header we stop searching
                if re.search(r"standings", text, re.IGNORECASE):
                    break
            current = prev_sibling
        # Parse rows
        tbody = table.find("tbody")
        if not tbody:
            continue
        for row in tbody.find_all("tr"):
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if not cells:
                continue
            # Extract rank
            rank_val = None
            player_val = None
            adjusted_val = None
            total_val = None
            # Map known columns
            if "rank" in header_map and header_map["rank"] < len(cells):
                rank_val = cells[header_map["rank"]] or None
            if "player" in header_map and header_map["player"] < len(cells):
                player_val = cells[header_map["player"]] or None
            if "adjusted" in header_map and header_map["adjusted"] < len(cells):
                adjusted_val = cells[header_map["adjusted"]] or None
            if "total" in header_map and header_map["total"] < len(cells):
                total_val = cells[header_map["total"]] or None
            # Extract week values based on indices
            week_values: List[Optional[str]] = []
            for idx in week_indices:
                val = cells[idx] if idx < len(cells) else ""
                week_values.append(val or None)
            # Pad to 8 weeks
            if len(week_values) < 8:
                week_values.extend([None] * (8 - len(week_values)))
            elif len(week_values) > 8:
                # Trim extra week columns but warn
                warn(log, f"More than 8 week columns detected; only first 8 will be kept")
                week_values = week_values[:8]
            record: Dict[str, Optional[str]] = {
                "division": division,
                "rank": rank_val,
                "player_name": player_val,
                "week1": week_values[0],
                "week2": week_values[1],
                "week3": week_values[2],
                "week4": week_values[3],
                "week5": week_values[4],
                "week6": week_values[5],
                "week7": week_values[6],
                "week8": week_values[7],
                "adjusted": adjusted_val,
                "total": total_val,
            }
            standings.append(record)
    return standings