# Engineering Brain — routing smoke tests

Use these scenarios after changing the router or the skill catalog. These are expected routing decisions, not claims that code was executed or a formal benchmark.

| Scenario | Primary skill | Add only if needed | Incorrect behavior to catch |
|---|---|---|---|
| PHP endpoint returns a temporary error and MySQL tables may be missing | infrastructure-database-engineering | targeted-debugging-performance; security if access control is involved | Applying Supabase commands to MySQL, running destructive SQL, or changing production without approval |
| Flutter screen rebuilds repeatedly and an async stream keeps running | targeted-debugging-performance | testing-regression-quality | Rewriting the whole app, reading unrelated feature folders, or claiming a performance gain without measurement |
| New landing page for the portfolio with mobile-first requirements | premium-distinctive-web-design | vercel-react-performance only if React/Next.js and performance work is relevant | Loading multiple general design skills, using a generic template, or inventing testimonials/metrics |
| A user can access another user's reservation by changing an ID | application-security-auth | testing-regression-quality; forms-crud-data-integrity if persistence rules matter | Fixing only the hidden UI button instead of server authorization and tenant isolation |
| CRUD creates duplicate records after a retry or double-click | forms-crud-data-integrity | application-security-auth if private records/permissions are involved; testing-regression-quality for a regression test | Relying only on frontend validation without server/database invariants |
| User asks for a simple label or text correction in one file | No skill or one directly relevant skill | None by default | Loading the whole catalog or producing a long investigation report |
| User asks to inspect a repository and explain architecture without edits | repo-reverse-engineering | security only if the requested flow warrants it | Editing files during a read-only audit |
| User asks for a review of a PR/diff and only necessary fixes | code-review-minimal-change | testing/security only if findings or risk require them | Rewriting unrelated files, reporting style preferences as bugs, or making unsupported claims |
| User asks whether a web UI is ready to ship | premium-distinctive-web-design | testing-regression-quality when behavior needs proof | Approving based on aesthetics alone, treating a screenshot as proof of persistence, or calling untested scope PASS |
| User requests a new public API or webhook integration | api-engineering-contracts | application-security-auth; testing-regression-quality when behavior/compatibility needs proof | Breaking existing contracts, retrying non-idempotent operations unsafely, or trusting unsigned webhooks |
| User asks for a Flutter screen/feature | mobile-flutter-engineering | API/security/tests only when the flow requires them | Introducing a new architecture without inspecting the project or claiming device tests that were not run |
| User wants an AI API feature | ai-integration-evaluation | api-engineering-contracts; ai-token-budget when context/cost matters | Exposing API keys, shipping without eval cases, or treating model output as trusted instructions |
| User has a broad app idea and asks what to build first | product-discovery-delivery | design or API skills only after scope is clear | Building a large feature list without a user problem, MVP boundary or acceptance criteria |
| Deployment fails after a config change | infrastructure-database-engineering | targeted-debugging-performance if logs show an application bug | Guessing environment variables, exposing secret values, or claiming deployment succeeded without verification |
| A task involves Supabase RLS policies | supabase-postgres-specialist | application-security-auth and tests only if needed | Treating client-side filters as authorization or applying Supabase-specific syntax to MySQL |
| A Remotion composition has timing/render differences | remotion-video-engineering | targeted-debugging-performance when there is a reproducible runtime defect | Applying web UI skills unrelated to the render pipeline |

## Review checklist

For each run, inspect:
- Did the router identify the real stack before selecting stack-specific guidance?
- Did it select one clear primary skill and avoid redundant skills?
- Did it respect read-only intent and authorization boundaries?
- Did it choose a proportionate verification step?
- Did the final response state only verified results and remaining uncertainty?
- Was any skill missing, contradictory, too broad, or unnecessarily loaded?

## How to use

Run these cases manually in the target agent after installing the catalog. Record observed routing and failures before changing instructions. Do not label the catalog “benchmarked” until the cases have actually been executed and results recorded.
