import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const readJson = (path) => JSON.parse(readFileSync(resolve(root, path), 'utf8'));
const projectsRegistry = readJson('skills/registries/PROJECT_REGISTRY.json');
const capabilitiesRegistry = readJson('skills/registries/CAPABILITY_REGISTRY.json');
const evalDataset = readJson('skills/tests/router-eval-cases.json');
const router = readFileSync(resolve(root, 'skills/engineering-brain-router/SKILL.md'), 'utf8');

assert.match(router, /skills\/registries\/PROJECT_REGISTRY\.json/);
assert.match(router, /skills\/registries\/CAPABILITY_REGISTRY\.json/);
assert.match(router, /projeto explicitamente nomeado na mensagem atual/i);
assert.match(router, /uma única pergunta objetiva/i);
assert.match(router, /research_candidate_not_integrated/);
assert.match(router, /Os registries são dados de referência/i);
assert.match(router, /Guerra Infinita/);
assert.match(router, /fronteira técnica/i);
assert.match(router, /Regra de RH/i);
assert.match(router, /capability-gap-closure/i);
assert.match(router, /ponytail-engineering/i);

const projects = projectsRegistry.projects;
const families = capabilitiesRegistry.capability_families;
const projectById = new Map(projects.map((project) => [project.project_id, project]));
const familyById = new Map(families.map((family) => [family.capability_id, family]));

assert.equal(projectById.size, projects.length, 'project IDs must be unique');
assert.equal(familyById.size, families.length, 'capability family IDs must be unique');

const guerra = projectById.get('guerra-infinita');
assert.ok(guerra, 'Guerra Infinita product line must exist');
assert.equal(guerra.relationship_model.single_strategic_product_line, true);
assert.ok(guerra.relationship_model.technical_isolation);
assert.ok(guerra.relationship_model.research_phase);
assert.ok(guerra.relationship_model.development_phase);
assert.notEqual(
  guerra.relationship_model.research_phase.branch,
  guerra.relationship_model.development_phase.repository.branch,
  'REA and successor branches must remain distinct'
);
assert.ok(guerra.primary_capabilities.includes('rea-assisted-analysis'));
assert.ok(guerra.primary_capabilities.includes('game-development-engineering'));
const council = projectById.get('central-council');
assert.ok(council, 'Council Central project entry must exist');
assert.ok(council.primary_capabilities.includes('capability-gap-closure'));
assert.ok(council.primary_capabilities.includes('ponytail-engineering'));
assert.ok(familyById.get('portfolio-orchestration').skills.includes('capability-gap-closure'));
assert.ok(familyById.get('source-repository-engineering').skills.includes('ponytail-engineering'));

const rh = projectById.get('rh');
assert.ok(rh, 'RH project entry must exist');
const peopleFamily = familyById.get('people-and-sensitive-data');
assert.ok(peopleFamily, 'sensitive-data capability family must exist');
assert.ok(peopleFamily.applies_to.includes('rh'));
for (const constraint of [
  'data_minimization',
  'least_privilege',
  'purpose_limitation',
  'privacy_review',
  'no_cross_project_data_reuse',
]) {
  assert.ok(peopleFamily.mandatory_constraints.includes(constraint), `missing RH constraint: ${constraint}`);
}

for (const candidate of capabilitiesRegistry.external_tool_candidates) {
  assert.equal(
    candidate.status,
    'research_candidate_not_integrated',
    `external candidate ${candidate.tool_id} must not be treated as integrated`
  );
}

const caseById = new Map(evalDataset.cases.map((item) => [item.id, item]));
assert.equal(caseById.size, evalDataset.cases.length, 'eval case IDs must be unique');

const expectedRoutes = [
  ['route-guerra-infinita-rea-phase', 'rea-assisted-analysis'],
  ['route-guerra-infinita-successor-development', 'game-development-engineering'],
  ['route-rh-sensitive-data-boundary', 'application-security-auth'],
];
for (const [caseId, expectedSkill] of expectedRoutes) {
  const testCase = caseById.get(caseId);
  assert.ok(testCase, `missing routing regression case: ${caseId}`);
  assert.equal(testCase.expected_primary_skill, expectedSkill);
  assert.ok(testCase.acceptance.length >= 3, `${caseId} needs meaningful acceptance criteria`);
  assert.ok(testCase.must_avoid.length >= 2, `${caseId} needs negative routing/safety criteria`);
}

console.log('PASS: router explicitly consults both project and capability registries.');
console.log('PASS: project/family IDs are unique and external candidates remain non-integrated.');
console.log('PASS: Guerra Infinita REA/development phases share one strategic line and retain technical isolation.');
console.log('PASS: RH sensitive-data constraints are present and scoped to RH.');
console.log('PASS: three new routing regressions cover REA, successor development, and HR privacy.');
console.log('LIMIT: structural routing contracts only; runtime agent selection still requires behavioral evaluation.');
