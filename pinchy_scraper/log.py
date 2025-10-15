"""Simple logger helper for collecting warnings during parsing.

The scraper collects human-readable messages about unexpected HTML structures or
unknown fields encountered during parsing. These messages are appended to a
list passed into the parsing functions. The log can then be included in the
resulting JSON output to aid debugging and provenance.
"""
from typing import List, Optional


def warn(log: Optional[List[str]], message: str) -> None:
    """Append a warning message to the provided log list.

    Args:
        log: A list of strings to append the message to. If ``None``, the
            message is silently ignored.
        message: The warning message.
    """
    if log is not None:
        log.append(str(message))