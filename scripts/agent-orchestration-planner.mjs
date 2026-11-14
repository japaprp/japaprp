/**
 * Deterministic, side-effect-free DAG planner for Council Central.
 * It selects tasks eligible for dispatch; it does not spawn agents or execute tools.
 */

const VALID_RISKS = new Set(['low', 'medium', 'high', 'critical']);
const MAX_VERIFIED_CONCURRENCY = 10;

export function validatePlan(plan) {
  if (!plan || typeof plan !== 'object' || Array.isArray(plan)) throw new TypeError('plan must be an object');
  if (typeof plan.project_id !== 'string' || !plan.project_id.trim()) throw new Error('plan.project_id is required');
  if (!Array.isArray(plan.tasks) || plan.tasks.length === 0) throw new Error('plan.tasks must be a non-empty array');

  const byId = new Map();
  for (const task of plan.tasks) {
    if (!task || typeof task !== 'object' || Array.isArray(task)) throw new Error('each task must be an object');
    if (typeof task.task_id !== 'string' || !task.task_id.trim()) throw new Error('task_id is required');
    if (byId.has(task.task_id)) throw new Error(`duplicate task_id: ${task.task_id}`);
    if (task.project_id !== plan.project_id) throw new Error(`cross-project task rejected: ${task.task_id}`);
    if (typeof task.assigned_role !== 'string' || !task.assigned_role.trim()) throw new Error(`assigned_role is required: ${task.task_id}`);
    if (!VALID_RISKS.has(task.risk)) throw new Error(`invalid risk for task: ${task.task_id}`);
    const dependencies = task.depends_on ?? [];
    const resources = task.resources ?? [];
    if (!Array.isArray(dependencies) || dependencies.some((id) => typeof id !== 'string' || !id.trim())) throw new Error(`depends_on must contain non-empty task IDs: ${task.task_id}`);
    if (new Set(dependencies).size !== dependencies.length) throw new Error(`duplicate dependency: ${task.task_id}`);
    if (!Array.isArray(resources) || resources.some((resource) => typeof resource !== 'string' || !resource.trim())) throw new Error(`resources must contain non-empty strings: ${task.task_id}`);
    if (new Set(resources).size !== resources.length) throw new Error(`duplicate resource: ${task.task_id}`);
    byId.set(task.task_id, task);
  }

  for (const task of plan.tasks) {
    for (const dependency of task.depends_on ?? []) {
      if (!byId.has(dependency)) throw new Error(`unknown dependency ${dependency} for task ${task.task_id}`);
      if (dependency === task.task_id) throw new Error(`self dependency: ${task.task_id}`);
    }
  }

  const visiting = new Set();
  const visited = new Set();
  function visit(taskId) {
    if (visiting.has(taskId)) throw new Error(`dependency cycle detected at task: ${taskId}`);
    if (visited.has(taskId)) return;
    visiting.add(taskId);
    for (const dependency of byId.get(taskId).depends_on ?? []) visit(dependency);
    visiting.delete(taskId);
    visited.add(taskId);
  }
  for (const taskId of byId.keys()) visit(taskId);
  return { taskCount: byId.size, taskIds: [...byId.keys()] };
}

export function selectReadyTasks(plan, options = {}) {
  validatePlan(plan);
  const completedIds = options.completedIds ?? [];
  const runningIds = options.runningIds ?? [];
  if (!Array.isArray(completedIds) || !Array.isArray(runningIds)) throw new Error('completedIds and runningIds must be arrays');
  const completed = new Set(completedIds);
  const running = new Set(runningIds);
  if (completed.size !== completedIds.length || running.size !== runningIds.length) throw new Error('task state IDs must be unique');
  if ([...completed].some((id) => running.has(id))) throw new Error('a task cannot be completed and running at the same time');
  const maxConcurrency = options.maxConcurrency ?? 5;
  if (!Number.isInteger(maxConcurrency) || maxConcurrency < 1 || maxConcurrency > MAX_VERIFIED_CONCURRENCY) {
    throw new Error(`maxConcurrency must be between 1 and the verified ceiling of ${MAX_VERIFIED_CONCURRENCY}`);
  }

  const byId = new Map(plan.tasks.map((task) => [task.task_id, task]));
  for (const id of [...completed, ...running]) {
    if (!byId.has(id)) throw new Error(`unknown task state id: ${id}`);
  }
  const activeResources = new Set();
  for (const id of running) {
    for (const resource of byId.get(id).resources ?? []) activeResources.add(resource);
  }
  const slots = Math.max(0, maxConcurrency - running.size);
  if (slots === 0) return [];

  const selected = [];
  for (const task of plan.tasks) {
    if (selected.length >= slots) break;
    if (completed.has(task.task_id) || running.has(task.task_id)) continue;
    if (!(task.depends_on ?? []).every((id) => completed.has(id))) continue;
    const resources = task.resources ?? [];
    if (resources.some((resource) => activeResources.has(resource))) continue;
    selected.push(task.task_id);
    for (const resource of resources) activeResources.add(resource);
  }
  return selected;
}
