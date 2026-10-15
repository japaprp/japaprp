#!/usr/bin/env python3
"""Validate basic structure and metadata for the repository's agent skills.

Uses only the Python standard library so CI does not need extra dependencies.
This is a structural check, not a test of an agent's reasoning or skill quality.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
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
            errors.append(f"{path.relative_to(ROOT)}: unsupported/malformed metadata line: {line!r}")
            continue
        key, value = match.groups()
        value = value.strip().strip('"').strip("'")
        if key in metadata:
            errors.append(f"{path.relative_to(ROOT)}: duplicate metadata key {key!r}")
        metadata[key] = value
    return metadata, text[end + 5 :]


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print("ERROR: skills/ directory not found")
        return 1

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
            warnings.append(f"{relative}: description is long ({len(description)} chars); consider keeping routing metadata concise")
        if not body.strip():
            errors.append(f"{relative}: skill body is empty")
        if len(body.strip()) < 80:
            warnings.append(f"{relative}: very short skill body; review whether instructions are actionable")

    print(f"Validated {len(skill_files)} skill files.")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"PASSED: structural metadata checks ({len(warnings)} warning(s)).")
    print("Note: this does not execute skills or benchmark agent behavior.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
