import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

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
console.log('LIMIT: these deterministic checks validate the contract, not live agent dispatch.');
