"""Tests for detecting division splits in standings."""
import unittest

from pinchy_scraper.standings import parse_standings


class TestDivisionSplit(unittest.TestCase):
    def test_division_names(self) -> None:
        """Multiple division headings should be reflected in the output records."""
        html = """
        <div>
        <h2>Standings</h2>
        <h3>A Division</h3>
        <table>
          <thead>
            <tr><th>RK</th><th>Player</th><th>Wk 1</th><th>Total</th></tr>
          </thead>
          <tbody>
            <tr><td>1</td><td>Alice</td><td>10</td><td>10</td></tr>
          </tbody>
        </table>
        <h3>B Division</h3>
        <table>
          <thead>
            <tr><th>RK</th><th>Player</th><th>1</th><th>Total</th></tr>
          </thead>
          <tbody>
            <tr><td>1</td><td>Bob</td><td>9</td><td>9</td></tr>
          </tbody>
        </table>
        </div>
        """
        res = parse_standings(html)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]["division"], "A Division")
        self.assertEqual(res[1]["division"], "B Division")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()