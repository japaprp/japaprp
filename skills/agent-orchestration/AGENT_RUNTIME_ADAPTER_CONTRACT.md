# Agent Runtime Adapter Contract

**Status:** runtime-neutral interface specification; no compatible child-agent runtime has been verified in this repository snapshot.

## Purpose

Connect the Council Central Router and its specialist role registry to a real host runtime without binding governance to one editor, model vendor, or operating system. This contract does not itself spawn agents.

## Required adapter operations

An adapter MUST expose these observable operations:

1. `discover_runtime()` — return runtime identity, version, host, and availability.
2. `inspect_capabilities()` — report whether independent child-agent dispatch, isolated contexts, cancellation, task status, and execution receipts are supported.
3. `dispatch_child_agent(task_envelope)` — start one real child agent and return a runtime-generated task/instance identifier. It must not return a fabricated success when dispatch is unsupported.
4. `get_task_status(task_id)` — report queued/running/completed/failed/cancelled/blocked state and timestamps.
5. `cancel_task(task_id, reason)` — request cancellation and return an observable acknowledgement; cancellation must not be assumed until status confirms it.
6. `collect_execution_receipt(task_id)` — return the original runtime receipt and tool trace reference.

## Task envelope

Every dispatch request MUST contain:

- stable `task_id` and `parent_task_id`;
- exact `project_id`, repository, branch and verified revision;
- `role_id` from `skills/registries/AGENT_ROLE_REGISTRY.json`;
- primary and supporting skill references selected by the Router;
- bounded objective, inputs, outputs and acceptance criteria;
- explicit allowed and forbidden actions;
- permission profile and resource/lock declarations;
- dependencies, timeout, retry ceiling and budget ceiling;
- independent QA assignment.

The adapter MUST reject unknown roles, cross-project context, undeclared tools, missing permission boundaries, invalid dependencies, and resource conflicts.

## Isolation and evidence

- Each independent child agent must receive a distinct runtime context identifier.
- Child agents must not receive peer drafts or outputs before the blind-work phase ends.
- Credentials and secrets are never copied into a task envelope unless a separately authorized integration explicitly requires them; the default is no secrets.
- A receipt must be runtime-generated and include task/project/role identity, runtime and agent instance IDs, context ID, timestamps, status, input/output digests, and immutable tool-trace reference.
- A coordinator-authored string, synthetic fixture, planner output, or parallel set of ordinary tool calls is not proof of child-agent dispatch.
- QA must inspect original runtime traces and independently verify project isolation, task scope, tool use and outputs.

## Failure, cancellation and retries

- Unsupported runtime capability returns `BLOCKED`, not a simulated dispatch.
- Timeouts, missing receipts, context collisions, unexpected tools, or failed cancellation stop dependent work and preserve evidence.
- Retry is allowed only for a classified transient failure, with idempotency evidence and the configured retry ceiling. No automatic retry of external or non-idempotent actions.
- Cancellation is complete only after the runtime reports a terminal cancelled state; otherwise report `BLOCKED` or `RUNNING` accurately.

## Security and authorization

The default specialist role permission profile is read-only. Any write grant must be task-specific, branch-scoped, time-bounded, and within the Owner-approved scope. The adapter cannot authorize merge, deploy, external publication, deletion, secrets/permission changes, paid resources, or cross-project access.

## Conformance gates

A runtime adapter may be called **operational** only after all are PASS:

- adapter discovery and capability inspection;
- two real independent child-agent dispatches with distinct contexts;
- task/project/role identity and tool traces verified by independent QA;
- resource-lock and write-conflict test;
- cancellation and recovery test;
- failure/timeout/retry-exhaustion tests;
- reserved-action denial test;
- no cross-project context or credential leakage.

Until then, role profiles are catalogued only and live child-agent dispatch remains **NOT RUN** or **BLOCKED**. Structural tests of this contract do not change that status.


## Canonical execution receipt shape

The runtime adapter must return these exact fields (additional runtime-specific fields are allowed):

```json
{
  "task_id": "runtime-generated-task-id",
  "project_id": "central-council",
  "role_id": "agent-evaluator",
  "runtime_id": "runtime-name-and-version",
  "agent_instance_id": "runtime-generated-agent-instance-id",
  "context_id": "runtime-generated-isolated-context-id",
  "started_at": "2026-11-15T10:00:00Z",
  "ended_at": "2026-11-15T10:01:00Z",
  "status": "completed",
  "input_digest": "sha256:...",
  "output_digest": "sha256:...",
  "tool_trace_ref": "immutable-runtime-trace-reference"
}
```

These are schema examples only. Placeholder values are not execution evidence. A receipt is accepted only when retrieved from the real runtime and independently checked against its original trace.
