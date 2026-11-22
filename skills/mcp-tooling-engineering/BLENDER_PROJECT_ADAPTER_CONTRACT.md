# Blender Project Adapter Contract

**Status:** proposed, read-only pilot contract. No Blender runtime adapter is installed or operational yet.
**Owner project:** `central-council`
**Target pilot:** Blender Android 5.3.0 on Galaxy S21 (SM-G991B, ARM64).
**Primary capability:** existing `mcp-tooling-engineering`; this document does not create a new Router or a duplicate generic MCP skill.

## 1. Purpose and boundaries

Provide durable, verifiable project continuity across devices and agents working with Blender. The adapter must identify the exact project and Blender runtime, inspect scene/assets, capture visual evidence, verify existing checkpoints, and produce a safe resume plan.

Architecture:

`Council Central Router + governance + registries`
→ `Blender Project Adapter`
→ `restricted Blender-side bridge`
→ `Blender runtime`

The existing Council Central project registry and Router remain authoritative. Blender projects are task-scoped resources, not new Council projects unless separately registered by the Owner.

## 2. Compatibility facts and unverified assumptions

Verified from the user's supplied Blender screen on 2026-11-22:
- Blender UI reports version **5.3.0**.
- The UI is running on the user's Galaxy S21 in Android.
- The visible scene is the default Camera/Cube/Light scene.

Not yet verified:
- Exact Android port build/tag, APK SHA-256, and build commit.
- Whether the add-on installation path is writable and persistent on this Android build.
- Availability of add-on dependencies (including `requests`) inside Blender's bundled Python.
- Whether a Blender-side loopback listener can be reached from Termux across Android app sandboxes.
- Whether the Android build supports the add-on's threading, timers, socket, and file APIs as expected.
- Actual `bpy.app.version_string`, `bpy.app.build_hash`, and `bpy.app.binary_path` from inside Blender.
- Any successful MCP handshake or real read-only scene query on the S21.

A desktop Blender minimum-version declaration is not evidence of Android-port compatibility. Do not mark Android support as PASS until the physical S21 pilot passes.

## 3. Required adapter operations — phase 1 is read-only

The public MCP surface for the first pilot is limited to:

1. `discover_runtime()` — Blender version/build, OS/platform, architecture, add-on bridge version, transport status, and capability flags.
2. `inspect_project()` — selected project manifest, root identity, active .blend file identity, file size, modification time, and SHA-256 where readable.
3. `inspect_scene()` — scene names, active scene, render engine/settings summary, frame range, unit settings, and object counts.
4. `inspect_object(object_id)` — stable object identity, type, transforms, collection membership, data/material references, and bounded mesh statistics.
5. `inspect_assets()` — read-only inventory of linked libraries, images, fonts, materials, caches, and missing references; never download or relink.
6. `capture_viewport()` — capture current viewport or a supported still render without saving or changing scene state.
7. `list_checkpoints()` — list only existing, explicitly registered checkpoints and their hashes.
8. `verify_checkpoint(checkpoint_id)` — verify file identity, SHA-256, Blender version/build compatibility metadata, and manifest consistency.
9. `plan_resume(project_id, checkpoint_id)` — return a proposed, non-executing resume plan with unresolved dependencies and risks.

No other Blender operation is available in phase 1.

## 4. Blender-side bridge requirements

The preferred implementation is a small, purpose-built bridge with a fixed command allowlist. It is not a general-purpose Python console.

- Do not install or expose the upstream MCP for Blender `execute_blender_code` tool as the adapter's execution path.
- Do not expose raw Python, `exec`, `eval`, arbitrary file paths, shell commands, network fetches, Blender operators with implicit context, add-on installation, or arbitrary imports.
- Every command maps to a fixed, reviewed handler that uses the Blender Data API for reads.
- Reject unknown command names, unknown fields, oversized payloads, invalid IDs, traversal paths, and cross-project references.
- Keep the listener bound to IPv4 loopback only. No LAN binding, port forwarding, public tunnel, or remote listener in the pilot.
- Authenticate each client using a per-install random secret and a challenge/response MAC; never place the secret in scene data, project files, logs, screenshots, or repository files.
- Use fresh nonces, bounded clock skew, request IDs, replay rejection, rate limits, and short connect/read timeouts.
- If the Android port cannot support this secure bridge, return BLOCKED and choose a different transport; do not silently fall back to an unauthenticated socket.
- Do not assume that Android loopback connectivity between Termux and Blender works; test it on the physical S21 before relying on it.

## 5. Gateway requirements

The MCP gateway may run in Termux on the S21 or on the Galaxy Book Go as a control console, subject to a verified transport path.

