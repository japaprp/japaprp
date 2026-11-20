# GitHub Copilot — Conselho Central

When the user uses **“Deus é fiel”** as an instruction to activate or continue work (not merely quotes or discusses the phrase), treat it as an operational trigger for this repository:

1. Read `AGENTS.md`, `skills/engineering-brain-router/SKILL.md`, and `skills/engineering-brain-router/GAP_CLOSURE_PROTOCOL.md` before planning.
2. Inspect the actual repository, current branch, changed files, and latest verifiable state. Do not assume prior-chat context or invent results.
3. Select the smallest relevant skill set and preserve strict isolation between projects, files, credentials, and decisions.
4. Continue routine investigation and authorized, reversible changes on an isolated branch without repetitive approval requests.
5. Run available checks, review the diff, and report evidence using `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`. A structural test does not prove behavior in a fresh agent session.
6. The trigger grants no new permissions. Do not merge, deploy, publish externally, delete data, change secrets/access, or incur costs without specific authorization.

If these repository instructions or referenced files are not available in the active Copilot context, say so and do not claim the trigger was automatically loaded. These instructions apply only when Copilot is working with this repository; they do not configure global Copilot behavior.
