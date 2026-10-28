# Content skills consolidation plan

Status: proposal for review. This document does not install external skills, change runtime routing, or authorize publishing.

## Goal

Reuse the existing content workflow and add only demonstrated Instagram-specific capabilities. Keep one source of truth for overlapping procedures and preserve separate brand context for each project.

## Current evidence

- `skills/content-commerce-distribution/SKILL.md` is the primary local workflow for short-form content, affiliate claims and links, cross-platform adaptation, metrics, and human approval.
- The public `Jakeschincariol/instagram-agent-skill` repository provides Instagram-specific modules, including `ig-viral`, `ig-reel`, `ig-caption`, `ig-profile`, and `ig-audit`.
- The public `Jakeschincariol/master-skills` repository provides `virality`, including hook scoring and short-form research/writing utilities.
- The virality hook-scoring implementation documents shared origin with the Instagram package. This establishes functional overlap, not byte-for-byte identity.
- Public repository presence does not establish installation or execution in any local/Codex environment.

## Proposed routing

1. Default to `content-commerce-distribution` for content planning, writing, affiliate content, platform adaptation, review, and measurement.
2. Use `virality` only when research into high-performing short-form content, hook variants, or timed scripts is specifically needed.
3. Consult Instagram-specific `ig-viral` procedures only when the task requires Instagram/Reels-specific research, especially account-relative comparisons such as views against the account median.
4. Use profile audit, caption, carousel, Reel, or Story procedures only when the requested deliverable requires that capability.
5. Do not add a second hook-scoring implementation unless tests demonstrate a meaningful, documented difference.
6. Treat publishing/scheduling as a separate integration. Prefer official Meta tools/APIs and preserve human approval unless a specific workflow is explicitly authorized.

## Brand isolation

- Casa Prática OFC: product facts, affiliate links, prices, availability, and disclosure requirements must be verified. Do not invent claims or change links.
- Instância Renascer Belvedere: use a separate voice and asset/data context; confirm events, times, institutional claims, and image permissions.
- Never share credentials, private data, unpublished assets, or brand-specific instructions between projects.

## Validation plan

Run these checks before incorporating code or installing modules:

| ID | Check | Acceptance criteria | Status |
|---|---|---|---|
| CSD-01 | Inventory current local skill and target external files | Paths and versions are recorded; installation status is not inferred from GitHub | NOT RUN |
| CSD-02 | Compare hook scoring implementations | Diff logic and dependencies; document any behavior differences | PASS — five representative hooks produced identical scoring-panel results in CI; virality adds formula/payoff analysis |
| CSD-03 | Test equivalent hook examples | Same inputs produce explained outputs; no unsupported prediction of virality | PASS — 5 paired examples; this validates score equivalence only, not predictive accuracy |
| CSD-04 | Test Instagram-specific Reel analysis | Account median and view data are handled correctly; missing data is flagged | PARTIAL — baseline mixing, missing baseline, zero baseline and output-path regressions covered by 5 unit tests; no real account dataset supplied |
| CSD-05 | Test caption review in Brazilian Portuguese | Useful edits without changing verified facts, affiliate links, or brand voice | PARTIAL — lint preserves Portuguese text, detects URL/hashtag, and warns that caption URLs are not clickable; no rewrite model is being tested |
| CSD-06 | Test routing | General content routes to CSD; Instagram-specific analysis calls the optional module only when needed | NOT RUN — routing is documented, not wired into runtime |
| CSD-07 | Test brand separation | Casa Prática facts/instructions do not appear in Renascer output and vice versa | NOT RUN — requires actual isolated brand-context fixtures/runtime |
| CSD-08 | Review scripts/dependencies | No unsafe network activity, credential collection, unbounded scraping, or unnecessary paid dependency | PARTIAL — reviewed copies of swipe/caption/hookscore are local-only by static inspection; full dependency/package audit not run |
| CSD-09 | Verify publishing boundary | Draft-only by default; no real account changes during tests | PASS for this test harness — no publishing/API/account integration is included; this does not certify any external runtime |

## Safety and scope

- Do not install the entire external package by default.
- Do not delete, overwrite, or silently replace existing skills.
- Do not access account credentials or publish, schedule, message, or change external accounts during validation.
- Do not claim tests passed unless they were actually executed and their outputs reviewed.
- Any later implementation should be a small, reviewable change with focused tests.

## Exit criteria

The consolidation is ready for implementation only after CSD-02 through CSD-08 have evidence, the minimal reusable capability is selected, and a reviewer approves the proposed diff. Until then, this document is a plan, not a claim of completed integration.


