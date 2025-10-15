"""Parser for NEPL score sheets sections."""
from __future__ import annotations

import re
from typing import List, Dict, Optional, Any

from bs4 import BeautifulSoup

from .log import warn


def _parse_group_header(text: str) -> Optional[Dict[str, Any]]:
    """Parse a score sheet group header for location, week and group numbers.

    The expected format is something like ``"Southern New Hampshire Pinball Club - Week 6 - Group 20"``.

    Args:
        text: The header text.

    Returns:
        A dict with keys ``location_name``, ``week_number``, and ``group_number`` if parsing
        succeeds, otherwise ``None``.
    """
    # Attempt to find week and group numbers using regex
    m_week = re.search(r"week\s*(\d+)", text, re.IGNORECASE)
    m_group = re.search(r"group\s*(\d+)", text, re.IGNORECASE)
    if not m_week or not m_group:
        return None
    week_number = int(m_week.group(1))
    group_number = int(m_group.group(1))
    # Location name is everything before the first " - Week"
    parts = re.split(r"\s+-\s+week\s+\d+", text, flags=re.IGNORECASE)
    location_name = parts[0].strip() if parts else text.strip()
    return {
        "location_name": location_name,
        "week_number": week_number,
        "group_number": group_number,
    }


def _extract_games_and_totals(tables: List[Any], log: Optional[List[str]] = None) -> (List[Dict[str, Any]], List[Dict[str, Any]]):  # noqa: ANN401
    """Given a list of tables belonging to a single group, separate games from totals and parse them.

    Args:
        tables: A list of BeautifulSoup table tags.
        log: Optional log list for warnings.

    Returns:
        A tuple of (games, totals) where games is a list of game dicts and totals is a list
        of total score dicts.
    """
    game_tables: List[Any] = []
    totals_table: Optional[Any] = None
    for t in tables:
        text = t.get_text(strip=True).lower()
        if "totals" in text:
            totals_table = t
        else:
            game_tables.append(t)
    games: List[Dict[str, Any]] = []
    # Parse game tables
    for t in game_tables:
        # Determine the game title from the first <th> or a caption
        game_title: str = "Unknown"
        era: Optional[str] = None
        # Try to find a caption
        cap = t.find("caption")
        if cap and cap.get_text(strip=True):
            game_title = cap.get_text(strip=True)
        else:
            # Use the first <th> in thead if present
            th = t.find("th")
            if th and th.get_text(strip=True):
                game_title = th.get_text(strip=True)
        # Extract era tag if present at the end of title in parentheses
        m_era = re.search(r"\(([^()]+)\)\s*$", game_title)
        if m_era:
            era = m_era.group(1).strip()
            # Remove the era part from the title
            game_title = re.sub(r"\s*\([^()]+\)\s*$", "", game_title).strip()
        # Parse rows for results
        results: List[Dict[str, Any]] = []
        for row in t.find_all("tr"):
            cells = row.find_all(["td", "th"])
            if not cells:
                continue
            row_texts = [c.get_text(strip=True) for c in cells]
            # Skip header-like rows with generic column names. Only skip if the cell
            # contents exactly match "player", "score" or "points" (case-insensitive).
            lower_texts = [txt.strip().lower() for txt in row_texts]
            if any(x in {"player", "player name", "score", "points"} for x in lower_texts):
                continue
            if len(row_texts) < 2:
                continue
            # Last cell is points, second-last is score, rest is player name
            points_raw = row_texts[-1]
            score_display = row_texts[-2]
            name_parts = row_texts[:-2]
            player_name = " ".join(name_parts).strip()
            # Parse points; if not integer, keep raw
            try:
                points_val: Any = int(points_raw)
            except Exception:
                points_val = points_raw
            # Parse score_raw: remove non-digits
            cleaned = re.sub(r"[^0-9]", "", score_display)
            score_raw: Optional[int] = int(cleaned) if cleaned else None
            results.append(
                {
                    "player_name": player_name,
                    "score_display": score_display if score_display else None,
                    "score_raw": score_raw,
                    "points": points_val,
                }
            )
        if not results:
            warn(log, f"No results parsed for game '{game_title}'")
        games.append(
            {
                "title": game_title,
                "era": era,
                "results": results,
            }
        )
    # Parse totals table
    totals: List[Dict[str, Any]] = []
    if totals_table:
        for row in totals_table.find_all("tr"):
            cells = row.find_all(["td", "th"])
            if not cells:
                continue
            row_texts = [c.get_text(strip=True) for c in cells]
            # Skip header containing "Totals"
            if row_texts and re.search(r"totals", row_texts[0], re.IGNORECASE):
                continue
            if len(row_texts) < 2:
                continue
            name = row_texts[0]
            pts_raw = row_texts[-1]
            try:
                pts_int: Any = int(re.sub(r"[^0-9]", "", pts_raw))
            except Exception:
                pts_int = pts_raw
            totals.append({"player_name": name, "total_points": pts_int})
    return games, totals


def parse_score_sheets(html: str, log: Optional[List[str]] = None) -> List[Dict[str, Any]]:  # noqa: ANN401
    """Parse the NEPL season score sheets from the given HTML.

    Args:
        html: The raw HTML string of the season results page.
        log: Optional list to append warning messages to.

    Returns:
        A list of dictionaries, one per (week, location, group). Each dictionary contains
        ``week_number``, ``location_name``, ``group_number``, ``games`` (list of game dicts)
        and ``totals`` (list of totals dicts).
    """
    soup = BeautifulSoup(html, "html.parser")
    groups: List[Dict[str, Any]] = []
    # Identify all potential group header elements containing both 'Week' and 'Group'
    potential_headers = soup.find_all(
        lambda tag: (
            hasattr(tag, "get_text")
            and tag.get_text(strip=True)
            and re.search(r"week\s*\d+", tag.get_text(), re.IGNORECASE)
            and re.search(r"group\s*\d+", tag.get_text(), re.IGNORECASE)
        )
    )
    for header in potential_headers:
        header_text = header.get_text(strip=True)
        parsed = _parse_group_header(header_text)
        if not parsed:
            continue
        # Gather subsequent tables until we hit the next group header
        tables: List[Any] = []
        # Iterate through siblings following the header within the same parent
        for sibling in header.find_all_next():
            if sibling == header:
                continue
            # Break if we encounter another header element
            if (
                hasattr(sibling, "get_text")
                and sibling.get_text()
                and sibling.name in {"h1", "h2", "h3", "h4", "h5", "h6"}
                and re.search(r"week\s*\d+", sibling.get_text(), re.IGNORECASE)
                and re.search(r"group\s*\d+", sibling.get_text(), re.IGNORECASE)
            ):
                break
            if sibling.name == "table":
                tables.append(sibling)
        if not tables:
            # Nothing to parse
            warn(log, f"No tables found for group header '{header_text}'")
            continue
        games, totals = _extract_games_and_totals(tables, log)
        group_entry = {
            "week_number": parsed["week_number"],
            "location_name": parsed["location_name"],
            "group_number": parsed["group_number"],
            "games": games,
            "totals": totals,
        }
        groups.append(group_entry)
    return groups