# Conselho Central — engine and subsystem status

Audit snapshot: 2026-11-14. Scope: the Council Central repository `japaprp/japaprp` and its agent-routing/governance machinery. This is not a health check of the separate Dark War REA, Guerra Infinita, Casa Prática, or other application runtimes.

## Executive result

The repository has a working structural catalog and CI validation, but it does not yet have a self-running agent orchestrator that guarantees skill loading, autonomous external discovery, or 100% task success. The main unfinished area is behavioral execution in the target agent/client, not missing documentation.

| Engine / subsystem | Verified state | Status | Remaining work |
|---|---|---|---|
| Skill catalog and metadata validator | 34 unique skills were cataloged on the parent PR branch; validator is in CI | PASS — structural | Re-run on this branch after additions; audit unreferenced/overlapping skills |
| Project registry | 6 project records, with active/planned status and evidence qualifiers | PASS — structural | Re-verify each project's live repository before project-specific operations |
| Capability registry | 8 capability families and 2 external research candidates | PASS — structural | Add coverage audit and keep candidate state/evidence current |
| Engineering Brain router | Routing, project isolation, skill budget, autonomy and approval boundaries documented | PARTIAL | Runtime depends on the host loading repository instructions and selected skills |
| Activation bootstrap | AGENTS.md and Copilot repository instructions contain the trigger procedure; deterministic structural test exists | PARTIAL | Fresh-session activation in each target client has not been behaviorally proven |
| Capability gap closure | Detailed protocol exists, but the previous flow did not guarantee the agent would search, compare, implement and verify when a gap appeared | PARTIAL — principal gap | Add a dedicated operational skill, explicit router trigger, regression cases and a local coverage audit |
| Ponytail engineering principles | Upstream 5.3.3 skill and MIT metadata inspected; existing review/audit capabilities overlap with local skills | RESEARCHED | Integrate only minimal-change implementation rules; do not install plugin/hooks by default |
| Behavioral evaluation harness | 25 routing cases and a manual no-API runner exist | PARTIAL | Run the target agent in a fresh session and record actual responses/traces; runner itself does not call a model |
| GitHub Actions validation | Parent PR #4 commit f446b4f had workflow run #69 completed successfully, all 11 validation steps passed | PASS — parent revision only | New branch must run its own CI before its changes can be called validated |
| Agent/client adapters | AGENTS.md and Copilot repository instructions exist | PARTIAL | Verify Codex/VS Code and other target clients separately; repository files do not globally configure every client |
| Runtime tool/plugin installation | No evidence that Ponytail plugin/hooks or all external candidates are installed in Codex/VS Code | NOT VERIFIED | Do not install without explicit system-level authorization and hook review |

## Current implementation branch

Branch: `feat/cacd-autonomy-ponytail-engine-audit`, based on PR #4's registry revision. This branch adds two focused skills (`ponytail-engineering` and `capability-gap-closure`), maps them to the Council's capability families, adds a local coverage auditor, and extends routing/autonomy regressions from 25 to 29 cases. These additions are implemented but remain pending this branch's own CI and behavioral verification until those checks complete.

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
