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
                [sys.executable, str(SCRIPT), str(input_path), "--out", "swipe.md", "--json"],
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


ROUTER_SCRIPT = ROOT / "tools" / "instagram-review" / "routing.py"
ROUTER_SPEC = importlib.util.spec_from_file_location("review_routing", ROUTER_SCRIPT)
router = importlib.util.module_from_spec(ROUTER_SPEC)
sys.modules[ROUTER_SPEC.name] = router
ROUTER_SPEC.loader.exec_module(router)

BRAND_SCRIPT = ROOT / "tools" / "instagram-review" / "brand_context.py"
BRAND_SPEC = importlib.util.spec_from_file_location("review_brand_context", BRAND_SCRIPT)
brand_context = importlib.util.module_from_spec(BRAND_SPEC)
sys.modules[BRAND_SPEC.name] = brand_context
BRAND_SPEC.loader.exec_module(brand_context)

AUDIT_SCRIPT = ROOT / "tools" / "instagram-review" / "dependency_audit.py"
AUDIT_SPEC = importlib.util.spec_from_file_location("review_dependency_audit", AUDIT_SCRIPT)
dependency_audit = importlib.util.module_from_spec(AUDIT_SPEC)
sys.modules[AUDIT_SPEC.name] = dependency_audit
AUDIT_SPEC.loader.exec_module(dependency_audit)


class RoutingIsolationAndDependencyTests(unittest.TestCase):
    def test_general_affiliate_content_routes_to_primary_workflow_only(self):
        result = router.route_content(platform="Kwai", intent="criar legenda de produto afiliado")
        self.assertEqual(result.primary, "content-commerce-distribution")
        self.assertEqual(result.optional, ())

    def test_instagram_caption_uses_specific_module_without_replacing_primary(self):
        result = router.route_content(platform="Instagram", intent="revisar legenda")
        self.assertEqual(result.primary, "content-commerce-distribution")
        self.assertIn("ig-caption", result.optional)

    def test_instagram_reel_benchmark_routes_to_ig_viral(self):
        result = router.route_content(platform="Instagram Reels", intent="benchmark de reels por mediana")
        self.assertIn("ig-viral", result.optional)

    def test_publishing_request_stays_draft_review_only(self):
        result = router.route_content(platform="Instagram", intent="publicar automaticamente")
        self.assertIn("draft/review only", result.reason)

    def test_missing_or_unknown_brand_fails_closed(self):
        for value in ("", "unknown", "casa pratica"):
            with self.subTest(brand=value):
                with self.assertRaises(ValueError):
                    brand_context.select_brand_context(value)

    def test_brand_contexts_are_separate_and_canonical(self):
        casa = brand_context.select_brand_context("casa_pratica_ofc")
        renascer = brand_context.select_brand_context("instancia_renascer_belvedere")
        self.assertNotEqual(casa["brand_id"], renascer["brand_id"])
        self.assertIn("affiliate home products", casa["allowed_context"])
        self.assertNotIn("affiliate home products", renascer["allowed_context"])
        self.assertIn("organization identity", renascer["allowed_context"])
        self.assertNotIn("organization identity", casa["allowed_context"])
        casa["allowed_context"] = "tampered"
        self.assertNotEqual(brand_context.select_brand_context("casa_pratica_ofc")["allowed_context"], "tampered")

    def test_static_dependency_audit_has_no_findings(self):
        self.assertEqual(dependency_audit.audit_review_scripts(), [])


class CanonicalRoutingAndEndToEndBrandTests(unittest.TestCase):
    def test_canonical_router_document_is_source_of_truth(self):
        router_doc = ROOT / "skills" / "engineering-brain-router" / "SKILL.md"
        text = router_doc.read_text(encoding="utf-8")
        self.assertIn("Esta seção é a **fonte de verdade**", text)
        self.assertIn("content-commerce-distribution", text)
        self.assertIn("ig-viral", text)
        self.assertIn("falhar fechado", text)
        self.assertIn("oráculo de regressão/teste", text)

    def test_synthetic_brand_payloads_are_isolated_end_to_end(self):
        casa = brand_context.build_brand_payload(
            "casa_pratica_ofc",
            {"product_facts": ["pote com tampa"], "verified_affiliate_links": ["https://example.test/casa"]},
        )
        renascer = brand_context.build_brand_payload(
            "instancia_renascer_belvedere",
            {"organization_facts": ["comunicado institucional"], "official_links": ["https://example.test/renascer"]},
        )
        self.assertEqual(casa["brand"]["brand_id"], "casa_pratica_ofc")
        self.assertEqual(renascer["brand"]["brand_id"], "instancia_renascer_belvedere")
        self.assertNotIn("organization_facts", casa["facts"])
        self.assertNotIn("product_facts", renascer["facts"])
        self.assertNotIn("https://example.test/renascer", str(casa))
        self.assertNotIn("https://example.test/casa", str(renascer))

    def test_cross_brand_fact_injection_is_rejected(self):
        with self.assertRaises(ValueError):
            brand_context.build_brand_payload("casa_pratica_ofc", {
                "product_facts": ["item"],
                "organization_facts": ["should not leak"],
            })
        with self.assertRaises(ValueError):
            brand_context.build_brand_payload("instancia_renascer_belvedere", {
                "approved_announcements": ["comunicado"],
                "verified_affiliate_links": ["https://example.test/affiliate"],
            })

    def test_upstream_license_notice_is_present(self):
        license_path = ROOT / "tools" / "instagram-review" / "LICENSE-MIT.txt"
        self.assertTrue(license_path.is_file())
        text = license_path.read_text(encoding="utf-8")
        self.assertIn("Permission is hereby granted", text)

    def test_source_inventory_is_valid_and_uses_exact_blob_shas(self):
        import json
        inventory_path = ROOT / "tools" / "instagram-review" / "source-inventory.json"
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(len(inventory["external_sources"]), 2)
        for source in inventory["external_sources"]:
            self.assertTrue((ROOT / source["license_file"]).is_file())
            for item in source["files"]:
                self.assertEqual(len(item["git_blob_sha"]), 40)
                self.assertTrue(all(ch in "0123456789abcdef" for ch in item["git_blob_sha"]))
                self.assertTrue((ROOT / item["local_copy"]).is_file())


if __name__ == "__main__":
    unittest.main()
