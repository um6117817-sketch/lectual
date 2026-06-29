// ===== Configuration =====
const API_BASE = 'http://localhost:8000/api/v1';

// ===== State Management =====
const state = {
  todos: [],
  filters: {
    status: '',
    priority: '',
  },
  pagination: {
    page: 1,
    size: 20,
    total: 0,
    pages: 0,
  },
  editingTodo: null,
};

// ===== Localization =====
const PRIORITY_LABELS = {
  low: '低',
  medium: '中',
  high: '高',
};

const STATUS_LABELS = {
  todo: '待办',
  in_progress: '进行中',
  done: '已完成',
};

// ===== Utility Functions =====
function priorityLabel(value) {
  return PRIORITY_LABELS[value] || value;
}

function statusLabel(value) {
  return STATUS_LABELS[value] || value;
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr.replace(' ', 'T') + 'Z');
  if (isNaN(d.getTime())) return dateStr;
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function showModal() {
  document.getElementById('edit-modal').classList.remove('hidden');
}

function hideModal() {
  document.getElementById('edit-modal').classList.add('hidden');
  state.editingTodo = null;
  document.getElementById('edit-error').classList.add('hidden');
}

// ===== API Client =====
async function apiRequest(method, path, body = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) {
    options.body = JSON.stringify(body);
  }
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    let detail = `HTTP ${response.status}`;
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch {}
    throw new Error(detail);
  }
  return response.json();
}

async function getTodos() {
  const params = new URLSearchParams();
  if (state.filters.status) params.set('status', state.filters.status);
  if (state.filters.priority) params.set('priority', state.filters.priority);
  params.set('page', state.pagination.page);
  params.set('size', state.pagination.size);

  return apiRequest('GET', `/todos?${params.toString()}`);
}

async function getTodo(id) {
  return apiRequest('GET', `/todos/${id}`);
}

async function createTodo(todo) {
  return apiRequest('POST', '/todos', todo);
}

async function updateTodo(id, todo) {
  return apiRequest('PUT', `/todos/${id}`, todo);
}

async function deleteTodo(id) {
  return apiRequest('DELETE', `/todos/${id}`);
}

// ===== UI Rendering =====
function renderTodoCard(todo) {
  return `
    <div class="todo-card" data-id="${todo.id}">
      <div class="todo-card-content">
        <div class="todo-card-title">${escapeHtml(todo.title)}</div>
        ${todo.description ? `<div class="todo-card-desc">${escapeHtml(todo.description)}</div>` : ''}
        <div class="todo-card-meta">
          <span class="badge badge-priority-${todo.priority}">${priorityLabel(todo.priority)}</span>
          <span class="badge badge-status-${todo.status}">${statusLabel(todo.status)}</span>
          <span class="todo-card-date">${formatDate(todo.updated_at)}</span>
        </div>
      </div>
      <div class="todo-card-actions">
        <button class="btn btn-sm btn-primary" onclick="openEditModal(${todo.id})">编辑</button>
        <button class="btn btn-sm btn-danger" onclick="handleDelete(${todo.id})">删除</button>
        ${renderStatusButtons(todo)}
      </div>
    </div>
  `;
}

function renderStatusButtons(todo) {
  if (todo.status === 'done') return '';
  const nextStatus = todo.status === 'todo' ? 'in_progress' : 'done';
  const label = nextStatus === 'in_progress' ? '开始' : '完成';
  return `<button class="btn btn-sm btn-secondary" onclick="handleStatusChange(${todo.id}, '${nextStatus}')">${label}</button>`;
}

function renderPagination() {
  const { page, pages } = state.pagination;
  const paginationEl = document.getElementById('pagination');
  const prevBtn = document.getElementById('prev-page');
  const nextBtn = document.getElementById('next-page');
  const pageInfo = document.getElementById('page-info');

  if (pages <= 1) {
    paginationEl.classList.add('hidden');
  } else {
    paginationEl.classList.remove('hidden');
    prevBtn.disabled = page <= 1;
    nextBtn.disabled = page >= pages;
    pageInfo.textContent = `第 ${page} 页 / 共 ${pages} 页`;
  }
}

