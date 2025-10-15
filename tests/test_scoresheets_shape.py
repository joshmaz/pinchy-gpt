"""Tests for the score sheets parser producing expected shape."""
import unittest

from pinchy_scraper.scoresheets import parse_score_sheets


class TestScoreSheetsShape(unittest.TestCase):
    def test_group_structure(self) -> None:
        """Ensure a simple score sheet group with one game and totals parses correctly."""
        html = """
        <div>
        <h2>Score Sheets</h2>
        <h3>My Club - Week 6 - Group 2</h3>
        <table>
          <thead>
            <tr><th colspan="3">Foo Bar (SS)</th></tr>
          </thead>
          <tbody>
            <tr><td>Player One</td><td>1,000</td><td>7</td></tr>
            <tr><td>Player Two</td><td>500</td><td>3</td></tr>
          </tbody>
        </table>
        <table>
          <thead>
            <tr><th>Totals</th><th></th></tr>
          </thead>
          <tbody>
            <tr><td>Player One</td><td>20</td></tr>
            <tr><td>Player Two</td><td>10</td></tr>
          </tbody>
        </table>
        </div>
        """
        res = parse_score_sheets(html)
        self.assertEqual(len(res), 1)
        group = res[0]
        self.assertEqual(group["week_number"], 6)
        self.assertEqual(group["location_name"], "My Club")
        self.assertEqual(group["group_number"], 2)
        self.assertEqual(len(group["games"]), 1)
        game = group["games"][0]
        self.assertEqual(game["title"], "Foo Bar")
        self.assertEqual(game["era"], "SS")
        self.assertEqual(len(game["results"]), 2)
        totals = group["totals"]
        self.assertEqual(len(totals), 2)
        self.assertEqual(totals[0]["player_name"], "Player One")
        # Total points should be parsed as integer
        self.assertEqual(totals[0]["total_points"], 20)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()