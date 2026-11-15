# Conselho Central — engine and subsystem status

Audit snapshot: 2026-11-15. PR #10 latest verified HEAD `6d171e51808d87f7576a00a40e97d1acb49e35a0` passed GitHub Actions run #173 (`43734428125`) with all 22 validation/test steps successful. Scope: the Council Central repository `japaprp/japaprp` and its agent-routing/governance machinery. This is not a health check of the separate Dark War REA, Guerra Infinita, Casa Prática, or other application runtimes.

## Executive result

The repository has a working structural catalog and CI validation, including eight governed specialist role profiles. It does not yet have a verified self-running agent orchestrator that guarantees skill loading, autonomous external discovery, or 100% task success. The main unfinished area is behavioral execution in the target agent/client, not missing documentation.

| Engine / subsystem | Verified state | Status | Remaining work |
|---|---|---|---|
| Skill catalog and metadata validator | 37 unique skill names and 61 routing cases validated on PR #10 HEAD `6d171e5` by CI run #173 | PASS — structural | Re-run after subsequent code/dataset changes |
| Project registry | 19 projects validated with cross-references against 17 repository records by PR #6 CI run #108 | PASS — structural | Re-verify each project's live repository before project-specific operations |
| Capability registry | 13 capability families; all 37 skills referenced and directly covered by the 61-case dataset in the PR #10 baseline audit | PASS — structural | Re-run after registry/catalog changes |
| Engineering Brain router | Routing, project isolation, skill budget, autonomy and approval boundaries documented | PARTIAL | Runtime depends on the host loading repository instructions and selected skills |
| Activation bootstrap | AGENTS.md and Copilot repository instructions contain the trigger procedure; deterministic structural test exists | PARTIAL | Fresh-session activation in each target client has not been behaviorally proven |
| Capability gap closure | Dedicated skill, router dispatch, internal-first/external GitHub discovery contract, isolated closure procedure and regression coverage exist | PASS — structural; PARTIAL — behavior | Prove the target agent actually discovers, compares and closes a gap in a fresh session |
| Ponytail engineering principles | Selective local minimal-change skill integrated; upstream review/audit/debt/gain functions intentionally not duplicated | PASS — local skill | Plugin/hooks remain uninstalled; review separately only if explicitly needed |
| Specialist role registry | Eight ECC-inspired role profiles reuse existing skills, default to read-only, require independent QA and are explicitly catalogued rather than runtime-active; PR #10 CI run #173 validated the registry, adapter contract and eight role-specific evaluation-case definitions | PASS — structural | Eight role-specific behavioral cases are added to the manual evaluation dataset; target-client execution remains NOT RUN |
| Multi-agent orchestration | Hierarchy, DAG planner, task validation, project isolation, exclusive resource locks and hard concurrency ceiling (10; default 5) pass deterministic tests; PR #10 run #173 passes the specialist role registry and role-evaluation coverage regression | PASS — planner/contract structural; PARTIAL — operational | Live child-agent dispatch, real isolation, conflict handling, cancellation and recovery remain NOT RUN until a runtime adapter is verified |
| Behavioral evaluation harness | 61 routing cases cover the existing primary skills plus eight specialist-role selections; manual no-API runner records observed specialist roles | PARTIAL | Run the target agent in a fresh session and record actual responses/traces; runner itself does not call a model |
| GitHub Actions validation | PR #10 run #173 completed successfully on latest verified HEAD with all 22 named validation/test steps | PASS — latest completed full validation is baseline HEAD; latest-head validation pending | Re-run after subsequent code/test changes |
| Open-source readiness | Research and gap matrix added at `skills/tests/OPEN_SOURCE_READINESS_AND_GAP_MATRIX.md` | PASS — planning artifact | Product repository strategy, license, distribution, public quickstart and community policies remain decisions/work items |
| Agent/client adapters | AGENTS.md and Copilot repository instructions exist | PARTIAL | Verify Codex/VS Code and other target clients separately; repository files do not globally configure every client |
| Runtime tool/plugin installation | No evidence that Ponytail plugin/hooks or all external candidates are installed in Codex/VS Code | NOT VERIFIED | Do not install without explicit system-level authorization and hook review |

## Current implementation branch

PR #10 `feat/council-agent-role-registry` is open as Draft, stacked on PR #9 `feat/adversarial-review-governance`. Its latest verified HEAD is `6d171e51808d87f7576a00a40e97d1acb49e35a0`; GitHub Actions run #173 (`43734428125`) completed successfully with all 22 named validation/test steps. The run validates the specialist role registry and adapter contract structurally; it does not activate child agents. Eight new role-specific cases are now included in `skills/tests/router-eval-cases.json`, with the manual runner extended to record observed specialist-role selection. These cases are definitions for future behavioral evaluation, not completed evaluations.

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
