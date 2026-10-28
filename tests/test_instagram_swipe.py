import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "instagram-review" / "swipe.py"
SPEC = importlib.util.spec_from_file_location("review_swipe", SCRIPT)
swipe = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = swipe
SPEC.loader.exec_module(swipe)


class SwipeRegressionTests(unittest.TestCase):
    def test_mixed_median_rows_do_not_mix_baselines(self):
        rows = [
            {"account": "@a", "views": 1200, "median": 400, "followers": 9000, "hook": "Você está perdendo dinheiro"},
            {"account": "@b", "views": 5000, "median": None, "followers": 1000, "hook": "Como economizar hoje"},
        ]
        result = swipe.analyse(rows, None)
        by_account = {r["account"]: r for r in result["reels"]}
        self.assertEqual(by_account["@a"]["baseline_type"], "account median")
        self.assertEqual(by_account["@a"]["outlier"], 3.0)
        self.assertEqual(by_account["@b"]["baseline_type"], "unavailable")
        self.assertIsNone(by_account["@b"]["outlier"])
        self.assertIsNone(by_account["@b"]["baseline"])

    def test_follower_baseline_used_only_when_no_medians_exist(self):
        rows = [
            {"account": "@a", "views": 1200, "median": None, "followers": 400, "hook": "Você precisa ver isto"},
            {"account": "@b", "views": 5000, "median": None, "followers": 1000, "hook": "Veja como funciona"},
        ]
        result = swipe.analyse(rows, None)
        by_account = {r["account"]: r for r in result["reels"]}
        self.assertEqual(by_account["@a"]["baseline_type"], "follower count")
        self.assertEqual(by_account["@a"]["outlier"], 3.0)
        self.assertEqual(by_account["@b"]["outlier"], 5.0)

    def test_zero_baseline_is_not_reported_as_a_real_multiple(self):
        rows = [{"account": "@a", "views": 1200, "median": None, "followers": None, "hook": "Teste de gancho"}]
        result = swipe.analyse(rows, None)
        self.assertIsNone(result["reels"][0]["outlier"])
        self.assertEqual(result["reels"][0]["baseline_type"], "unavailable")

    def test_output_filename_without_parent_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.tsv"
            output_path = Path(tmp) / "swipe.md"
            input_path.write_text("account\tfollowers\tviews\thook\n@conta\t100\t300\tComo economizar hoje\n", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(input_path), "--out", str(output_path), "--json"],
                capture_output=True, text=True, cwd=tmp, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(output_path.is_file())
            self.assertIn("# Swipe file", output_path.read_text(encoding="utf-8"))

    def test_portuguese_hook_is_preserved_in_output(self):
        rows = [{"account": "@casa", "views": 900, "median": 300, "followers": 2000,
                 "hook": "Sua cozinha organizada sem gastar muito"}]
        result = swipe.analyse(rows, None)
        self.assertEqual(result["reels"][0]["hook"], "Sua cozinha organizada sem gastar muito")
        self.assertEqual(result["reels"][0]["outlier"], 3.0)


if __name__ == "__main__":
    unittest.main()
