---
name: remotion-video-engineering
description: Analyze, build, debug, and optimize programmatic videos with Remotion and React. Use for compositions, frame-accurate timing, props, assets, audio, rendering, Player integration, or render failures.
---

# Remotion Video Engineering

## Objective

Work with the actual Remotion version and project conventions to build reproducible videos from React components. Treat the code and render configuration as the source of truth; verify APIs against the installed version and official documentation.

## First-pass inspection

1. Read the repository's `README`, `AGENTS.md`, package manifest, lockfile, and Remotion-specific scripts.
2. Record the versions of `remotion`, `@remotion/cli`, `@remotion/renderer`, and related packages. Do not assume all packages use the same version.
3. Find the entry file, `registerRoot`, root component, `Composition` declarations, default props, and render scripts.
4. Locate assets, fonts, audio, captions, transitions, and any data-fetching or browser-only code.
5. Check the applicable Remotion license and deployment terms before recommending commercial use.

## Composition model

Trace the composition through:

`composition id → input props → component tree → frame/time calculations → visual/audio assets → renderer → encoded output`

For each composition, identify:

- Width, height, FPS, duration in frames, and derived duration in seconds.
- Props and their validation/defaults.
- Timeline intervals and boundary behavior.
- Use of `useCurrentFrame`, `useVideoConfig`, `interpolate`, `spring`, `Sequence`, `Series`, `AbsoluteFill`, and other APIs actually present.
- Fonts, images, video, audio, and remote resources.
- Determinism requirements and external dependencies.

Remember: frame counts are discrete. Check off-by-one errors, inclusive/exclusive endpoints, FPS assumptions, and rounding between seconds and frames. Avoid introducing wall-clock time or nondeterministic data into a frame-rendered composition.

## Implementation procedure

1. Define the visual result, exact duration, FPS, dimensions, and input data.
2. Build the smallest working composition using the installed API version.
3. Keep reusable visual elements in components and timeline logic explicit.
4. Make data-driven output deterministic: stable ordering, fixed inputs, controlled random seeds, and predictable asset loading.
5. Add fallback states for missing media and document required assets/environment variables without exposing secrets.
6. Preview before rendering when tooling is available; then render a short test segment before the full output.
7. Validate the output file, dimensions, duration, audio, frame boundaries, and visual consistency.

## Debugging checklist

When a render fails or differs from preview, inspect:

- Browser console and renderer logs.
- Missing assets, font loading, remote requests, CORS, and path resolution.
- Browser-only APIs executed in an incompatible environment.
- Invalid duration/FPS, props mismatch, frame math, interpolation ranges, and sequence offsets.
- Memory pressure, concurrency, image/video decoding, codec availability, and render timeout.
- Difference between Player preview and server/CLI rendering.
- Version mismatch between Remotion packages.

Change one likely cause at a time and preserve the failing command and error output.

## Testing and performance

- Test pure timing/math functions separately from visual components.
- Add regression coverage for timeline boundaries and variable props.
- Use low-resolution/short-duration renders for rapid iteration, then verify final settings.
- Optimize large images/video, repeated expensive computations, and concurrency only after measuring.
- Do not remove visual effects or lower quality silently to make rendering faster.

## Deliverables

For an analysis task, report:

1. Composition inventory and entry points.
2. Timeline/frame map.
3. Data and asset dependencies.
4. Reproduction steps and exact checks executed.
5. Root cause with evidence, or ranked hypotheses if unverified.
6. Minimal patch plan and regression tests.

For an implementation task, include changed files, relevant commands, render/test outcome, output path only if verified, and remaining limitations.

## Safety and scope

Only fetch or process media the user is authorized to use. Do not hardcode tokens or credentials into composition props, source files, logs, or rendered overlays. Do not claim a video was rendered unless the renderer actually completed and the output was checked.
