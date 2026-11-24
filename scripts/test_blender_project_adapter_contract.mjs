import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(root, path), 'utf8');
const contract = read('skills/mcp-tooling-engineering/BLENDER_PROJECT_ADAPTER_CONTRACT.md');
const skill = read('skills/mcp-tooling-engineering/SKILL.md');

assert.match(contract, /Status:\*\* proposed, read-only pilot contract/i);
assert.match(contract, /Owner project:\*\* `central-council`/);
assert.match(contract, /Blender Android 5\.3\.0 on Galaxy S21/);
for (const operation of [
  'discover_runtime()', 'inspect_project()', 'inspect_scene()', 'inspect_object(',
  'inspect_assets()', 'capture_viewport()', 'list_checkpoints()',
  'verify_checkpoint(', 'plan_resume('
]) assert.ok(contract.includes(operation), `missing required read-only operation: ${operation}`);
for (const forbidden of [
  'execute_blender_code', 'arbitrary Python', 'raw Python', 'Save As',
  'checkpoint creation', 'cross-project', 'no client authentication'
]) assert.ok(contract.toLowerCase().includes(forbidden.toLowerCase()), `missing explicit security boundary: ${forbidden}`);
assert.match(contract, /loopback only/i);
assert.match(contract, /challenge\/response MAC/i);
assert.match(contract, /fresh nonces/i);
assert.match(contract, /fail closed/i);
assert.match(contract, /Safe Mode.*not a sandbox/is);
assert.match(contract, /issue #429/i);
for (const issue of ["#430", "#431", "#437", "#440"]) assert.ok(contract.includes(issue), `missing current upstream risk reference: ${issue}`);
assert.match(contract, /historical finding with a reported fix/i);
assert.match(contract, /_check_public_url/);
assert.match(contract, /client disconnect/i);
assert.match(contract, /per-request deadlines/i);
assert.match(contract, /read_factory_settings/i);
assert.match(contract, /canonical repository/i);
assert.match(contract, /physical S21/i);
assert.match(contract, /Gates A–D pass/i);
assert.match(contract, /documentation tests prove contract structure only/i);
assert.match(skill, /BLENDER_PROJECT_ADAPTER_CONTRACT\.md/);
assert.match(skill, /read-only/i);
console.log('PASS: Blender Project Adapter contract is present and attached to the existing MCP tooling skill.');
console.log('PASS: nine read-only operations are specified; arbitrary Python and write operations are explicitly excluded.');
console.log('PASS: Android 5.3.0/S21 compatibility unknowns, authentication, loopback, replay protection and fail-closed behavior are documented.');
console.log('PASS: continuity manifest, checkpoint verification, project isolation and independent acceptance gates are specified.');
console.log('LIMIT: structural contract test only; no Android runtime, add-on, socket or MCP connection is tested.');
