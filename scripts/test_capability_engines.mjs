import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(root, path), 'utf8');
const router = read('skills/engineering-brain-router/SKILL.md');
const gapProtocol = read('skills/engineering-brain-router/GAP_CLOSURE_PROTOCOL.md');
const gapSkill = read('skills/capability-gap-closure/SKILL.md');
const ponytail = read('skills/ponytail-engineering/SKILL.md');
const status = read('skills/ENGINE_STATUS.md');
const orchestration = read('skills/agent-orchestration/SKILL.md');
const catalog = read('skills/README.md');
const dataset = JSON.parse(read('skills/tests/router-eval-cases.json'));
const registry = JSON.parse(read('skills/registries/CAPABILITY_REGISTRY.json'));
const skillIds = [...new Set([...catalog.matchAll(/\]\(\.\/([^/]+)\/SKILL\.md\)/g)].map((match) => match[1]))];

assert.match(router, /capability-gap-closure/i, 'router must route demonstrated capability gaps to the dedicated workflow');
assert.match(router, /ponytail-engineering/i, 'router must expose the minimal-change engineering lens');
assert.match(router, /não pare em uma recomendação/i, 'router must require safe gap closure rather than advice only');
assert.match(gapProtocol, /Inspect the current project's registry entry/i);
assert.match(gapProtocol, /If still uncovered, use the available GitHub search/i);
assert.match(gapProtocol, /close the loop/i);
assert.match(gapSkill, /do not stop at recommending/i);
assert.match(gapSkill, /GitHub search/i);
assert.match(gapSkill, /BLOCKED/i);
assert.match(gapSkill, /Do not install plugins/i);
assert.match(ponytail, /Decision ladder/i);
assert.match(ponytail, /Never cut/i);
assert.match(ponytail, /upstream/i);
assert.match(ponytail, /does not authorize installing the upstream plugin/i);
assert.match(status, /Behavioral PASS/i);
assert.match(orchestration, /DAG/);
assert.match(orchestration, /NOT RUN/);
assert.match(catalog, /ponytail-engineering/i);
assert.match(catalog, /capability-gap-closure/i);

const familySkills = new Set(registry.capability_families.flatMap((family) => family.skills));
const evaluatedSkills = new Set(dataset.cases.map((item) => item.expected_primary_skill).filter(Boolean));
assert.equal(skillIds.length, 37, 'catalog skill count must match the audited 37-skill inventory');
for (const skillId of skillIds) {
  assert.ok(familySkills.has(skillId), `skill is not mapped to a capability family: ${skillId}`);
  assert.ok(evaluatedSkills.has(skillId), `skill has no direct primary-route eval case: ${skillId}`);
}
assert.equal(familySkills.size, 37, 'all catalog skills must be represented by capability families');
assert.equal(evaluatedSkills.size, 37, 'all catalog skills must have direct route evaluation');

const ids = new Set(dataset.cases.map((item) => item.id));
for (const id of [
  'route-ponytail-minimal-change',
  'route-capability-gap-closure',
  'autonomy-discover-and-close-skill-gap',
  'autonomy-stop-before-paid-or-global-install',
  'route-multi-agent-orchestration',
]) {
  assert.ok(ids.has(id), `missing capability-engine regression case: ${id}`);
}

console.log('PASS: router exposes the gap-closure and minimal-change capabilities.');
console.log('PASS: discovery workflow requires internal-first research, external comparison, and evidence.');
console.log('PASS: Ponytail adaptation preserves security, tests, and installation boundaries.');
console.log('PASS: every catalog skill is mapped to a capability family and has a direct route-evaluation case.');
console.log('PASS: engine inventory and new routing/autonomy regression cases are present.');
