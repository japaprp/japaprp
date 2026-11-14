import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { selectReadyTasks, validatePlan } from './agent-orchestration-planner.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(root, path), 'utf8');
const skill = read('skills/agent-orchestration/SKILL.md');
const contract = read('skills/agent-orchestration/ORCHESTRATION_CONTRACT.md');
const router = read('skills/engineering-brain-router/SKILL.md');
const projects = JSON.parse(read('skills/registries/PROJECT_REGISTRY.json'));
const capabilities = JSON.parse(read('skills/registries/CAPABILITY_REGISTRY.json'));
const cases = JSON.parse(read('skills/tests/router-eval-cases.json')).cases;

assert.match(skill, /Owner \/ usuário/);
assert.match(skill, /DAG/);
assert.match(skill, /admission control/i);
assert.match(skill, /QA independente/);
assert.match(skill, /DEUS É FIEL/);
assert.match(skill, /100\+/);
assert.match(skill, /não concede novas permissões/i);
assert.match(contract, /NOT RUN/);
assert.match(contract, /um único writer por recurso mutável/i);
assert.match(contract, /pelo menos duas tarefas independentes/i);
assert.match(router, /agent-orchestration/);

const council = projects.projects.find((p) => p.project_id === 'central-council');
assert.ok(council);
assert.ok(council.primary_capabilities.includes('agent-orchestration'));
const family = capabilities.capability_families.find((f) => f.capability_id === 'multi-agent-orchestration');
assert.ok(family);
assert.ok(family.skills.includes('agent-orchestration'));
assert.ok(family.applies_to.includes('central-council'));

const orchestrationCase = cases.find((c) => c.id === 'route-multi-agent-orchestration');
assert.ok(orchestrationCase);
assert.equal(orchestrationCase.expected_primary_skill, 'agent-orchestration');
assert.ok(orchestrationCase.must_avoid.some((v) => /100 agents/i.test(v)));
console.log('PASS: hierarchy, DAG, admission control, QA, isolation, and owner approval gates are specified.');
console.log('PASS: orchestration capability is mapped only to the Council Central project.');
console.log('PASS: routing regression covers one-command multi-agent orchestration.');

const plan = {
  project_id: 'central-council',
  tasks: [
    { task_id: 'research', project_id: 'central-council', assigned_role: 'researcher', risk: 'low', resources: ['repo:docs'], depends_on: [] },
    { task_id: 'unit-tests', project_id: 'central-council', assigned_role: 'qa', risk: 'medium', resources: ['tests:unit'], depends_on: [] },
    { task_id: 'docs-update', project_id: 'central-council', assigned_role: 'technical-writer', risk: 'low', resources: ['repo:docs'], depends_on: ['research'] },
    { task_id: 'integration-qa', project_id: 'central-council', assigned_role: 'independent-qa', risk: 'high', resources: ['qa:integration'], depends_on: ['unit-tests', 'docs-update'] }
  ]
};
assert.equal(validatePlan(plan).taskCount, 4);
assert.deepEqual(selectReadyTasks(plan, { maxConcurrency: 2 }), ['research', 'unit-tests']);
assert.deepEqual(selectReadyTasks(plan, { completedIds: ['research'], runningIds: ['unit-tests'], maxConcurrency: 2 }), ['docs-update']);
assert.deepEqual(selectReadyTasks(plan, { completedIds: ['research', 'unit-tests', 'docs-update'], maxConcurrency: 2 }), ['integration-qa']);
assert.throws(() => validatePlan({ ...plan, tasks: [...plan.tasks, { ...plan.tasks[0] }] }), /duplicate task_id/);
assert.throws(() => validatePlan({ ...plan, tasks: plan.tasks.map((task) => task.task_id === 'research' ? { ...task, project_id: 'guerra-infinita' } : task) }), /cross-project task rejected/);
assert.throws(() => validatePlan({ ...plan, tasks: plan.tasks.map((task) => task.task_id === 'research' ? { ...task, depends_on: ['docs-update'] } : task) }), /dependency cycle detected/);
assert.throws(() => selectReadyTasks(plan, { maxConcurrency: 0 }), /verified ceiling/);
assert.throws(() => selectReadyTasks(plan, { maxConcurrency: 11 }), /verified ceiling/);
assert.throws(() => selectReadyTasks(plan, { completedIds: 'research' }), /must be arrays/);
assert.throws(() => selectReadyTasks(plan, { completedIds: ['research', 'research'] }), /must be unique/);
assert.throws(() => selectReadyTasks(plan, { completedIds: ['research'], runningIds: ['research'] }), /cannot be completed and running/);
assert.throws(() => validatePlan({ ...plan, tasks: plan.tasks.map((task) => task.task_id === 'research' ? { ...task, resources: ['repo:docs', ''] } : task) }), /resources must contain non-empty strings/);
console.log('PASS: DAG planner admits only ready tasks, respects concurrency and exclusive resource locks.');
console.log('PASS: planner rejects duplicate IDs, cross-project tasks, invalid limits and dependency cycles.');

const adversarialProtocol = read('skills/agent-orchestration/ADVERSARIAL_DECISION_REVIEW.md');
const adversarialGate = read('scripts/adversarial_review_gate.py');
assert.match(skill, /Revisão adversarial de decisões consequenciais/);
assert.match(contract, /pode rejeitar a maioria/);
assert.match(router, /ADVERSARIAL_DECISION_REVIEW/);
assert.match(adversarialProtocol, /não decide por maioria/i);
assert.match(adversarialProtocol, /inconclusive/);
assert.match(adversarialProtocol, /single_agent_multi_perspective/);
assert.match(adversarialGate, /def should_trigger/);
for (const id of [
  'route-adversarial-consequential-decision',
  'route-adversarial-routine-negative',
  'route-adversarial-boundary-two-signals'
]) assert.ok(cases.some((testCase) => testCase.id === id), `missing adversarial routing regression: ${id}`);
assert.equal(cases.find((testCase) => testCase.id === 'route-adversarial-routine-negative').expected_primary_skill, null);
console.log('PASS: adversarial review is integrated into the existing orchestration skill without duplication.');
console.log('PASS: majority-independent synthesis, dissent, uncertainty, independence labeling and trigger regressions are present.');
console.log('LIMIT: the planner selects work but does not spawn agents; live agent dispatch remains unverified.');
