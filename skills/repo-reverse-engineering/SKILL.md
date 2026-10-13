---
name: repo-reverse-engineering
description: Map an unfamiliar codebase and explain its architecture, dependencies, entry points, data flow, runtime behavior, tests, risks, and extension points. Use before major edits, when onboarding to a repository, or when comparing implementations.
---

# Evidence-Driven Repository Reverse Engineering

## Objective

Produce an accurate, navigable explanation of how a repository works before proposing changes. Prefer source-backed conclusions over guesses and keep the investigation proportional to the task.

## Workflow

### 1. Establish boundaries

- Confirm the repository root, branch, working-tree state, and requested outcome.
- Read `README*`, `AGENTS.md`, `CONTRIBUTING*`, package/build manifests, CI workflows, and local agent instructions.
- Identify generated files, vendor directories, ignored files, submodules, and large assets.
- Do not overwrite uncommitted user work. Never print secret values.

### 2. Inventory the system

Inspect directory structure and identify:

- Runtime and language versions.
- Application entry points and boot sequence.
- UI, API, domain/business logic, persistence, jobs, integrations, and infrastructure boundaries.
- Dependency injection, routing, state management, configuration, feature flags, and error handling.
- Test suites, fixtures, mocks, migrations, build scripts, and deployment definitions.

Use targeted search and inspect files in context. Avoid dumping the entire repository into the context window. Follow imports and callers from the relevant entry point.

### 3. Trace a real execution path

For the target feature, document this chain when applicable:

`trigger → entry point → validation → domain logic → data access/integration → response or rendered output → error paths`

For UI/video features, include state, props, timing, assets, frame or event lifecycle, and rendering boundaries. For backend features, include authn/authz, validation, transactions, side effects, and response contracts.

For each important claim, record the file path and symbol; include line numbers when available. Label conclusions as:

- **Observed** — directly visible in source or verified in execution.
- **Inferred** — strongly suggested by source structure but not executed.
- **Unknown** — evidence is missing or conflicting.

### 4. Validate behavior

- Find the most relevant tests and run the smallest useful test set first.
- Inspect scripts before executing them, especially install, migration, cleanup, deployment, and postinstall scripts.
- Use static checks when execution is unavailable.
- Do not claim runtime behavior was verified if only source code was read.
- Record command, result, environment constraints, and any untested paths.

### 5. Evaluate quality and risk

Review only evidence-backed issues, including:

- Broken or circular dependencies, duplicated logic, unclear boundaries, and dead code candidates.
- Input validation, authorization, secrets handling, unsafe deserialization, injection, and cross-user data isolation.
- Error handling, observability, retry behavior, concurrency, resource usage, and performance hotspots.
- Missing tests for critical behavior and mismatch between docs and implementation.

Do not label a possibility as a confirmed vulnerability without a reproducible path and impact.

### 6. Deliver the report

Use this structure:

1. **Executive summary** — purpose, confidence, and highest-impact findings.
2. **System map** — directories and responsibilities.
3. **Architecture** — components and dependency direction.
4. **Execution traces** — target feature flows with source evidence.
5. **Data and API contracts** — schemas, endpoints, events, and state.
6. **Build, test, and deployment** — exact commands and observed outcomes.
7. **Risks and gaps** — severity, evidence, impact, and remediation.
8. **Extension plan** — smallest safe changes, affected files, and acceptance criteria.
9. **Open questions** — evidence that is still needed.

## Editing rules

- Default to read-only investigation unless implementation is requested.
- Before changing files, list the planned edits and why each is necessary.
- Keep changes minimal and consistent with existing conventions.
- Preserve public APIs and existing structure unless the task explicitly calls for redesign.
- Never delete files, rewrite history, rotate production settings, or deploy without explicit scope and authorization.
- After editing, inspect the diff and run relevant checks.

## Completion checklist

- [ ] Repository instructions reviewed.
- [ ] Entry points and main dependencies identified.
- [ ] At least one relevant execution path traced.
- [ ] Facts separated from inferences.
- [ ] Tests/checks and limitations reported accurately.
- [ ] Sensitive data excluded.
- [ ] Findings tied to paths/symbols and next steps prioritized.
