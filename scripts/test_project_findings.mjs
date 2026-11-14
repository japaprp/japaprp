import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const readJson = (path) => JSON.parse(readFileSync(resolve(root, path), 'utf8'));
const findings = readJson('skills/registries/PROJECT_FINDINGS.json');
const projects = readJson('skills/registries/PROJECT_REGISTRY.json').projects;
const projectIds = new Set(projects.map((project) => project.project_id));
const allowedStatuses = new Set(['PASS', 'FAIL', 'BLOCKED', 'NOT RUN']);
const allowedEvidenceLabels = new Set(['OBSERVED', 'INFERRED', 'HYPOTHESIS', 'UNKNOWN']);
const ids = new Set();

assert.equal(findings.schema_version, '1.0.0');
assert.equal(findings.registry_kind, 'project_findings');
assert.ok(findings.policy?.closure_rule?.includes('final commit'));
assert.ok(findings.policy?.isolation?.includes('separate research and development fronts'));
assert.ok(Array.isArray(findings.findings) && findings.findings.length > 0);

for (const finding of findings.findings) {
  assert.match(finding.finding_id, /^[A-Z][A-Z0-9]*-\d{3}$/);
  assert.ok(!ids.has(finding.finding_id), `duplicate finding_id: ${finding.finding_id}`);
  ids.add(finding.finding_id);

  assert.ok(projectIds.has(finding.project_id), `unknown project_id for ${finding.finding_id}: ${finding.project_id}`);
  assert.ok(allowedStatuses.has(finding.status), `invalid status for ${finding.finding_id}`);
  assert.ok(['P0', 'P1', 'P2', 'P3'].includes(finding.priority));
  assert.ok(finding.source?.kind && finding.source?.reference, `missing source provenance for ${finding.finding_id}`);
  assert.ok(allowedEvidenceLabels.has(finding.source.evidence_label), `invalid evidence label for ${finding.finding_id}`);
  assert.ok(Array.isArray(finding.evidence) && finding.evidence.length > 0);
  assert.ok(Array.isArray(finding.closure_gate) && finding.closure_gate.length > 0);
  assert.ok(finding.regression_test?.path && finding.regression_test?.test);

  if (finding.fix !== null) {
    assert.ok(Array.isArray(finding.fix.pr_numbers));
    assert.ok(finding.fix.branch);
  }

  if (finding.status === 'PASS') {
    assert.ok(finding.fix?.correction_commit, `PASS finding lacks correction commit: ${finding.finding_id}`);
    assert.ok(finding.closure?.regression_test_passed === true, `PASS finding lacks passing regression evidence: ${finding.finding_id}`);
    assert.ok(finding.closure?.verified_commit === finding.fix.correction_commit, `PASS finding is not closed on its final correction commit: ${finding.finding_id}`);
  }

  if (finding.front === 'dark-war-survival-rea') {
    assert.equal(finding.project_id, 'guerra-infinita', 'REA must remain within its strategic product line');
    assert.ok(!finding.fix || finding.fix.branch.startsWith('research/'), 'REA fixes must not point into the game-development branch');
  }

  if (finding.project_id === 'guerra-infinita' && finding.front === 'development') {
    assert.ok(!finding.source.reference.includes('DarkWar_Analysis_Core'), 'development findings must not cite REA workspace paths as source code');
  }
}

assert.equal(ids.size, findings.findings.length);
console.log(`PASS: ${ids.size} findings have unique stable IDs and valid project references.`);
console.log('PASS: every finding has provenance, evidence, a regression-test definition and closure gates.');
console.log('PASS: PASS status requires both a passing regression and the exact final correction commit.');
console.log('PASS: Dark War REA and Guerra Infinita development are represented as separate fronts.');
console.log('LIMIT: this validates register integrity only; it does not prove any project finding is fixed.');
