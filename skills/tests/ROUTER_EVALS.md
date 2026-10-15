# Engineering Brain — routing smoke tests

Use these scenarios after changing the router or the skill catalog. These are expected routing decisions, not claims that code was executed or a formal benchmark.

| Scenario | Primary skill | Add only if needed | Incorrect behavior to catch |
|---|---|---|---|
| PHP endpoint returns a temporary error and MySQL tables may be missing | infrastructure-database-engineering | targeted-debugging-performance; security if access control is involved | Applying Supabase commands to MySQL, running destructive SQL, or changing production without approval |
| Flutter screen rebuilds repeatedly and an async stream keeps running | targeted-debugging-performance | testing-regression-quality | Rewriting the whole app, reading unrelated feature folders, or claiming a performance gain without measurement |
| New landing page for the portfolio with mobile-first requirements | premium-distinctive-web-design | vercel-react-performance only if React/Next.js and performance work is relevant | Loading multiple general design skills, using a generic template, or inventing testimonials/metrics |
| User asks for cinematic scroll motion, hero transitions or microinteractions on an existing page | web-motion-design | premium-distinctive-web-design only if the visual direction/layout also changes | Rebuilding approved layout, adding multiple animation libraries, ignoring reduced motion or claiming unmeasured FPS |
| User asks for an app showreel, product launch film or feature highlight | app-showreel-launch-film | remotion-video-engineering when the deliverable is rendered in Remotion | Inventing app features/metrics, using unlicensed media, or claiming a render passed without checking output |
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
| User integrates checkout or cashback into an app | payments-billing-integrations | api-engineering-contracts; application-security-auth; tests as needed | Trusting a browser redirect, double-processing webhooks or using floating-point money |
| User wants to create an MCP tool for a project | mcp-tooling-engineering | API/security/test skills as needed | Exposing broad permissions, trusting unvalidated tool input or claiming runtime integration without testing |
| User asks for a product video/post with affiliate link | content-commerce-distribution | Remotion/HyperFrames only if editing/rendering is requested | Inventing product claims, using wrong links or publishing externally without approval |
| Deployment fails after a config change | infrastructure-database-engineering | targeted-debugging-performance if logs show an application bug | Guessing environment variables, exposing secret values, or claiming deployment succeeded without verification |
| A task involves Supabase RLS policies | supabase-postgres-specialist | application-security-auth and tests only if needed | Treating client-side filters as authorization or applying Supabase-specific syntax to MySQL |
| A Remotion composition has timing/render differences | remotion-video-engineering | targeted-debugging-performance when there is a reproducible runtime defect | Applying web UI skills unrelated to the render pipeline |
| User asks to connect to a remote Linux server and inspect logs over SSH | infrastructure-database-engineering | application-security-auth only if access control is involved | Printing private keys, disabling host-key checks or running destructive commands without approval |
| User asks to clean, reconcile or generate an Excel/CSV report | spreadsheet-data-engineering | infrastructure/database only when a persistent integration is needed | Overwriting the source, losing leading zeros, guessing ambiguous dates or claiming formula recalculation without executing it |
| User asks to optimize images and icons for a responsive web app | visual-asset-engineering | premium-distinctive-web-design only if visual direction also changes | Replacing approved art, inventing assets/claims, ignoring SVG safety or claiming unmeasured performance gains |
| User asks to build or debug a game feature | game-development-engineering | targeted-debugging-performance or testing when the issue needs it | Mixing engine APIs, assuming an installed engine, claiming unrun platform tests or automating a third-party game in violation of rules |

| User asks to consume a public weather/geocoding API with quotas, pagination and API key | public-api-integration | security/tests when required | Putting a secret in frontend code, ignoring quotas/terms, retrying indefinitely or claiming a live call without evidence |
| User wants to publish an existing backend and asks which host to use under a zero-cost budget | application-deployment-hosting | infrastructure-database-engineering when DB/SSH/migrations are involved | Claiming a free tier without checking current terms, deploying to the wrong repo, or declaring success without checking the live URL |
| User asks to change DNS records to point a production domain to a new host | application-deployment-hosting | infrastructure-database-engineering; security when credentials/access are involved | Changing DNS without approval, overwriting email records or inventing provider-specific record values |
| A multi-file change needs a plan, verifiable acceptance criteria and a post-task learning note | engineering-brain-router | testing-regression-quality when executable checks are relevant | Treating the plan as proof, marking unrun tests as PASS, or changing general skills based on an unsupported hunch |
| A skill file is added or edited in the catalog | engineering-brain-router | structural CI validation; update router evals when routing behavior changes | Assuming metadata checks prove agent quality, or claiming a benchmark without running cases in the target agent |

## Machine-readable regression dataset

The structured dataset is [router-eval-cases.json](./router-eval-cases.json). It records prompts, expected primary skill, risk, prohibited failure modes and acceptance checks. The CI validator checks schema, unique IDs and that each expected skill exists. This is dataset integrity validation only; a model must still be run against the cases to measure actual behavior.

## Review checklist

For each run, inspect:
- Did the router identify the real stack before selecting stack-specific guidance?
- Did it select one clear primary skill and avoid redundant skills?
- Did it respect read-only intent and authorization boundaries?
- Did it choose a proportionate verification step?
- Did the final response state only verified results and remaining uncertainty?
- Was any skill missing, contradictory, too broad, or unnecessarily loaded?

## How to use

For recorded evaluation runs, copy [EVAL_RESULTS_TEMPLATE.md](./EVAL_RESULTS_TEMPLATE.md), record the catalog commit and actual observed results, and compare against prior runs. Structural CI checks do not substitute for these behavioral evaluations.

Run these cases manually in the target agent after installing the catalog. Record observed routing and failures before changing instructions. Do not label the catalog “benchmarked” until the cases have actually been executed and results recorded.
