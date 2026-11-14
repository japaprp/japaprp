/**
 * Deterministic, side-effect-free DAG planner for Council Central.
 * It selects tasks eligible for dispatch; it does not spawn agents or execute tools.
 */

const VALID_RISKS = new Set(['low', 'medium', 'high', 'critical']);

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
    if (!Array.isArray(task.depends_on ?? [])) throw new Error(`depends_on must be an array: ${task.task_id}`);
    if (!Array.isArray(task.resources ?? [])) throw new Error(`resources must be an array: ${task.task_id}`);
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
  const completed = new Set(options.completedIds ?? []);
  const running = new Set(options.runningIds ?? []);
  const maxConcurrency = options.maxConcurrency ?? 5;
  if (!Number.isInteger(maxConcurrency) || maxConcurrency < 1) throw new Error('maxConcurrency must be a positive integer');

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
