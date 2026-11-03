---
name: unity-il2cpp-analysis
description: Analyze authorized Unity Android/iOS game artifacts built with IL2CPP or Mono. Use when APK/IPA files contain libil2cpp.so, global-metadata.dat, Assembly-CSharp.dll, ELF ARM64 code, or require mapping managed metadata to native functions and Ghidra evidence.
---

# Unity IL2CPP Analysis

## Purpose and boundaries

Recover a defensible map from Unity-managed types and methods to native code in an authorized Unity application. This skill is static-first and evidence-driven. It complements rea-assisted-analysis; it does not replace general repository analysis.

Analyze only software the user owns or is explicitly authorized to inspect. Do not develop cheats, bypass anti-cheat, evade licensing, defeat access controls, dump protected runtime memory, or interfere with live multiplayer services. If a required artifact is protected or unavailable, document the blocker rather than bypassing it.

## 1. Establish target identity

1. Record the exact APK/IPA path, package identifier, version/build, acquisition context, file size, SHA-256, and analysis date.
2. Work from a verified copy in a project-specific staging directory. Preserve the original and never overwrite it.
3. Inventory archive entries before extraction. Confirm whether the build is Unity and whether it is Mono or IL2CPP.
4. Record CPU architecture and ABI. For Android ARM64, verify the actual ELF architecture rather than assuming it from the device model.
5. Identify the Unity version from reliable metadata or binary evidence. Label uncertain version guesses as hypotheses.

Useful Unity indicators include libil2cpp.so, global-metadata.dat, UnityPlayer.so, assets/bin/Data/, and managed assemblies. Their presence/absence must be recorded, not inferred from a single filename.

## 2. Select the analysis path

| Evidence | Likely build | First analysis |
|---|---|---|
| Assembly-CSharp.dll and Mono runtime libraries | Mono | Inspect managed assemblies with ILSpy/dnSpy-compatible tooling |
| libil2cpp.so plus global-metadata.dat | IL2CPP | Pair the exact binary and metadata, then use Il2CppDumper or Cpp2IL |
| libil2cpp.so without usable metadata | Incomplete/protected/variant | Record the missing or invalid input and stop at the evidence boundary |
| Native ELF without Unity metadata | Native or incomplete Unity capture | Use native ELF/ARM64 analysis; do not assume IL2CPP |

Do not pair artifacts from different APK versions, architectures, or acquisition sessions. Hash both inputs before analysis.

## 3. Recover the managed metadata map

For an authorized, unprotected IL2CPP pair:

1. Start with the maintained Il2CppDumper release or Cpp2IL, checking their current supported Unity/metadata versions.
2. Preserve tool version, command, stdout/stderr, exit status, and output hashes.
3. Inventory generated outputs. Common useful outputs include recovered type/method declarations, dummy managed assemblies, string literals, headers, and Ghidra/IDA symbol scripts.
4. Compare a second parser when the first result is incomplete or version-sensitive. Agreement increases confidence but is not proof by itself.
5. Never force an unsupported parser version merely to obtain output. Record the version mismatch and the exact failure.

Treat recovered declarations as metadata-derived representations, not original C# source. Names, signatures, generics, inlining, virtual dispatch, and generated wrappers may be incomplete or transformed.

## 4. Map declarations to native ARM64 code

1. Confirm ELF class, endianness, machine architecture, load segments, and build identity.
2. Import the exact libil2cpp.so into Ghidra or another verified disassembler.
3. Apply symbol/type scripts only when generated from the matching binary/metadata pair.
4. Verify a small sample of mappings manually: method name, RVA/offset, containing function boundary, call references, and nearby strings or metadata.
5. Distinguish file offset, ELF virtual address, RVA, and runtime address. Do not add a module base to an address unless its address type is known.
6. Trace callers/callees and data references with bounded queries. Record the searched range and unresolved references.
7. When code is stripped, optimized, inlined, or generated, state that limitation rather than fabricating a one-to-one managed/native mapping.

## 5. Evidence and reporting

Maintain an evidence table with:

- Artifact path, byte size, SHA-256, architecture, version, and source identity.
- Tool name/version, exact command, exit status, and output hash.
- Managed type/method name, recovered token/signature, native RVA/offset, and Ghidra function identity.
- Supporting xrefs/callers/callees, strings, data references, and exact output locations.
- Coverage: complete, partial, failed, or unknown.
- Claim class: OBSERVED, DERIVED, INFERRED, or UNKNOWN.

A recovered symbol name alone does not prove the function's runtime behavior. A decompiler's pseudocode is an interpretation of machine code, not original source.

## 6. Safe stopping conditions

Stop and report BLOCKED when the exact binary/metadata pair is missing, corrupted, mismatched, unsupported, or protected. Do not use memory dumping, runtime hooks, protection bypasses, anti-cheat evasion, or live-service manipulation as an automatic fallback. Request a legally obtained, matching, unprotected analysis artifact or a narrower static question.

## 7. Handoff

- Use unity-assetbundle-forensics for CABs, AssetBundles, SerializedFiles, TypeTrees, PathIDs, and PPtr dependencies.
- Use blender-asset-validation for extracted FBX/OBJ geometry and import/export round trips.
- Use rea-assisted-analysis only when a supported REA provider is actually available and the question requires its capabilities.
- Use repo-reverse-engineering for complete source repositories rather than packaged binaries.

## Completion checklist

- [ ] Target identity, architecture, version, and hashes recorded.
- [ ] Binary and metadata pair verified as belonging together.
- [ ] Tool versions and outputs preserved.
- [ ] Address types distinguished and sample mappings checked.
- [ ] Static facts separated from inferred behavior.
- [ ] Protected or unsupported paths reported as BLOCKED, not bypassed.
- [ ] No original artifact modified and no live service manipulated.

## Primary references

- Il2CppDumper: https://github.com/Perfare/Il2CppDumper
- Cpp2IL: https://github.com/SamboyCoding/Cpp2IL
- Unity IL2CPP manual: https://docs.unity3d.com/Manual/IL2CPP.html
- Ghidra: https://github.com/NationalSecurityAgency/ghidra
