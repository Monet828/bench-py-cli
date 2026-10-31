import os
import subprocess
import sys
import tempfile
import unittest

from expenses.core import format_summary, load_rows, summarize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE = os.path.join(ROOT, "sample.csv")


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "expenses", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class CoreTest(unittest.TestCase):
    def test_load_rows(self):
        rows = load_rows(SAMPLE)
        self.assertEqual(len(rows), 8)
        self.assertEqual(rows[0], {"date": "2026-09-01", "category": "food", "amount": 1200})

    def test_summarize(self):
        totals = summarize(load_rows(SAMPLE))
        self.assertEqual(totals, {"food": 3850, "transport": 690, "rent": 72000})

    def test_summarize_normalizes_category(self):
        rows = [
            {"date": "2026-10-01", "category": "Food", "amount": 100},
            {"date": "2026-10-02", "category": " food ", "amount": 200},
            {"date": "2026-10-03", "category": "FOOD", "amount": 300},
        ]
        self.assertEqual(summarize(rows), {"food": 600})

    def test_load_rows_normalizes_category(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "mixed.csv")
            with open(path, "w", encoding="utf-8") as f:
                f.write("date,category,amount\n2026-10-01,Food,100\n2026-10-02, FOOD ,200\n")
            rows = load_rows(path)
        self.assertEqual([r["category"] for r in rows], ["food", "food"])
        self.assertEqual(summarize(rows), {"food": 300})

    def test_format_summary(self):
        self.assertEqual(format_summary({"b": 2, "a": 1}), "a\t1\nb\t2\n合計\t3")


class CliTest(unittest.TestCase):
    def test_summary(self):
        result = run_cli("summary", SAMPLE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            ["food\t3850", "rent\t72000", "transport\t690", "合計\t76540"],
        )

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            result = run_cli("summary", os.path.join(d, "none.csv"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("見つからない", result.stderr)


if __name__ == "__main__":
    unittest.main()
