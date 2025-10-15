"""Utilities for fetching web pages with retries and a desktop user agent."""
import time
from typing import Optional

import requests

# Default desktop-like User-Agent string. It includes a reference to this package
# so downstream services can identify requests originating from this scraper.
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36 "
    "pinchy-scraper/2.0.0"
)


def fetch_html(url: str, ua: Optional[str] = None, retries: int = 3, backoff: float = 1.0) -> str:
    """Fetch a URL and return its HTML content as a string.

    Args:
        url: The full URL to fetch.
        ua: Optional user-agent string. If not provided, ``DEFAULT_UA`` is used.
        retries: How many attempts to make before giving up.
        backoff: Initial backoff delay in seconds between retries. Each retry doubles this delay.

    Returns:
        The response text on success.

    Raises:
        Exception: The last exception raised if all retries fail or the server returns a non-success status code.
    """
    headers = {
        "User-Agent": ua if ua is not None else DEFAULT_UA,
    }
    last_exception: Optional[Exception] = None
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as exc:  # noqa: BLE001
            last_exception = exc
            # Sleep before retrying, doubling the backoff each attempt
            sleep_time = backoff * (2 ** attempt)
            time.sleep(sleep_time)
    # If we get here we've exhausted retries
    assert last_exception is not None
    raise last_exception