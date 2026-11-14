# Conselho Central — engine and subsystem status

Audit snapshot: 2026-11-14. Scope: the Council Central repository `japaprp/japaprp` and its agent-routing/governance machinery. This is not a health check of the separate Dark War REA, Guerra Infinita, Casa Prática, or other application runtimes.

## Executive result

The repository has a working structural catalog and CI validation, but it does not yet have a self-running agent orchestrator that guarantees skill loading, autonomous external discovery, or 100% task success. The main unfinished area is behavioral execution in the target agent/client, not missing documentation.

| Engine / subsystem | Verified state | Status | Remaining work |
|---|---|---|---|
| Skill catalog and metadata validator | 36 unique skills; structural validator and catalog checks pass on this branch | PASS — structural | Continue periodic overlap and maintenance review |
| Project registry | 6 project records, with active/planned status and evidence qualifiers | PASS — structural | Re-verify each project's live repository before project-specific operations |
| Capability registry | 12 capability families map all 36 skills; 2 external research candidates remain explicitly unintegrated | PASS — structural | Keep candidate state/evidence current and re-check project applicability |
| Engineering Brain router | Routing, project isolation, skill budget, autonomy and approval boundaries documented | PARTIAL | Runtime depends on the host loading repository instructions and selected skills |
| Activation bootstrap | AGENTS.md and Copilot repository instructions contain the trigger procedure; deterministic structural test exists | PARTIAL | Fresh-session activation in each target client has not been behaviorally proven |
| Capability gap closure | Dedicated skill, router dispatch, internal-first/external GitHub discovery contract, isolated closure procedure and regression coverage exist | PASS — structural; PARTIAL — behavior | Prove the target agent actually discovers, compares and closes a gap in a fresh session |
| Ponytail engineering principles | Selective local minimal-change skill integrated; upstream review/audit/debt/gain functions intentionally not duplicated | PASS — local skill | Plugin/hooks remain uninstalled; review separately only if explicitly needed |
| Behavioral evaluation harness | 49 routing cases cover all 36 primary skills; manual no-API runner exists | PARTIAL | Run the target agent in a fresh session and record actual responses/traces; runner itself does not call a model |
| GitHub Actions validation | Current branch workflow run #78 completed successfully; all 14 validation steps passed and coverage audit returned PASS with zero warnings | PASS — current revision | Re-run after any subsequent change |
| Agent/client adapters | AGENTS.md and Copilot repository instructions exist | PARTIAL | Verify Codex/VS Code and other target clients separately; repository files do not globally configure every client |
| Runtime tool/plugin installation | No evidence that Ponytail plugin/hooks or all external candidates are installed in Codex/VS Code | NOT VERIFIED | Do not install without explicit system-level authorization and hook review |

## Current implementation branch

Branch: `feat/cacd-autonomy-ponytail-engine-audit`, based on PR #4's registry revision. This branch adds two focused skills (`ponytail-engineering` and `capability-gap-closure`), maps all 36 catalog skills into 12 capability families, adds a local coverage auditor, and expands direct routing/autonomy regressions from 25 to 49 cases. The audit now targets 36/36 skill-to-family mappings and 36/36 direct primary-route evals. These additions passed structural CI in run #77 (14/14 steps). Coverage is 36/36 skills mapped to 12 families and 36/36 with direct primary-route evals; 0 unreferenced skills and 0 missing direct evals. Fresh-session behavioral tests A/B/C remain NOT RUN in the target Codex/VS Code environment.

## What "working" means

- **Structural PASS:** files, schemas, references, scripts, and CI checks are valid.
- **Behavioral PASS:** the target agent actually loads the intended instructions, routes correctly, follows the procedure, respects boundaries, and produces evidence in a fresh session.
- **Operational PASS:** required tools are actually available and the end-to-end task completes in its intended environment.
- These levels are not interchangeable. A green CI run cannot certify model behavior or production readiness.

## Required finish gates

1. Structural validation on the current branch.
2. GitHub Actions success for the current branch.
3. Fresh-session tests A/B/C in the target Codex/VS Code environment.
4. Focused routing cases for capability discovery and minimal-change engineering.
5. Explicit verification of tool availability before any future plugin or system integration.
6. Review of the resulting diff; no merge or deployment is implied.

## Non-goal

No system can guarantee 100% success on every future project. The engineering target is high, measurable coverage: detect missing capability early, select the right tool/skill, verify actual behavior, expose unknowns, and stop safely at authorization boundaries.
