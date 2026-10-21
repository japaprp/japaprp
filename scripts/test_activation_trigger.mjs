import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const trigger = 'DEUS É FIEL';
const skill = readFileSync(resolve(root, 'skills/engineering-brain-router/SKILL.md'), 'utf8');
const dataset = JSON.parse(readFileSync(resolve(root, 'skills/tests/router-eval-cases.json'), 'utf8'));

const frontmatter = skill.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
assert.ok(frontmatter, 'router skill must have valid frontmatter delimiters');
assert.match(frontmatter[1], /description:.*DEUS É FIEL/, 'skill description must expose the activation phrase to routing');
assert.match(skill, /## Gatilho de continuidade — `DEUS É FIEL`/, 'router must define the activation procedure');
for (const requiredStep of [
  'Reconstruir o contexto',
  'Preservar isolamento',
  'Selecionar skills',
  'Tomar decisões dentro da autorização existente',
  'Verificar e relatar',
  'Manter continuidade',
]) {
  assert.ok(skill.includes(requiredStep), `activation procedure is missing step: ${requiredStep}`);
}
assert.match(skill, /não concede novas permissões/i, 'activation must not grant additional permissions');
assert.match(skill, /não autoriza misturar projetos/i, 'activation must preserve project isolation');

const cases = dataset.cases;
assert.ok(Array.isArray(cases), 'routing eval dataset must contain cases');
const ids = cases.map((item) => item.id);
assert.equal(new Set(ids).size, ids.length, 'routing eval case IDs must be unique');
const activationCase = cases.find((item) => item.id === 'route-deus-e-fiel-activation');
assert.ok(activationCase, 'dedicated activation regression case must exist');
assert.ok(activationCase.prompt.includes(trigger), 'activation regression prompt must include the exact trigger');
assert.equal(activationCase.expected_primary_skill, 'engineering-brain-router', 'activation must route to the engineering brain router');
assert.ok(activationCase.acceptance.length > 0, 'activation case must define acceptance criteria');
assert.ok(activationCase.must_avoid.length > 0, 'activation case must define prohibited behaviors');

console.log('PASS: activation phrase is discoverable in skill metadata.');
console.log('PASS: continuity procedure includes context recovery, isolation, skill routing, bounded autonomy, verification, and continuity.');
console.log('PASS: permissions and project-isolation guardrails are explicit.');
console.log('PASS: dedicated activation regression case is valid and uniquely identified.');
console.log('LIMIT: this is a deterministic structural regression test; it does not prove behavior in a fresh agent session.');
