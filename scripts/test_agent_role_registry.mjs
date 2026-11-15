import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(root, path), 'utf8');
const registry = JSON.parse(read('skills/registries/AGENT_ROLE_REGISTRY.json'));
const adapter = read('skills/agent-orchestration/AGENT_RUNTIME_ADAPTER_CONTRACT.md');
const orchestration = read('skills/agent-orchestration/SKILL.md');
const skillFiles = new Set([
  'agent-orchestration','ai-integration-evaluation','ai-token-budget','api-engineering-contracts',
  'application-security-auth','code-review-minimal-change','cryptography-security-analysis',
  'engineering-brain-router','mcp-tooling-engineering','rea-assisted-analysis',
  'repo-reverse-engineering','targeted-debugging-performance','testing-regression-quality'
]);
const expected = [
  'agent-evaluator','harness-optimizer','silent-failure-hunter','spec-miner',
  'loop-operator','security-reviewer','pr-test-analyzer','opensource-sanitizer'
];
assert.equal(registry.project_id, 'central-council');
assert.equal(registry.status, 'catalogued_not_runtime_active');
assert.equal(registry.roles.length, 8);
assert.deepEqual(registry.roles.map((r) => r.role_id).sort(), [...expected].sort());
assert.equal(registry.default_permission_profile.mode, 'read_only');
assert.equal(registry.default_permission_profile.write_scope, 'none_by_default');
for (const role of registry.roles) {
  assert.ok(skillFiles.has(role.primary_skill), `unknown primary skill for ${role.role_id}`);
  for (const skill of role.supporting_skills) assert.ok(skillFiles.has(skill), `unknown supporting skill ${skill}`);
  assert.equal(role.default_permission_profile, 'read_only');
  assert.equal(role.qa_independence_required, true);
  assert.ok(role.triggers.length > 0);
}
for (const operation of ['discover_runtime','inspect_capabilities','dispatch_child_agent','get_task_status','cancel_task','collect_execution_receipt']) assert.ok(adapter.includes(operation), `missing adapter operation ${operation}`);
for (const field of registry.runtime_binding.required_receipt_fields) assert.ok(adapter.includes(field), `missing receipt field ${field}`);
assert.match(adapter, /parallel set of ordinary tool calls is not proof/i);
assert.match(adapter, /BLOCKED/);
assert.match(adapter, /independent QA/i);
assert.match(orchestration, /AGENT_ROLE_REGISTRY\.json/);
assert.match(orchestration, /catalogued_not_runtime_active/);
console.log('PASS: eight specialist roles are uniquely registered and mapped to existing skills.');
console.log('PASS: all roles default to read-only with independent QA required.');
console.log('PASS: runtime adapter operations, isolation, receipts, cancellation and failure gates are specified.');
console.log('LIMIT: these checks validate registry and contract structure only; no live agent runtime is activated.');
