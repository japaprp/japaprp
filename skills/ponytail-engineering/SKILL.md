---
name: ponytail-engineering
description: Apply minimal-change engineering to coding tasks: reuse existing code, prefer native/platform capabilities, avoid needless dependencies and abstractions, and keep tests, security, error handling, and accessibility intact.
license: MIT
---

# Ponytail Engineering — minimal complete change

## Purpose

Use this skill as an engineering decision lens when implementing, fixing, refactoring, reviewing, or choosing dependencies. The goal is the smallest change that completely satisfies the requirement—not the fewest lines at the expense of correctness.

Upstream reference: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), skill concept reviewed from release metadata version 5.3.3 on 2026-11-14. Upstream project declares MIT licensing. This local skill is a selective adaptation of its engineering principles, not a copy of its plugin, hooks, or command suite.

## Decision ladder

Stop at the first option that fully solves the requirement:

1. **Need:** Does this behavior need to exist? Do not add unrequested options or speculative flexibility.
2. **Reuse:** Is there already a helper, component, service, pattern, or capability in this repository?
3. **Native:** Can the platform or standard library solve it safely?
4. **Existing dependency:** Is a suitable dependency already installed and maintained?
5. **Minimal implementation:** If none of the above works, implement the smallest complete solution consistent with the existing architecture.

## Completeness rules

- Read the touched code and trace affected callers, tests, fixtures, configuration, exports, and data flows before editing.
- Fix root causes at the narrowest shared point; do not patch symptoms at multiple call sites.
- Preserve existing validation, error handling, authorization, data-loss protections, accessibility, and compatibility.
- Add one focused test or assert-based check for new non-trivial logic (branches, loops, parsers, money, security, or a new script).
- Prefer established repository conventions over introducing new abstractions, wrappers, options, or dependencies.
- When a deliberate shortcut has a known limit, document the limit and the condition that would justify upgrading it. Never hide a known limitation.
- Report what was not checked and the remaining risk.

## Review checklist

Before calling the work complete, verify:

- [ ] The change solves the requested behavior end-to-end.
- [ ] Existing code was reused where suitable.
- [ ] No unnecessary dependency, abstraction, configuration, or feature was added.
- [ ] Callers and adjacent contracts were checked.
- [ ] Relevant tests were added or updated and actually run.
- [ ] Security, trust-boundary validation, error handling, and accessibility were preserved.
- [ ] The diff is understandable and no unrelated files changed.

## Scope and composition

- This is a method skill, not an autonomous installer or a replacement for domain-specific skills.
- Use it as the primary skill for explicit minimal-change engineering work, or as a single complementary lens when implementation complexity or dependency selection is material.
- Do not load it alongside `code-review-minimal-change` merely to repeat the same review. Prefer the existing review skill for PR review; use this skill when the implementation approach itself needs simplification.
- It does not authorize installing the upstream plugin, running lifecycle hooks, adding dependencies, using paid APIs, or changing global agent configuration.
- The upstream review/audit/debt/gain commands overlap existing repository review, audit, and evaluation procedures; they are intentionally not duplicated here.
