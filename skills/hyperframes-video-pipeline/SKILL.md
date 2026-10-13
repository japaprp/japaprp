---
name: hyperframes-video-pipeline
description: Build, inspect, debug, and validate HyperFrames compositions and HTML-to-video pipelines. Use for HTML/CSS/JavaScript scenes, seekable animations, synchronization, Puppeteer capture, FFmpeg encoding, audio mixing, or rendering reliability.
---

# HyperFrames Video Pipeline

## Objective

Trace a composition from web markup and time-based animation through browser capture and media encoding. Use the repository's installed HyperFrames version and verify current commands from its own CLI/help and documentation.

## Repository reconnaissance

- Read `README`, `AGENTS.md`, package manifests, lockfiles, examples, and the relevant package documentation.
- Identify the CLI and packages actually used. The upstream project may separate core parsing/runtime, capture engine, producer pipeline, studio, player, transitions, and cloud integrations; confirm which exist in the checked-out version.
- Find composition manifests, scene markup, styles, animation code, media assets, audio tracks, rendering scripts, and test fixtures.
- Check whether the repository uses Git LFS before cloning or testing media-heavy fixtures. Do not download large test artifacts unnecessarily.

## Trace the pipeline

Document the concrete path:

`composition/config → scene and asset resolution → time/seek control → browser/page initialization → capture frames/audio → FFmpeg encode/mix → output validation`

At each boundary, record inputs, outputs, errors, and ownership of timing. Distinguish the project’s documented architecture from the exact implementation found in source.

## Time and animation correctness

- Identify the canonical time unit and conversion to frame indices.
- Verify that animations can seek directly to any requested timestamp rather than relying on previous frames or wall-clock playback.
- Avoid unseeded randomness, live network data, and stateful animations that make the same timestamp render differently.
- Test scene start/end boundaries, overlapping layers, transitions, pauses, and missing media.
- Check CSS animations, Web Animations API, canvas/WebGL, video elements, and custom animation libraries for deterministic seeking.
- Keep audio timing, sample rate, offsets, fades, and video frame rate consistent.

## Rendering and media debugging

For capture/encoding failures, inspect:

- Browser launch arguments, page readiness, fonts, image decoding, and network dependencies.
- Viewport size, device scale factor, browser version, and GPU/WebGL assumptions.
- Seek protocol and frame scheduling; do not assume a screenshot after a sleep means the target frame is ready.
- FFmpeg executable/version, codecs, pixel formats, stream mapping, frame rate, duration, and audio mix.
- Temporary directories, process cleanup, concurrency limits, memory, and disk usage.
- Differences between preview, local render, and hosted/distributed render environments.

Reproduce with the smallest scene and shortest output that exposes the issue. Preserve logs and exact commands, and never delete user output or temporary data without checking what owns it.

## Implementation procedure

1. Define output dimensions, FPS, duration, scene timeline, and audio requirements.
2. Create or isolate a minimal reproducible composition.
3. Ensure every animated element is seekable and stable at a fixed timestamp.
4. Run the project's lint/validation command if available.
5. Render a short clip; inspect representative frames and audio sync.
6. Render the full output only after the short render passes.
7. Verify the resulting file exists and inspect its streams/duration with available media tools.

Use CLI flags supported by the installed version; check `--help` rather than inventing flags.

## Quality gates

- Same inputs and timestamp produce the same visual state.
- No missing assets, console errors, or unhandled promises in the capture path.
- Video dimensions, FPS, and duration match the specification.
- Audio is present when expected and synchronized with the timeline.
- Scene transitions and first/last frames are checked.
- Failure paths clean up child processes and temporary resources safely.
- Tests or manual checks are recorded with actual outcomes.

## Deliverables

Produce a scene/timeline map, pipeline diagram in text, identified source files, reproducible commands, evidence-backed diagnosis, test/render results, and a minimal remediation plan. Label unexecuted steps as unverified.

## Scope and safety

Use only authorized assets and applications. Avoid committing generated MP4s, large fixtures, local caches, or secrets unless the repository explicitly requires them. Respect project licensing and attribution.