async function renderTodoList() {
  const listEl = document.getElementById('todo-list');
  const emptyEl = document.getElementById('empty-state');
  const loadingEl = document.getElementById('loading-state');
  const errorEl = document.getElementById('error-state');

  // Show loading
  listEl.innerHTML = '';
  emptyEl.classList.add('hidden');
  errorEl.classList.add('hidden');
  loadingEl.classList.remove('hidden');

  try {
    const data = await getTodos();
    state.todos = data.items;
    state.pagination.total = data.total;
    state.pagination.pages = data.pages;

    loadingEl.classList.add('hidden');

    if (data.items.length === 0) {
      emptyEl.classList.remove('hidden');
      listEl.innerHTML = '';
    } else {
      emptyEl.classList.add('hidden');
      listEl.innerHTML = data.items.map(renderTodoCard).join('');
    }

    renderPagination();
  } catch (err) {
    loadingEl.classList.add('hidden');
    errorEl.classList.remove('hidden');
    console.error('Failed to load todos:', err);
  }
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ===== Event Handlers =====
async function handleCreate(e) {
  e.preventDefault();

  const titleInput = document.getElementById('title-input');
  const descInput = document.getElementById('desc-input');
  const prioritySelect = document.getElementById('priority-select');
  const statusSelect = document.getElementById('status-select');
  const errorEl = document.getElementById('create-error');
  const submitBtn = document.getElementById('submit-btn');

  const title = titleInput.value.trim();
  if (!title) {
    errorEl.textContent = '标题不能为空';
    errorEl.classList.remove('hidden');
    return;
  }

  errorEl.classList.add('hidden');
  submitBtn.disabled = true;
  submitBtn.textContent = '创建中...';

  try {
    await createTodo({
      title,
      description: descInput.value.trim(),
      priority: prioritySelect.value,
      status: statusSelect.value,
    });

    // Reset form
    titleInput.value = '';
    descInput.value = '';
    prioritySelect.value = 'medium';
    statusSelect.value = 'todo';

    // Refresh list
    state.pagination.page = 1;
    await renderTodoList();
  } catch (err) {
    errorEl.textContent = `创建失败: ${err.message}`;
    errorEl.classList.remove('hidden');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = '➕ 创建事项';
  }
}

async function openEditModal(id) {
  try {
    const todo = await getTodo(id);
    state.editingTodo = todo;

    document.getElementById('edit-id').value = todo.id;
    document.getElementById('edit-title').value = todo.title;
    document.getElementById('edit-desc').value = todo.description || '';
    document.getElementById('edit-priority').value = todo.priority;
    document.getElementById('edit-status').value = todo.status;
    document.getElementById('edit-error').classList.add('hidden');

    showModal();
  } catch (err) {
    alert(`获取事项失败: ${err.message}`);
  }
}

async function handleEdit(e) {
  e.preventDefault();

  const id = parseInt(document.getElementById('edit-id').value);
  const title = document.getElementById('edit-title').value.trim();
  const desc = document.getElementById('edit-desc').value.trim();
  const priority = document.getElementById('edit-priority').value;
  const status = document.getElementById('edit-status').value;
  const errorEl = document.getElementById('edit-error');

  if (!title) {
    errorEl.textContent = '标题不能为空';
    errorEl.classList.remove('hidden');
    return;
  }

  errorEl.classList.add('hidden');

  try {
    await updateTodo(id, {
      title,
      description: desc,
      priority,
      status,
    });
    hideModal();
    await renderTodoList();
  } catch (err) {
    errorEl.textContent = `更新失败: ${err.message}`;
    errorEl.classList.remove('hidden');
  }
}

async function handleDelete(id) {
  if (!confirm('确定要删除这个事项吗？')) return;
  try {
    await deleteTodo(id);
    await renderTodoList();
  } catch (err) {
    alert(`删除失败: ${err.message}`);
  }
}

async function handleStatusChange(id, newStatus) {
  try {
    await updateTodo(id, { status: newStatus });
    await renderTodoList();
  } catch (err) {
    alert(`状态更新失败: ${err.message}`);
  }
}

function handleFilterChange() {
  state.filters.status = document.getElementById('filter-status').value;
  state.filters.priority = document.getElementById('filter-priority').value;
  state.pagination.page = 1;
  renderTodoList();
}

function handlePrevPage() {
  if (state.pagination.page > 1) {
    state.pagination.page--;
    renderTodoList();
  }
}

function handleNextPage() {
  if (state.pagination.page < state.pagination.pages) {
    state.pagination.page++;
    renderTodoList();
  }
}

// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', () => {
  // Create form
  document.getElementById('create-form').addEventListener('submit', handleCreate);

  // Edit form
  document.getElementById('edit-form').addEventListener('submit', handleEdit);
  document.getElementById('cancel-edit').addEventListener('click', hideModal);
  document.getElementById('close-modal').addEventListener('click', hideModal);

  // Close modal on backdrop click
  document.getElementById('edit-modal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) hideModal();
  });

  // Filters
  document.getElementById('filter-status').addEventListener('change', handleFilterChange);
  document.getElementById('filter-priority').addEventListener('change', handleFilterChange);

  // Pagination
  document.getElementById('prev-page').addEventListener('click', handlePrevPage);
  document.getElementById('next-page').addEventListener('click', handleNextPage);

  // Initial load
  renderTodoList();
});