## Regression run evidence (2026-10-28)

- Added isolated, MIT-attributed review copies under `tools/instagram-review/`; upstream license text is retained in `tools/instagram-review/LICENSE-MIT.txt`.
- Corrected baseline consistency: when any Reel has a median baseline, rows without a median are left unranked instead of silently switching to follower count.
- Corrected output path handling: `--out swipe.md` no longer attempts to create an empty parent directory; file writes use a context manager.
- Added 8 unit tests for mixed/missing/zero baselines, output paths, Portuguese caption parsing/link handling, and hook-score equivalence.
- GitHub Actions run #13: **SUCCESS**; job `swipe-regression` completed successfully for commit `50696611c77a13e96c0821ed0d230e95077597cb`, including the regression test using a bare relative output filename.
- This is a successful isolated regression run, not a full integration, runtime routing test, live Instagram test, or brand-isolation proof.


## Routing, brand isolation, and dependency audit follow-up (2026-10-28)

- Added `tools/instagram-review/routing.py`: deterministic intent/platform routing keeps `content-commerce-distribution` primary and adds Instagram-specific modules only for matching requests. Publishing-related intents remain draft/review-only.
- Added `tools/instagram-review/brand_context.py`: explicit allowlisted brand IDs for Casa Prática OFC and Instância Renascer Belvedere; missing/unknown brand IDs fail closed rather than guessing.
- Added `tools/instagram-review/dependency_audit.py`: AST-based import allowlist plus a small risky-operation token scan for the isolated review copies.
- Added tests for general-content routing, Instagram caption routing, Reel benchmark routing, publishing boundary, unknown-brand rejection, non-overlapping brand contexts, immutable canonical profile behavior, and a clean static dependency audit.
- GitHub Actions push run #24: **SUCCESS**, job `swipe-regression`, commit `eef59f5f2128daa6528b1cc7dfb25579a737fb89`.
- Scope limitation: these are tested helper modules and test fixtures, not yet wired into a production/runtime router or a full content-generation agent. Brand isolation test verifies the selector contract, not every downstream model prompt or external app.
- Dependency result: the reviewed Python copies use only allowlisted Python standard-library imports; the static scan found no disallowed imports or flagged operation tokens. This is not a complete software supply-chain audit of the full upstream repositories, their Claude skill instructions, or future versions.
- No external packages were installed. No Instagram accounts, tokens, API, posting, scheduling, or messaging were accessed.


## Follow-up: canonical routing, synthetic brand isolation, dependency inventory (2026-10-28)

### Canonical routing
- Added Instagram/content selection rules to `skills/engineering-brain-router/SKILL.md`, which is the single source of truth.
- `tools/instagram-review/routing.py` remains a deterministic regression oracle only; it is not represented as wired into a production runtime.
- The workflow trigger now includes changes to the canonical router and this evidence document.

### Synthetic end-to-end isolation
- Extended `brand_context.py` with `build_brand_payload`, which rejects fields outside the allowlist for the explicitly selected brand.
- Added synthetic payload tests for Casa Prática OFC and Instância Renascer Belvedere, cross-brand field injection rejection, unknown-brand rejection, and non-mutation of canonical profiles.
- These tests validate the local payload boundary; they do not prove isolation in every future prompt, conversation history, or external integration.

### Dependency and license review
- Added `source-inventory.json` pinning exact Git blob SHAs for reviewed source copies, local copy paths, and their license files.
- Preserved MIT license text for both upstream repositories in separate files.
- Recursive Git tree inspection found no repository-root `package.json`, `pyproject.toml`, `requirements*.txt`, `Pipfile*`, `poetry.lock`, or `uv.lock` in this branch. The added review copies require only Python standard-library imports; no third-party package was installed.
- Static AST/import and risky-token scan is intentionally scoped to `tools/instagram-review/*.py`. This is not a complete SCA/CVE scan, does not audit every upstream skill instruction/script, and is not a security sandbox.
- Source version pinning uses immutable blob SHAs rather than upstream release tags/full repository commit SHAs; this is explicit in the inventory.

### CI and review status
- Regression suite expanded to 20 tests across hook score equivalence, Reel baselines/output paths, Portuguese caption checks, canonical routing documentation, synthetic brand isolation, license files and source inventory.
- Final workflow for the latest code commit must finish successfully before this PR can be considered test-verified. A successful earlier run is not substituted for a run on the final HEAD.
- PR remains draft/open; no merge, deployment, account connection, scheduling, or publication was performed.
