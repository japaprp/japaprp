import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const trigger = 'Deus é fiel';
const bootstrap = readFileSync(resolve(root, 'AGENTS.md'), 'utf8');
const copilotInstructions = readFileSync(resolve(root, '.github/copilot-instructions.md'), 'utf8');
const skill = readFileSync(resolve(root, 'skills/engineering-brain-router/SKILL.md'), 'utf8');
const protocol = readFileSync(resolve(root, 'skills/engineering-brain-router/GAP_CLOSURE_PROTOCOL.md'), 'utf8');
const testPlan = readFileSync(resolve(root, 'skills/tests/ACTIVATION_AUTONOMY_TESTS.md'), 'utf8');
const dataset = JSON.parse(readFileSync(resolve(root, 'skills/tests/router-eval-cases.json'), 'utf8'));

assert.ok(bootstrap.toLowerCase().includes(trigger.toLowerCase()), 'repository bootstrap must expose the activation phrase');
assert.ok(copilotInstructions.toLowerCase().includes(trigger.toLowerCase()), 'Copilot repository instructions must expose the activation phrase');
assert.match(copilotInstructions, /grants no new permissions/i, 'Copilot instructions must preserve authorization boundaries');
assert.match(copilotInstructions, /do not merge, deploy/i, 'Copilot instructions must preserve merge/deploy boundaries');
assert.match(bootstrap, /Read `skills\/engineering-brain-router\/SKILL\.md` and `skills\/engineering-brain-router\/GAP_CLOSURE_PROTOCOL\.md`/i,
  'bootstrap must instruct the agent to load the router and gap-closure protocol');
assert.match(skill, /Gatilho persistente de ativação/i, 'router must define the activation procedure');
assert.match(skill, /não concede permissões novas/i, 'activation must not grant additional permissions');
assert.match(skill, /merge/i, 'router must document merge boundaries');
assert.match(skill, /deploy/i, 'router must document deployment boundaries');
assert.match(protocol, /Nível 1 — rotina/i, 'protocol must define routine autonomy');
assert.match(protocol, /Nível 2 — reversível e isolado/i, 'protocol must define reversible isolated work');
assert.match(protocol, /Nível 3 — impacto externo ou custo/i, 'protocol must define approval boundaries for external impact/cost');
assert.match(protocol, /Nível 4 — crítico/i, 'protocol must define critical-operation boundaries');
assert.match(protocol, /sessão nova/i, 'protocol must require fresh-session behavioral validation');
assert.match(testPlan, /Test A — activation and state recovery/i, 'manual fresh-session test A must exist');
assert.match(testPlan, /Test B — routine autonomy/i, 'manual autonomy test B must exist');
assert.match(testPlan, /Test C — approval boundary/i, 'manual approval-boundary test C must exist');

const cases = dataset.cases;
assert.ok(Array.isArray(cases), 'routing eval dataset must contain cases');
const ids = cases.map((item) => item.id);
assert.equal(new Set(ids).size, ids.length, 'routing eval case IDs must be unique');
for (const id of [
  'activate-central-new-session',
  'route-deus-e-fiel-multi-project-disambiguation',
  'autonomy-routine-work',
  'autonomy-impact-boundary',
]) {
  assert.ok(cases.some((item) => item.id === id), `required regression case must exist: ${id}`);
}
const activationCase = cases.find((item) => item.id === 'activate-central-new-session');
assert.ok(activationCase.prompt.toLowerCase().includes(trigger.toLowerCase()), 'activation regression prompt must include the trigger');
assert.equal(activationCase.expected_primary_skill, 'engineering-brain-router',
  'activation must route to the engineering brain router');

console.log('PASS: activation bootstrap, Copilot repository instructions, and router procedure are present.');
console.log('PASS: routine autonomy and impact/critical approval boundaries are explicit.');
console.log('PASS: fresh-session, autonomy, and approval-boundary test plans exist.');
console.log('PASS: activation, multi-project isolation, and autonomy regression cases exist with unique IDs.');
console.log('LIMIT: deterministic structural regression only; fresh-session runtime behavior is not proven.');
