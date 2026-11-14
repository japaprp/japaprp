# Conselho Central — engine and subsystem status

Audit snapshot: 2026-11-14, after PR #6 run #108. Scope: the Council Central repository `japaprp/japaprp` and its agent-routing/governance machinery. This is not a health check of the separate Dark War REA, Guerra Infinita, Casa Prática, or other application runtimes.

## Executive result

The repository has a working structural catalog and CI validation, but it does not yet have a self-running agent orchestrator that guarantees skill loading, autonomous external discovery, or 100% task success. The main unfinished area is behavioral execution in the target agent/client, not missing documentation.

| Engine / subsystem | Verified state | Status | Remaining work |
|---|---|---|---|
| Skill catalog and metadata validator | 37 unique skill names and 50 routing cases validated by PR #6 CI run #108 | PASS — structural | Re-run after subsequent code/dataset changes |
| Project registry | 19 projects validated with cross-references against 17 repository records by PR #6 CI run #108 | PASS — structural | Re-verify each project's live repository before project-specific operations |
| Capability registry | 13 capability families; all 37 skills referenced and directly evaluated, with zero missing or unreferenced skills in PR #6 CI run #108 | PASS — structural | Re-run after registry/catalog changes |
| Engineering Brain router | Routing, project isolation, skill budget, autonomy and approval boundaries documented | PARTIAL | Runtime depends on the host loading repository instructions and selected skills |
| Activation bootstrap | AGENTS.md and Copilot repository instructions contain the trigger procedure; deterministic structural test exists | PARTIAL | Fresh-session activation in each target client has not been behaviorally proven |
| Capability gap closure | Dedicated skill, router dispatch, internal-first/external GitHub discovery contract, isolated closure procedure and regression coverage exist | PASS — structural; PARTIAL — behavior | Prove the target agent actually discovers, compares and closes a gap in a fresh session |
| Ponytail engineering principles | Selective local minimal-change skill integrated; upstream review/audit/debt/gain functions intentionally not duplicated | PASS — local skill | Plugin/hooks remain uninstalled; review separately only if explicitly needed |
| Multi-agent orchestration | Hierarchy, DAG planner, task validation, project isolation, exclusive resource locks and hard concurrency ceiling (10; default 5) pass deterministic tests in PR #6 CI run #108 | PASS — planner/contract structural; PARTIAL — operational | Live child-agent dispatch, real isolation, conflict handling, cancellation and recovery remain NOT RUN until a runtime adapter is verified |
| Behavioral evaluation harness | 50 routing cases cover all 37 primary skills; manual no-API runner exists | PARTIAL | Run the target agent in a fresh session and record actual responses/traces; runner itself does not call a model |
| GitHub Actions validation | PR #5 run #79 passed; PR #6 run #108 completed successfully with all 16 named job steps passing, including registry validation, coverage audit, capability tests, orchestration planner tests, activation and routing regressions | PASS — latest full validation of the current implementation | Re-run after subsequent code/test changes |
| Open-source readiness | Research and gap matrix added at `skills/tests/OPEN_SOURCE_READINESS_AND_GAP_MATRIX.md` | PASS — planning artifact | Product repository strategy, license, distribution, public quickstart and community policies remain decisions/work items |
| Agent/client adapters | AGENTS.md and Copilot repository instructions exist | PARTIAL | Verify Codex/VS Code and other target clients separately; repository files do not globally configure every client |
| Runtime tool/plugin installation | No evidence that Ponytail plugin/hooks or all external candidates are installed in Codex/VS Code | NOT VERIFIED | Do not install without explicit system-level authorization and hook review |

## Current implementation branch

Branch stack: PR #5 `feat/cacd-autonomy-ponytail-engine-audit` → PR #6 `feat/central-portfolio-registry-20261114`. PR #6 extends the portfolio to 19 project records and 17 repository inventory rows, adds the `agent-orchestration` skill and its contract, maps all 37 catalog skills into 13 capability families, and expands direct routing/autonomy regressions to 50 cases. PR #6 CI run #108 (`43562347040`) completed successfully with all 16 named job steps passing after the open-source readiness matrix was added. The earlier PR #6 run #80 validator SyntaxError was corrected before run #95. An intermediate run #96 failed because a test expected outdated error wording; the assertion was corrected, and runs #97–#108 passed. The planner enforces a default concurrency of 5 and a hard ceiling of 10. Fresh-session behavioral tests A/B/C and multi-agent runtime tests D1–D3 remain NOT RUN in the target Codex/VS Code environment.

The new open-source readiness matrix is a planning document, not a claim that the project is already packaged, licensed, ready for external contributions, or operating a live multi-agent runtime.

## What "working" means

- **Structural PASS:** files, schemas, references, scripts, and CI checks are valid.
- **Behavioral PASS:** the target agent actually loads the intended instructions, routes correctly, follows the procedure, respects boundaries, and produces evidence in a fresh session.
- **Operational PASS:** required tools are actually available and the end-to-end task completes in its intended environment.
- These levels are not interchangeable. A green CI run cannot certify model behavior or production readiness.

## Required finish gates

1. Structural validation on the current branch.
2. GitHub Actions success for the current branch.
3. Fresh-session tests A/B/C in the target Codex/VS Code environment.
4. Multi-agent runtime tests D1–D3 from `skills/tests/AGENT_ORCHESTRATION_RUNTIME_TEST.md`, including real child-agent dispatch, locks, QA and approval gates.
5. Focused routing cases for capability discovery and minimal-change engineering.
6. Explicit verification of tool availability before any future plugin or system integration.
7. Review of the resulting diff; no merge or deployment is implied.
8. Verify real runtime dispatch with at least two independent tasks, resource isolation, QA, cancellation/recovery and authorization gates before marking orchestration operational.
9. Complete the public-product decisions and onboarding gates in `skills/tests/OPEN_SOURCE_READINESS_AND_GAP_MATRIX.md` before claiming the repository is ready for external adoption.

## Non-goal

No system can guarantee 100% success on every future project. The engineering target is high, measurable coverage: detect missing capability early, select the right tool/skill, verify actual behavior, expose unknowns, and stop safely at authorization boundaries.
