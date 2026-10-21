#!/usr/bin/env python3
"""Validate skill metadata and the machine-readable routing eval dataset.

Standard-library only. Structural checks do not evaluate an LLM's reasoning.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
EVALS_PATH = SKILLS_DIR / "tests" / "router-eval-cases.json"
errors: list[str] = []
warnings: list[str] = []


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter opener")
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter closing delimiter")
        return {}, text
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([a-zA-Z][a-zA-Z0-9_-]*):\s*(.*?)\s*$", line)
        if not match:
            errors.append(f"{path.relative_to(ROOT)}: malformed metadata line: {line!r}")
            continue
        key, value = match.groups()
        value = value.strip().strip('"').strip("'")
        if key in metadata:
            errors.append(f"{path.relative_to(ROOT)}: duplicate metadata key {key!r}")
        metadata[key] = value
    return metadata, text[end + 5 :]


def validate_skill_files() -> set[str]:
    if not SKILLS_DIR.is_dir():
        errors.append("skills/ directory not found")
        return set()
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        errors.append("No skills/*/SKILL.md files found")
    names: dict[str, Path] = {}
    for path in skill_files:
        relative = path.relative_to(ROOT)
        metadata, body = parse_frontmatter(path)
        name = metadata.get("name", "").strip()
        description = metadata.get("description", "").strip()
        expected_folder = path.parent.name
        if not name:
            errors.append(f"{relative}: missing non-empty 'name'")
        elif name in names:
            errors.append(f"{relative}: duplicate skill name {name!r} also used by {names[name].relative_to(ROOT)}")
        else:
            names[name] = path
        if name and name != expected_folder:
            errors.append(f"{relative}: name {name!r} does not match folder {expected_folder!r}")
        if not description:
            errors.append(f"{relative}: missing non-empty 'description'")
        if len(description) > 300:
            warnings.append(f"{relative}: description is long ({len(description)} chars)")
        if not body.strip():
            errors.append(f"{relative}: skill body is empty")
        elif len(body.strip()) < 80:
            warnings.append(f"{relative}: very short skill body; review actionability")
    return set(names)


def validate_eval_dataset(skill_names: set[str]) -> int:
    if not EVALS_PATH.is_file():
        errors.append(f"{EVALS_PATH.relative_to(ROOT)}: routing eval dataset is missing")
        return 0
    try:
        dataset = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{EVALS_PATH.relative_to(ROOT)}: invalid JSON: {exc}")
        return 0
    if dataset.get("schema_version") != 1:
        errors.append("router eval dataset: unsupported or missing schema_version (expected 1)")
    cases = dataset.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("router eval dataset: 'cases' must be a non-empty array")
        return 0
    seen: set[str] = set()
    required = {"id", "prompt", "expected_primary_skill", "risk", "must_avoid", "acceptance"}
    valid_risks = {"low", "medium", "high"}
    for index, case in enumerate(cases):
        prefix = f"router eval case #{index + 1}"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        missing = required - case.keys()
        if missing:
            errors.append(f"{prefix}: missing fields: {', '.join(sorted(missing))}")
            continue
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{prefix}: id must be a non-empty string")
        elif case_id in seen:
            errors.append(f"{prefix}: duplicate id {case_id!r}")
        else:
            seen.add(case_id)
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            errors.append(f"{prefix}: prompt must be a non-empty string")
        skill = case["expected_primary_skill"]
        if skill is not None and skill not in skill_names:
            errors.append(f"{prefix}: unknown expected_primary_skill {skill!r}")
        if case["risk"] not in valid_risks:
            errors.append(f"{prefix}: risk must be one of {sorted(valid_risks)}")
        for field in ("must_avoid", "acceptance"):
            if not isinstance(case[field], list) or not case[field] or not all(isinstance(v, str) and v.strip() for v in case[field]):
                errors.append(f"{prefix}: {field} must be a non-empty array of strings")

    # Activation and autonomy contracts must match the canonical PR #1 dataset.
    required_cases = {
        "activate-central-new-session": "deus é fiel",
        "autonomy-routine-work": None,
        "autonomy-impact-boundary": None,
    }
    for case_id, required_phrase in required_cases.items():
        matched = next((case for case in cases if isinstance(case, dict) and case.get("id") == case_id), None)
        if matched is None:
            errors.append(f"router eval dataset: missing required activation/autonomy case {case_id!r}")
        elif required_phrase and required_phrase.casefold() not in matched.get("prompt", "").casefold():
            errors.append(f"router eval case {case_id!r}: prompt must include {required_phrase!r}")
        elif matched.get("expected_primary_skill") != "engineering-brain-router":
            errors.append(f"router eval case {case_id!r}: expected_primary_skill must be engineering-brain-router")

    router_path = SKILLS_DIR / "engineering-brain-router" / "SKILL.md"
    if not router_path.is_file():
        errors.append("activation trigger: skills/engineering-brain-router/SKILL.md is missing")
    else:
        router_text = router_path.read_text(encoding="utf-8")
        router_lower = router_text.casefold()
        for marker in (
            "deus é fiel",
            "gatilho persistente de ativação",
            "não concede permissões novas",
            "nível 1 — rotina",
            "nível 2 — mudança reversível e isolada",
            "nível 3 — impacto/custo/permissões externos",
            "nível 4 — crítico",
        ):
            if marker.casefold() not in router_lower:
                errors.append(f"activation trigger: router skill is missing required marker {marker!r}")
    return len(cases)


def main() -> int:
    skill_names = validate_skill_files()
    case_count = validate_eval_dataset(skill_names)
    print(f"Validated {len(skill_names)} unique skill names and {case_count} routing eval cases.")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"PASSED: structural checks ({len(warnings)} warning(s)).")
    print("Note: eval cases are validated as data; this does not execute or benchmark an agent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