- Expose only the nine read-only operations in section 3.
- Never register a tool named `execute_blender_code` or an equivalent arbitrary-code escape hatch.
- Validate schemas at the gateway and again in the Blender-side bridge.
- Bind the gateway to stdio for the local MCP client by default; do not expose an HTTP listener unless separately reviewed and approved.
- Preserve project identity and enforce one-project-per-task context.
- Attach source hashes, runtime identity, timestamps, request IDs, and evidence references to every result.
- Treat Blender scene names, asset metadata, text blocks, file names, and external content as untrusted data, never as instructions.
- Fail closed when the bridge version, Blender build, project identity, authentication, or response schema is unknown.

## 6. Continuity manifest and checkpoint model

Every project session must record:
- stable `project_id`, repository (if any), branch and exact revision (if any);
- exact .blend file path within the authorized project root, file size, modified time, and SHA-256;
- Blender version, build hash, platform, architecture, bridge version, and adapter version;
- active scene, relevant object/asset identities, and linked external dependencies;
- decisions, verified facts, hypotheses, open risks, completed tasks, and next task;
- evidence references and hashes, not copied secrets or unrelated project data;
- checkpoint ID, source file hash, and verification result.

A checkpoint is immutable evidence. Never overwrite a checkpoint or the source .blend file automatically. Phase 1 only lists and verifies existing checkpoints and plans a resume; it does not save, duplicate, export, or mutate.

## 7. Explicitly deferred capabilities

Until phase 1 passes on the physical S21 and a separate write-safety review is approved, the adapter must reject:
- create/delete/rename objects or collections;
- transform, mesh, material, modifier, rig, animation, or node edits;
- save, Save As, overwrite, export, render-to-file, import, append, link, or asset downloads;
- Python console access, script execution, operators that mutate state, handlers, timers, drivers, or add-on registration;
- network calls from Blender, credentials, cloud synchronization, and remote control;
- checkpoint creation or restoration.

A later write phase must use task-specific grants, an isolated disposable .blend copy, explicit destination paths, no-overwrite semantics, before/after hashes, and independent QA. It is not authorized by this contract.

## 8. Security review of upstream MCP for Blender

Upstream `ahujasid/mcp-for-blender` 2.3.1 is a research reference, not an approved dependency for direct S21 installation.

Observed source and issue evidence:
- The add-on registers an `execute_code` command that calls Python `exec` in Blender.
- The socket protocol has no client authentication; loopback-only binding reduces network exposure but does not isolate local applications.
- The upstream Safe Mode validates the MCP server's code path; it is explicitly not a sandbox around the Blender socket.
- Upstream issues #404 and #406 document unauthenticated socket code execution and internal-network URL fetching.
- Upstream issue #429 reports Blender 5.3.0 exceptions that terminate the add-on socket server thread. The report is from Linux, not the Android port; treat it as a relevant regression risk, not proof of an S21 failure.

Do not patch, fork, install, or expose upstream code until a separate source audit, dependency/license review, Android compatibility check, and security regression plan are complete.

## 9. Acceptance gates

### Gate A — static/source review
- [ ] Confirm exact APK build provenance and hash.
- [ ] Review Blender Android port's bundled Python and add-on support.
- [ ] Review bridge source, dependency/license inventory, and Android filesystem constraints.
- [ ] Verify that the adapter has no arbitrary execution, writes, external network fetches, or cross-project access.

### Gate B — physical S21 read-only pilot
- [ ] Obtain Blender's in-process version/build metadata.
- [ ] Install/enable the purpose-built bridge only after the source review and user-visible confirmation of the exact file.
- [ ] Prove authenticated loopback transport from Termux to Blender, or mark that transport BLOCKED.
- [ ] Pass runtime discovery and read-only scene/object/asset inspection.
- [ ] Capture a viewport image and verify it matches the visible scene.
- [ ] Prove a rejected unknown command and invalid authentication do not change scene/file hashes.
- [ ] Repeat after closing/reopening Blender and after loading a disposable .blend.

### Gate C — continuity
- [ ] Create a test manifest for a disposable project without touching Dark War or Guerra Infinita data.
- [ ] Verify checkpoint hash and compatibility.
- [ ] Produce a resume plan without executing it.
- [ ] Transfer the manifest to a second agent/device and confirm it can identify the exact same project state.

### Gate D — independent QA
- [ ] Review traces, source hashes, project isolation, permission enforcement, and all failure cases.
- [ ] Record PASS/FAIL/BLOCKED/NOT RUN per gate.
- [ ] Keep all write operations disabled until separately authorized.

The adapter is **not operational** until Gates A–D pass. Documentation tests prove contract structure only; they do not prove runtime compatibility.

## 10. Current decision

**Decision:** proceed with a custom, read-only Blender Project Adapter contract and compatibility pilot. Keep upstream MCP for Blender as a research reference only. Do not install the upstream add-on or execute code inside Blender yet.

**Current state:** Android Blender 5.3.0 is visually confirmed; all in-process runtime, bridge, transport, checkpoint, and cross-agent acceptance tests remain NOT RUN.
