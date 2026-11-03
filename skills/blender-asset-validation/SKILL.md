---
name: blender-asset-validation
description: Inspect and compare 3D game assets in Blender, including OBJ/FBX imports and exports, geometry metrics, materials, UVs, transforms, bounds and fresh-process round-trip validation. Use when a model must be checked independently before reuse.
---

# Blender Asset Validation

## Purpose

Verify that a 3D asset is structurally readable and that important geometry and visual properties survive import/export. This is a validation workflow, not a modeling or repair workflow. Preserve the original files and use new output paths for every conversion.

## 1. Confirm the environment

1. Identify the exact Blender executable and version before running scripts.
2. On Windows, check Get-Command blender and known installation locations; do not assume Blender is on PATH.
3. If Python is not installed system-wide, prefer Blender's bundled Python through Blender's own --python execution. Do not require a separate Python installation unless a specific tool truly needs it.
4. Record Blender version, executable path, operating system, source file paths, sizes, and SHA-256 hashes.
5. If Blender is unavailable, stop and report BLOCKED rather than installing it without authorization.

## 2. Establish a baseline

For each OBJ/FBX input, inspect and record:

- Objects, mesh objects, vertices, edges, polygons, and evaluated triangles.
- Object names, hierarchy, transforms, dimensions, and world-space bounds.
- Material slots and actual material assignments.
- UV layers and UV coordinate presence.
- Image textures and external texture paths.
- Normals and smoothing/split-normal information where supported.
- Armatures, bones, actions, animation clips, and frame ranges when applicable.
- Import warnings, missing resources, invalid coordinates, degenerate faces, and loose geometry.

Do not apply 3D-printing rules blindly to game meshes. Open boundaries, disconnected pieces, duplicate vertices, and non-manifold edges may be intentional depending on the asset.

## 3. Perform a controlled round trip

1. Import the source into a clean Blender scene using the importer appropriate to the installed Blender version.
2. Capture baseline metrics and a visual inspection view before exporting.
3. Export to a new staging path. Do not overwrite the source or an earlier candidate.
4. Start a fresh Blender process with a clean scene and import the exported file again.
5. Capture the same metrics and equivalent views from the re-imported result.
6. Compare source and re-imported results using explicit invariants rather than demanding identical raw counts in every format.

Useful invariants include required object names, object/mesh counts, expected vertex/face ranges, dimensions, world bounds, material assignments, UV presence, texture links, armature hierarchy, and critical animation frames.

## 4. Interpret differences correctly

- OBJ and FBX may represent vertex sharing, normals, transforms, materials, axes, units, and animation differently.
- A changed vertex count is not automatically corruption; exporters may split vertices at UV seams or normals.
- A changed coordinate basis may be an axis-conversion setting rather than lost geometry.
- Missing material appearance may be a missing external texture path or unsupported shader translation, not missing mesh geometry.
- Compare bounding boxes and transforms in a common coordinate basis and unit scale.
- Distinguish source-authored values from evaluated values after modifiers.
- Never claim visual fidelity from counts alone. Open the actual render or viewport evidence.

If an invariant fails, preserve both files, inspect the smallest affected object/material/texture, and repeat only the focused check. Do not repair the source automatically during a validation task.

## 5. PowerShell execution pattern

Use Blender's background mode when the exact executable and script are known:

> $Blender = (Get-Command blender -ErrorAction SilentlyContinue).Source
> if (-not $Blender) { throw "Blender executable not found; resolve the installed path first." }
> & $Blender --version
> & $Blender --background --factory-startup --python .\\inspect_asset.py -- --input .\\staging\\Generator_Lv1.obj --output .\\staging\\obj_metrics.json

The script must use Blender's bundled bpy API, write JSON to an explicit new output path, return a non-zero exit code on an invalid input or failed required invariant, and never save over the source. Inspect the script before executing it. If background execution is unavailable, use the Blender UI Text Editor and preserve the same clean-scene, output-path, and evidence requirements.

Importer/exporter operator names and options vary by Blender version. Inspect the installed version's operators or use its UI importer/exporter; do not blindly reuse flags from another Blender release.

## 6. Evidence and result classification

For each required invariant, report:

- Source value.
- Re-imported value.
- Difference and tolerance.
- Evidence file or screenshot.
- Status: PASS, FAIL, BLOCKED, or NOT RUN.

Also record source/output SHA-256, Blender version, command, return code, warnings, and any checks omitted. A successful process exit is not sufficient if required invariants were not compared.

## Completion checklist

- [ ] Exact Blender executable and version recorded.
- [ ] Source hashes recorded and originals preserved.
- [ ] Baseline geometry/material/UV/hierarchy metrics captured.
- [ ] Export written to a new path.
- [ ] Fresh-process re-import performed.
- [ ] Differences interpreted with format-specific tolerances.
- [ ] Visual evidence inspected when visual fidelity matters.
- [ ] Every validation classified PASS, FAIL, BLOCKED, or NOT RUN.

## Primary reference

- Blender Agent Studio asset-validation workflow (method reference): https://github.com/ifBars/blender-agent-studio/tree/main/plugins/blender-agent-studio/skills/blender-asset-validation
- Blender Python API: https://docs.blender.org/api/current/
