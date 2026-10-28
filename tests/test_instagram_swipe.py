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


CAPTION_SCRIPT = ROOT / "tools" / "instagram-review" / "caption.py"
CAPTION_SPEC = importlib.util.spec_from_file_location("review_caption", CAPTION_SCRIPT)
caption = importlib.util.module_from_spec(CAPTION_SPEC)
sys.modules[CAPTION_SPEC.name] = caption
CAPTION_SPEC.loader.exec_module(caption)

HOOK_IG_SCRIPT = ROOT / "tools" / "instagram-review" / "hookscore_instagram.py"
HOOK_IG_SPEC = importlib.util.spec_from_file_location("review_hookscore_ig", HOOK_IG_SCRIPT)
hook_ig = importlib.util.module_from_spec(HOOK_IG_SPEC)
sys.modules[HOOK_IG_SPEC.name] = hook_ig
HOOK_IG_SPEC.loader.exec_module(hook_ig)

HOOK_VIRAL_SCRIPT = ROOT / "tools" / "instagram-review" / "hookscore_virality.py"
HOOK_VIRAL_SPEC = importlib.util.spec_from_file_location("review_hookscore_virality", HOOK_VIRAL_SCRIPT)
hook_virality = importlib.util.module_from_spec(HOOK_VIRAL_SPEC)
sys.modules[HOOK_VIRAL_SPEC.name] = hook_virality
HOOK_VIRAL_SPEC.loader.exec_module(hook_virality)


class CaptionAndHookScoreTests(unittest.TestCase):
    def test_brazilian_portuguese_caption_preserves_links_and_accents(self):
        text = "Sua cozinha organizada sem gastar muito. Confira: https://example.com/produto\n#CasaPratica"
        result = caption.analyse(text)
        self.assertIn("cozinha organizada", result["visible"])
        self.assertIn("https://example.com/produto", result["links"][0])
        self.assertIn("#CasaPratica", result["hashtags"])
        self.assertEqual(text.strip(), text)  # linter analyzes; it does not rewrite the draft

    def test_caption_does_not_claim_link_is_clickable(self):
        result = caption.analyse("Veja os detalhes: https://example.com/produto")
        link_check = next(c for c in result["checks"] if c["check"] == "LINKS")
        self.assertEqual(link_check["status"], "WARN")
        self.assertIn("not clickable", link_check["detail"])

    def test_hook_scoring_panel_is_equivalent_for_representative_inputs(self):
        examples = [
            "Você está perdendo R$ 200 por mês sem perceber",
            "Como organizar sua cozinha em 5 minutos",
            "Hey guys, welcome to my video",
            "Sua casa merece mais praticidade",
            "Pare de cometer este erro na cozinha",
        ]
        for hook in examples:
            with self.subTest(hook=hook):
                ig_results, ig_score, ig_verdict, ig_flags = hook_ig.run(hook)
                vir_results, vir_score, vir_verdict, vir_flags = hook_virality.run(hook)
                self.assertEqual(ig_results, vir_results)
                self.assertEqual(ig_score, vir_score)
                self.assertEqual(ig_verdict, vir_verdict)
                self.assertEqual(ig_flags, vir_flags)


if __name__ == "__main__":
    unittest.main()
