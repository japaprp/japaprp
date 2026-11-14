#!/usr/bin/env python3
"""Validate the project and capability registries against the local skill catalog.

Standard-library only. This checks structural references, not runtime routing behavior.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
PROJECTS_PATH = SKILLS_DIR / "registries" / "PROJECT_REGISTRY.json"
CAPABILITIES_PATH = SKILLS_DIR / "registries" / "CAPABILITY_REGISTRY.json"
INVENTORY_PATH = SKILLS_DIR / "registries" / "REPOSITORY_INVENTORY.json"
errors: list[str] = []


def load_json(path: Path, expected_kind: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path.relative_to(ROOT)}: file not found")
        return {}
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: root must be a JSON object")
        return {}
    if value.get("schema_version") != "1.0.0":
        errors.append(f"{path.relative_to(ROOT)}: schema_version must be '1.0.0'")
    if value.get("registry_kind") != expected_kind:
        errors.append(f"{path.relative_to(ROOT)}: registry_kind must be {expected_kind!r}")
    return value


def unique_ids(items: Any, field: str, label: str) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"{label}: must be an array")
        return set()
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{label}[{index}]: must be an object")
            continue
        value = item.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}[{index}]: {field} must be a non-empty string")
        elif value in seen:
            errors.append(f"{label}: duplicate {field} {value!r}")
        else:
            seen.add(value)
    return seen


def main() -> int:
    projects_data = load_json(PROJECTS_PATH, "project_registry")
    capabilities_data = load_json(CAPABILITIES_PATH, "capability_registry")
    inventory_data = load_json(INVENTORY_PATH, "repository_inventory")

    projects = projects_data.get("projects", [])
    families = capabilities_data.get("capability_families", [])
    candidates = capabilities_data.get("external_tool_candidates", [])
    repositories = inventory_data.get("repositories", [])

    project_ids = unique_ids(projects, "project_id", "projects")
    repository_ids = unique_ids(repositories, "repository_id", "repositories")
    for repository in repositories if isinstance(repositories, list) else []:
        if not isinstance(repository, dict):
            continue
        repository_id = repository.get("repository_id", "<unknown>")
        project_id = repository.get("project_id")
        if project_id not in project_ids:
            errors.append(f"repository {repository_id!r}: unknown project_id {project_id!r}")
        if not isinstance(repository.get("default_branch"), str) or not repository.get("default_branch", "").strip():
            errors.append(f"repository {repository_id!r}: default_branch must be a non-empty string")
    family_ids = unique_ids(families, "capability_id", "capability_families")
    unique_ids(candidates, "tool_id", "external_tool_candidates")

    skill_dirs = {
        path.name for path in SKILLS_DIR.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    } if SKILLS_DIR.is_dir() else set()
    if not skill_dirs:
        errors.append("skills/: no skill folders containing SKILL.md were found")

    # Project primary_capabilities currently stores skill IDs, not family IDs.
    for project in projects if isinstance(projects, list) else []:
        if not isinstance(project, dict):
            continue
        project_id = project.get("project_id", "<unknown>")
        refs = project.get("primary_capabilities", [])
        if not isinstance(refs, list):
            errors.append(f"project {project_id!r}: primary_capabilities must be an array")
            continue
        for skill_id in refs:
            if not isinstance(skill_id, str) or skill_id not in skill_dirs:
                errors.append(
                    f"project {project_id!r}: primary_capabilities references "
                    f"unknown skill {skill_id!r}"
                )

    allowed_scope_tokens = {
        "all_projects", "all_projects_when_needed", "future_business_projects"
    }
    for family in families if isinstance(families, list) else []:
        if not isinstance(family, dict):
            continue
        family_id = family.get("capability_id", "<unknown>")
        refs = family.get("skills", [])
        if not isinstance(refs, list):
            errors.append(f"capability {family_id!r}: skills must be an array")
        else:
            for skill_id in refs:
                if not isinstance(skill_id, str) or skill_id not in skill_dirs:
                    errors.append(
                        f"capability {family_id!r}: references unknown skill {skill_id!r}"
                    )
        scopes = family.get("applies_to", [])
        if not isinstance(scopes, list):
            errors.append(f"capability {family_id!r}: applies_to must be an array")
        else:
            for scope in scopes:
                if not isinstance(scope, str) or (
                    scope not in project_ids and scope not in allowed_scope_tokens
                ):
                    errors.append(
                        f"capability {family_id!r}: unknown applies_to project/scope {scope!r}"
                    )

    for candidate in candidates if isinstance(candidates, list) else []:
        if not isinstance(candidate, dict):
            continue
        tool_id = candidate.get("tool_id", "<unknown>")
        family_id = candidate.get("capability")
        if not isinstance(family_id, str) or family_id not in family_ids:
            errors.append(
                f"external tool {tool_id!r}: unknown capability family {family_id!r}"
            )
        if candidate.get("status") != "research_candidate_not_integrated":
            errors.append(
                f"external tool {tool_id!r}: candidate status must remain "
                "'research_candidate_not_integrated' until adoption is reviewed"
            )

    # Preserve the user's explicit strategic relationship and technical boundary.
    guerra = next(
        (p for p in projects if isinstance(p, dict) and p.get("project_id") == "guerra-infinita"),
        None,
    ) if isinstance(projects, list) else None
    if guerra:
        relationship = guerra.get("relationship_model", {})
        if not isinstance(relationship, dict):
            errors.append("guerra-infinita: relationship_model must be an object")
        else:
            if relationship.get("single_strategic_product_line") is not True:
                errors.append("guerra-infinita: must remain one strategic product line")
            if not relationship.get("technical_isolation"):
                errors.append("guerra-infinita: technical_isolation rule is required")
            for phase in ("research_phase", "development_phase"):
                if not isinstance(relationship.get(phase), dict):
                    errors.append(f"guerra-infinita: missing relationship_model.{phase}")

    print(
        f"Validated {len(project_ids)} projects, {len(family_ids)} capability "
        f"families, {len(repository_ids)} repositories, {len(skill_dirs)} skill folders, and "
        f"{len(candidates) if isinstance(candidates, list) else 0} external candidates."
    )
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s).")
        return 1
    print("PASSED: registry structure and cross-references.")
    print("Note: this does not execute the router or prove behavioral routing quality.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
