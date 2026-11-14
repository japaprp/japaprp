#!/usr/bin/env python3
"""Audit local project/skill/evaluation coverage without network or API calls."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
PROJECTS_FILE = SKILLS_DIR / "registries" / "PROJECT_REGISTRY.json"
CAPABILITIES_FILE = SKILLS_DIR / "registries" / "CAPABILITY_REGISTRY.json"
EVAL_FILE = SKILLS_DIR / "tests" / "router-eval-cases.json"
INVENTORY_FILE = SKILLS_DIR / "registries" / "REPOSITORY_INVENTORY.json"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def skill_ids() -> set[str]:
    found: set[str] = set()
    for path in SKILLS_DIR.glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^name:\s*([a-z0-9][a-z0-9-]*)\s*$", text)
        if not match:
            raise ValueError(f"{path.relative_to(ROOT)} has no valid name in frontmatter")
        if match.group(1) in found:
            raise ValueError(f"duplicate skill id: {match.group(1)}")
        found.add(match.group(1))
    return found


def audit() -> dict[str, Any]:
    projects = read_json(PROJECTS_FILE).get("projects", [])
    repositories = read_json(INVENTORY_FILE).get("repositories", [])
    registry = read_json(CAPABILITIES_FILE)
    families = registry.get("capability_families", [])
    candidates = registry.get("external_tool_candidates", [])
    cases = read_json(EVAL_FILE).get("cases", [])
    available = skill_ids()
    errors: list[str] = []
    warnings: list[str] = []
    referenced: set[str] = set()
    family_by_project: dict[str, list[str]] = {}

    project_ids = {p.get("project_id") for p in projects if isinstance(p, dict)}
    repository_ids = {r.get("repository_id") for r in repositories if isinstance(r, dict)}
    for repository in repositories:
        if not isinstance(repository, dict):
            errors.append("repository inventory entries must be objects")
            continue
        if repository.get("project_id") not in project_ids:
            errors.append("repository " + str(repository.get("repository_id")) + ": unknown project " + str(repository.get("project_id")))
    family_ids = {f.get("capability_id") for f in families if isinstance(f, dict)}
    if len(project_ids) != len(projects):
        errors.append("project IDs are missing or duplicated")
    if len(family_ids) != len(families):
        errors.append("capability family IDs are missing or duplicated")

    for project in projects:
        pid = project.get("project_id", "<unknown>")
        for sid in project.get("primary_capabilities", []):
            if sid not in available:
                errors.append(f"project {pid}: unknown primary capability {sid}")
        for family in families:
            scopes = family.get("applies_to", [])
            if pid in scopes or "all_projects" in scopes or "all_projects_when_needed" in scopes:
                family_by_project.setdefault(pid, []).append(family.get("capability_id", ""))
                referenced.update(family.get("skills", []))
        if project.get("portfolio_status") == "active" and not family_by_project.get(pid):
            warnings.append(f"active project {pid} has no applicable capability family")

    for family in families:
        fid = family.get("capability_id", "<unknown>")
        for sid in family.get("skills", []):
            if sid not in available:
                errors.append(f"family {fid}: unknown skill {sid}")
        for scope in family.get("applies_to", []):
            if scope not in project_ids and scope not in {
                "all_projects", "all_projects_when_needed", "future_business_projects"
            }:
                errors.append(f"family {fid}: unknown project/scope {scope}")

    unreferenced = sorted(available - referenced)
    if unreferenced:
        warnings.append("skills not referenced by a capability family: " + ", ".join(unreferenced))

    eval_ids: set[str] = set()
    eval_covered: set[str] = set()
    for case in cases:
        cid = case.get("id", "<unknown>")
        if cid in eval_ids:
            errors.append(f"duplicate eval case id: {cid}")
        eval_ids.add(cid)
        expected = case.get("expected_primary_skill")
        if expected:
            if expected not in available:
                errors.append(f"eval case {cid}: unknown expected skill {expected}")
            eval_covered.add(expected)

    untested = sorted(referenced - eval_covered)
    if untested:
        warnings.append("referenced skills without a direct primary-route eval case: " + ", ".join(untested))

    for candidate in candidates:
        if candidate.get("status") != "research_candidate_not_integrated":
            errors.append(f"external candidate {candidate.get('tool_id')}: invalid unadopted status")

    return {
        "summary": {
            "projects": len(projects),
            "repositories": len(repository_ids),
            "capability_families": len(families),
            "skills": len(available),
            "eval_cases": len(cases),
            "referenced_skills": len(referenced),
            "skills_without_direct_eval": len(untested),
            "unreferenced_skills": len(unreferenced),
            "external_candidates": len(candidates),
        },
        "warnings": warnings,
        "errors": errors,
        "status": "FAIL" if errors else ("PARTIAL" if warnings else "PASS"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    try:
        result = audit()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        summary = result["summary"]
        print("Capability coverage audit")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        print(f"STATUS: {result['status']}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
