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
| CSD-02 | Compare hook scoring implementations | Diff logic and dependencies; document any behavior differences | NOT RUN |
| CSD-03 | Test equivalent hook examples | Same inputs produce explained outputs; no unsupported prediction of virality | NOT RUN |
| CSD-04 | Test Instagram-specific Reel analysis | Account median and view data are handled correctly; missing data is flagged | NOT RUN |
| CSD-05 | Test caption review in Brazilian Portuguese | Useful edits without changing verified facts, affiliate links, or brand voice | NOT RUN |
| CSD-06 | Test routing | General content routes to CSD; Instagram-specific analysis calls the optional module only when needed | NOT RUN |
| CSD-07 | Test brand separation | Casa Prática facts/instructions do not appear in Renascer output and vice versa | NOT RUN |
| CSD-08 | Review scripts/dependencies | No unsafe network activity, credential collection, unbounded scraping, or unnecessary paid dependency | NOT RUN |
| CSD-09 | Verify publishing boundary | Draft-only by default; no real account changes during tests | NOT RUN |

## Safety and scope

- Do not install the entire external package by default.
- Do not delete, overwrite, or silently replace existing skills.
- Do not access account credentials or publish, schedule, message, or change external accounts during validation.
- Do not claim tests passed unless they were actually executed and their outputs reviewed.
- Any later implementation should be a small, reviewable change with focused tests.

## Exit criteria

The consolidation is ready for implementation only after CSD-02 through CSD-08 have evidence, the minimal reusable capability is selected, and a reviewer approves the proposed diff. Until then, this document is a plan, not a claim of completed integration.
