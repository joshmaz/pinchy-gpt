"""Tests for dynamic week header handling in standings parser."""
import unittest

from pinchy_scraper.standings import parse_standings


class TestWeekHeaders(unittest.TestCase):
    def test_dynamic_weeks_padded(self) -> None:
        """Ensure week columns are padded to eight entries when fewer are present."""
        html = """
        <div>
          <h2>Standings</h2>
          <table>
            <thead>
              <tr><th>RK</th><th>Player</th><th>Wk 1</th><th>Wk 2</th><th>Adj.</th><th>Total</th></tr>
            </thead>
            <tbody>
              <tr><td>1</td><td>Alice</td><td>10</td><td>20</td><td></td><td>30</td></tr>
            </tbody>
          </table>
        </div>
        """
        res = parse_standings(html)
        self.assertEqual(len(res), 1)
        row = res[0]
        self.assertEqual(row["week1"], "10")
        self.assertEqual(row["week2"], "20")
        # Weeks 3-8 should be None
        for i in range(3, 9):
            self.assertIsNone(row[f"week{i}"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()