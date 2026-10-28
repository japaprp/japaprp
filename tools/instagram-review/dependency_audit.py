"""Static dependency/safety audit for the isolated Python review copies."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "tools" / "instagram-review"
STDLIB_ALLOWED = {
    "argparse", "dataclasses", "json", "os", "pathlib", "re", "statistics", "sys", "textwrap",
}
FORBIDDEN_IMPORT_ROOTS = {
    "requests", "httpx", "urllib3", "aiohttp", "socket", "webbrowser",
    "selenium", "playwright", "instagrapi", "instaloader",
}


def audit_review_scripts():
    findings = []
    for path in sorted(REVIEW_DIR.glob("*.py")):
        if path.name.startswith("test_"):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots = [node.module.split(".")[0]]
            else:
                continue
            for root in roots:
                if root in FORBIDDEN_IMPORT_ROOTS:
                    findings.append(f"{path.name}: network/browser/account module imported: {root}")
                elif root not in STDLIB_ALLOWED:
                    findings.append(f"{path.name}: dependency not allowlisted: {root}")
        source = path.read_text(encoding="utf-8")
        for token in ("os.system(", "subprocess.", "eval(", "exec(", "requests.", "httpx.", "urlopen("):
            if token in source:
                findings.append(f"{path.name}: risky operation token requires manual review: {token}")
    return findings
