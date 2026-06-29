# Todo App — 开发任务清单

> **项目名称**: todo-app  
> **项目经理**: AI PM Agent  
> **委托人**: 老王  
> **创建日期**: 2026-06-29  
> **技术栈**: 后端 Python (FastAPI)，前端 Node.js (原生 HTML/CSS/JS)  
> **项目路径**: `/opt/hermes/projects/todo-app/`

---

## 一、项目概述

一个简单的待办事项（Todo）管理应用。用户可以创建、查看、编辑、删除待办事项。每个事项包含标题、描述、优先级（低/中/高）、状态（待办/进行中/已完成）。后端使用 FastAPI 提供 RESTful API 数据服务，前端使用 Node.js 搭建静态资源服务器并渲染交互界面。

### 1.1 核心功能

| 功能 | 描述 |
|------|------|
| 创建事项 | 用户填写标题、描述、优先级，创建新的待办事项 |
| 查看列表 | 分页展示所有待办事项，支持按优先级/状态筛选 |
| 查看详情 | 查看单个待办事项的完整信息 |
| 编辑事项 | 修改已有事项的标题、描述、优先级、状态 |
| 删除事项 | 删除指定的事项（硬删除） |
| 状态流转 | 待办 → 进行中 → 已完成 |

### 1.2 数据模型

```
TodoItem {
    id:          int          (主键，自增)
    title:       string       (必填，1-200 字符)
    description: string       (可选，最大 2000 字符)
    priority:    enum         (low | medium | high，默认 medium)
    status:      enum         (todo | in_progress | done，默认 todo)
    created_at:  datetime     (自动生成)
    updated_at:  datetime     (自动更新)
}
```

---

## 二、项目文件结构

```
/opt/hermes/projects/todo-app/
├── TASKS.md                  ← 本文件（任务清单）
├── README.md                 ← 项目说明
├── backend/                  ← 后端 Python/FastAPI
│   ├── requirements.txt      ← Python 依赖
│   ├── main.py               ← 应用入口，FastAPI 实例化 & CORS 配置
│   ├── database.py           ← SQLite 数据库连接 & 表初始化
│   ├── models.py             ← Pydantic 数据模型定义
│   ├── schemas.py            ← 请求/响应 Schema
│   ├── crud.py               ← 数据库 CRUD 操作
│   ├── routers/
│   │   └── todos.py          ← Todo 路由（API 端点）
│   └── tests/
│       └── test_api.py       ← API 单元测试
├── frontend/                 ← 前端 Node.js 静态服务
│   ├── package.json          ← Node 项目配置
│   ├── server.js             ← 静态文件服务器（Express 或 http）
│   ├── public/
│   │   ├── index.html        ← 主页面
│   │   ├── style.css         ← 样式表
│   │   └── app.js            ← 前端交互逻辑
│   └── tests/
│       └── test_ui.js        ← 前端测试（可选）
└── docker-compose.yml        ← 容器编排（可选）
```

---

## 三、API 接口定义

Base URL: `http://localhost:8000/api/v1`

### 3.1 接口一览

| 方法 | 路径 | 描述 | 请求体 | 响应 |
|------|------|------|--------|------|
| `GET` | `/todos` | 获取事项列表 | Query: `?status=&priority=&page=&size=` | `PaginatedResponse<TodoItem>` |
| `GET` | `/todos/{id}` | 获取单个事项 | — | `TodoItem` |
| `POST` | `/todos` | 创建事项 | `TodoCreate` | `TodoItem` (201) |
| `PUT` | `/todos/{id}` | 更新事项 | `TodoUpdate` | `TodoItem` |
| `DELETE` | `/todos/{id}` | 删除事项 | — | `{message: "deleted"}` (200) |
| `GET` | `/health` | 健康检查 | — | `{status: "ok"}` |

### 3.2 请求/响应 Schema 详细定义

#### TodoCreate（创建请求）
```json
{
    "title": "string (必填，1-200字符)",
    "description": "string (可选，最大2000字符，默认空字符串)",
    "priority": "enum: low | medium | high (默认 medium)",
    "status": "enum: todo | in_progress | done (默认 todo)"
}
```

#### TodoUpdate（更新请求，所有字段可选）
```json
{
    "title": "string (可选，1-200字符)",
    "description": "string (可选，最大2000字符)",
    "priority": "enum: low | medium | high (可选)",
    "status": "enum: todo | in_progress | done (可选)"
}
```

#### TodoItem（响应）
```json
{
    "id": 1,
    "title": "完成项目报告",
    "description": "整理Q2项目数据并撰写报告",
    "priority": "high",
    "status": "in_progress",
    "created_at": "2026-06-29T10:00:00",
    "updated_at": "2026-06-29T12:30:00"
}
```

#### PaginatedResponse（分页响应）
```json
{
    "items": [TodoItem, ...],
    "total": 42,
    "page": 1,
    "size": 20,
    "pages": 3
}
```

#### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `status` | string | — | 按状态筛选: `todo`, `in_progress`, `done` |
| `priority` | string | — | 按优先级筛选: `low`, `medium`, `high` |
| `page` | int | 1 | 页码，最小 1 |
| `size` | int | 20 | 每页条数，范围 1-100 |

---

## 四、任务拆分

### 📋 阶段一：项目初始化与环境搭建

---

#### 任务 1.1：创建项目目录结构

- **优先级**: P0（最高）
- **预估工时**: 10 分钟
- **前置依赖**: 无
- **负责人**: code_agent

**功能描述**:  
创建 `/opt/hermes/projects/todo-app/` 下的完整目录结构，包括 `backend/`、`frontend/`、`backend/routers/`、`backend/tests/`、`frontend/public/`、`frontend/tests/`。

**交付物**:
- 完整的空目录结构

**验收标准**:
- [ ] 所有目录均已创建
- [ ] 目录结构符合上述文件结构定义

---

#### 任务 1.2：初始化后端 Python 项目

- **优先级**: P0
- **预估工时**: 15 分钟
- **前置依赖**: 任务 1.1
- **负责人**: code_agent

**功能描述**:  
创建 `backend/requirements.txt`，写入依赖：`fastapi`、`uvicorn[standard]`、`pydantic`。确认 Python 3.9+ 可用。

**交付物**:
- `backend/requirements.txt`
- 已安装的 Python 依赖

**验收标准**:
- [ ] `pip install -r requirements.txt` 成功
- [ ] `uvicorn --version` 正常
- [ ] `python -c "import fastapi"` 无报错

---

#### 任务 1.3：初始化前端 Node.js 项目

- **优先级**: P0
- **预估工时**: 15 分钟
- **前置依赖**: 任务 1.1
- **负责人**: code_agent

**功能描述**:  
创建 `frontend/package.json`，配置项目名 `todo-app-frontend`。运行 `npm install`。

**交付物**:
- `frontend/package.json`
- `frontend/node_modules/`（安装后）

**验收标准**:
- [ ] `npm install` 成功
- [ ] Node.js 版本 >= 16

---

### 📋 阶段二：后端 API 开发

---

#### 任务 2.1：数据库层 — SQLite 表创建

- **优先级**: P0
- **预估工时**: 30 分钟
- **前置依赖**: 任务 1.2
- **负责人**: code_agent
- **文件**: `backend/database.py`

**功能描述**:  
使用 Python 内置 `sqlite3` 模块，建立数据库连接。创建 `todos` 表，字段对齐数据模型定义。包含 `created_at` 和 `updated_at` 的默认值及自动更新逻辑（使用触发器）。数据库文件存储在 `backend/todo.db`。

**建表 SQL 参考**:
```sql
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK(length(title) >= 1 AND length(title) <= 200),
    description TEXT DEFAULT '' CHECK(length(description) <= 2000),
    priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high')),
    status TEXT NOT NULL DEFAULT 'todo' CHECK(status IN ('todo', 'in_progress', 'done')),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TRIGGER IF NOT EXISTS update_todo_timestamp
    AFTER UPDATE ON todos
    FOR EACH ROW
BEGIN
    UPDATE todos SET updated_at = datetime('now') WHERE id = OLD.id;
END;
```

**验收标准**:
- [ ] 数据库文件 `backend/todo.db` 自动创建
- [ ] `todos` 表结构正确
- [ ] `updated_at` 触发器正常工作
- [ ] CHECK 约束生效

---

#### 任务 2.2：Pydantic 模型定义

- **优先级**: P0
- **预估工时**: 25 分钟
- **前置依赖**: 任务 2.1
- **负责人**: code_agent
- **文件**: `backend/models.py`, `backend/schemas.py`

**功能描述**:  
定义 Pydantic 数据模型。

**`models.py` — 数据库行模型**:
- `TodoItem`: 包含所有字段的完整模型

**`schemas.py` — 请求/响应 Schema**:
- `TodoCreate`: 创建请求，`title` 必填，其他可选且有默认值
- `TodoUpdate`: 更新请求，所有字段可选（`Optional`）
- `TodoResponse`: API 响应模型
- `PaginatedResponse`: 泛型分页响应，包含 `items`, `total`, `page`, `size`, `pages`
- `PriorityEnum`: `Literal["low", "medium", "high"]`
- `StatusEnum`: `Literal["todo", "in_progress", "done"]`

**验收标准**:
- [ ] 所有 Schema 可通过 Pydantic 验证
- [ ] `TodoCreate` 正确处理默认值
- [ ] `TodoUpdate` 支持部分更新
- [ ] 枚举值校验生效

---

#### 任务 2.3：CRUD 数据库操作层

- **优先级**: P0
- **预估工时**: 45 分钟
- **前置依赖**: 任务 2.1, 2.2
- **负责人**: code_agent
- **文件**: `backend/crud.py`

**功能描述**:  
实现所有数据库 CRUD 操作函数。

**函数清单**:

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `get_todos(db, status, priority, page, size)` | 筛选条件 + 分页 | `(items: list, total: int)` | 获取分页列表，支持筛选 |
| `get_todo_by_id(db, todo_id)` | id | `dict 或 None` | 根据 ID 获取单个事项 |
| `create_todo(db, todo: TodoCreate)` | TodoCreate | `dict` (含 id, timestamps) | 创建事项，返回完整记录 |
| `update_todo(db, todo_id, todo: TodoUpdate)` | id, TodoUpdate | `dict 或 None` | 部分更新，只更新传入字段 |
| `delete_todo(db, todo_id)` | id | `bool` | 删除事项，返回是否成功 |

**关键实现细节**:
- `get_todos`: 动态构建 SQL WHERE 子句，支持按 `status` 和 `priority` 筛选；使用 `LIMIT` 和 `OFFSET` 分页
- `create_todo`: 参数化查询；INSERT 后通过 `lastrowid` 获取新 ID，再 SELECT 返回完整记录
- `update_todo`: 使用 `model_dump(exclude_unset=True)` 获取仅用户传入的字段；动态构建 SET 子句
- `delete_todo`: 执行 `DELETE FROM todos WHERE id = ?`，返回 `rowcount > 0`
- 所有 SQL 操作均使用参数化查询（`?` 占位符）

**验收标准**:
- [ ] 创建事项后能正确返回包含 id 和时间戳的完整记录
- [ ] 分页参数正确
- [ ] 筛选功能正确
- [ ] 更新不存在的 ID 返回 None
- [ ] 更新仅修改传入字段
- [ ] 删除不存在的 ID 返回 False
- [ ] 所有 SQL 使用参数化查询

---

#### 任务 2.4：API 路由定义

- **优先级**: P0
- **预估工时**: 40 分钟
- **前置依赖**: 任务 2.3
- **负责人**: code_agent
- **文件**: `backend/routers/todos.py`

**功能描述**:  
定义所有 RESTful API 端点，使用 FastAPI 的 `APIRouter`。

**端点实现**:

| # | 方法 | 路径 | 说明 |
|---|------|------|------|
| 1 | `GET` | `/api/v1/todos` | 获取事项列表，支持筛选和分页 |
| 2 | `GET` | `/api/v1/todos/{todo_id}` | 获取单个事项，不存在返回 404 |
| 3 | `POST` | `/api/v1/todos` | 创建事项，返回 201 |
| 4 | `PUT` | `/api/v1/todos/{todo_id}` | 更新事项，不存在返回 404 |
| 5 | `DELETE` | `/api/v1/todos/{todo_id}` | 删除事项，不存在返回 404 |

**验收标准**:
- [ ] 所有端点可访问
- [ ] 请求/响应格式正确
- [ ] 不存在的 ID 返回 404
- [ ] 参数校验生效（无效参数返回 422）
- [ ] Swagger UI 可在 `/docs` 访问

---

#### 任务 2.5：应用入口 & CORS 配置

- **优先级**: P0
- **预估工时**: 20 分钟
- **前置依赖**: 任务 2.4
- **负责人**: code_agent
- **文件**: `backend/main.py`

**功能描述**:  
创建 FastAPI 应用实例，配置 CORS 中间件，挂载路由，添加健康检查端点。

**实现细节**:
- `app = FastAPI(title="Todo App API", version="1.0.0")`
- CORS: 允许 `http://localhost:3000`，允许所有方法和头
- `app.include_router(todos.router, prefix="/api/v1")`
- 健康检查: `GET /api/v1/health` → `{"status": "ok", "version": "1.0.0"}`
- 启动事件: `@app.on_event("startup")` 中调用 `database.init_db()`
- `uvicorn.run(app, host="0.0.0.0", port=8000)`

**验收标准**:
- [ ] `python main.py` 启动成功，监听 8000 端口
- [ ] `GET /api/v1/health` 返回 `{"status": "ok"}`
- [ ] `GET /docs` 显示 Swagger UI
- [ ] CORS 头正确

---

#### 任务 2.6：后端 API 测试

- **优先级**: P1（高）
- **预估工时**: 30 分钟
- **前置依赖**: 任务 2.5
- **负责人**: code_agent
- **文件**: `backend/tests/test_api.py`

**功能描述**:  
使用 FastAPI 的 `TestClient` 编写 API 集成测试。

**测试用例**:

| 编号 | 用例 | 预期结果 |
|------|------|----------|
| TC-01 | 健康检查 | 200, `{"status": "ok"}` |
| TC-02 | 创建事项（正常） | 201, 返回完整 TodoItem |
| TC-03 | 创建事项（缺少 title） | 422 |
| TC-04 | 创建事项（空 title） | 422 |
| TC-05 | 创建事项（无效 priority） | 422 |
| TC-06 | 获取事项列表（空） | 200, `items: [], total: 0` |
| TC-07 | 获取事项列表（有数据） | 200, 包含已创建的事项 |
| TC-08 | 获取事项列表（按状态筛选） | 200, 仅返回匹配项 |
| TC-09 | 获取事项列表（分页） | 200, 正确分页 |
| TC-10 | 获取单个事项（存在） | 200 |
| TC-11 | 获取单个事项（不存在） | 404 |
| TC-12 | 更新事项（部分字段） | 200, 仅更新指定字段 |
| TC-13 | 更新事项（不存在） | 404 |
| TC-14 | 删除事项（存在） | 200, 再次获取返回 404 |
| TC-15 | 删除事项（不存在） | 404 |

**验收标准**:
- [ ] 所有 15 个测试用例通过

---

### 📋 阶段三：前端界面开发

---

#### 任务 3.1：Node.js 静态文件服务器

- **优先级**: P0
- **预估工时**: 20 分钟
- **前置依赖**: 任务 1.3
- **负责人**: code_agent
- **文件**: `frontend/server.js`

**功能描述**:  
使用 Node.js 内置 `http` 模块搭建静态文件服务器，将 `frontend/public/` 对外提供服务。支持 SPA 回退（所有路由返回 `index.html`）。

**实现细节**:
- 监听 `localhost:3000`
- 静态文件根目录: `frontend/public/`
- 正确处理 MIME 类型
- SPA 回退：不存在的路径返回 `index.html`

**验收标准**:
- [ ] `node server.js` 启动成功，监听 3000 端口
- [ ] 访问 `http://localhost:3000` 返回 `index.html`
- [ ] 静态资源正确加载

---

#### 任务 3.2：主页面 HTML 结构

- **优先级**: P0
- **预估工时**: 30 分钟
- **前置依赖**: 任务 3.1
- **负责人**: code_agent
- **文件**: `frontend/public/index.html`

**功能描述**:  
构建单页应用的主 HTML 结构。

**页面区域**:
1. **顶部标题栏**: "Todo App"
2. **创建表单区**: 标题输入框、描述输入框、优先级下拉选择、提交按钮
3. **事项列表区**: 筛选栏（状态、优先级）和 Todo 卡片列表
4. **编辑弹窗（Modal）**: 编辑已有事项，默认隐藏

**验收标准**:
- [ ] HTML 结构完整，包含所有必要元素
- [ ] 表单元素可交互

---

#### 任务 3.3：CSS 样式设计

- **优先级**: P0
- **预估工时**: 40 分钟
- **前置依赖**: 任务 3.2
- **负责人**: code_agent
- **文件**: `frontend/public/style.css`

**功能描述**:  
设计现代化、响应式的界面样式。

**优先级颜色方案**:

| 优先级 | 颜色 | 色值 |
|--------|------|------|
| high | 红色 | `#E74C3C` |
| medium | 黄色/橙色 | `#F39C12` |
| low | 绿色 | `#27AE60` |

**状态颜色方案**:

| 状态 | 颜色 | 色值 |
|------|------|------|
| todo | 灰色 | `#95A5A6` |
| in_progress | 蓝色 | `#3498DB` |
| done | 绿色 | `#27AE60` |

**核心样式要求**:
- 卡片式设计（白色背景，圆角，阴影）
- 最大内容宽度 800px，居中显示
- 提交按钮使用主题蓝色 `#4A90D9`
- 悬停交互效果
- 移动端响应式适配（< 600px）

**验收标准**:
- [ ] 界面美观，风格统一
- [ ] 优先级和状态颜色正确
- [ ] 交互元素有视觉反馈
- [ ] 移动端布局正常

---

#### 任务 3.4：前端交互逻辑

- **优先级**: P0
- **预估工时**: 60 分钟
- **前置依赖**: 任务 3.3, 2.5（后端 API 可用）
- **负责人**: code_agent
- **文件**: `frontend/public/app.js`

**功能描述**:  
实现完整的前端交互逻辑，使用原生 JavaScript。

**核心模块**:

1. **API 客户端**:
   ```javascript
   const API_BASE = 'http://localhost:8000/api/v1';
   // getTodos, getTodo, createTodo, updateTodo, deleteTodo
   ```

2. **UI 渲染**: `renderTodoList()`, `renderTodoCard()`, `renderPagination()`

3. **事件处理**: 创建/编辑/删除/筛选/分页/状态切换

4. **状态管理**: `state = { todos, filters, pagination, editingTodo }`

5. **工具函数**: `priorityLabel()`, `statusLabel()`, `formatDate()`, `showModal()`, `hideModal()`

**中文本地化**:
- `low → "低"`, `medium → "中"`, `high → "高"`
- `todo → "待办"`, `in_progress → "进行中"`, `done → "已完成"`

**验收标准**:
- [ ] 创建事项后列表即时更新
- [ ] 编辑功能正常
- [ ] 删除功能正常（确认后删除）
- [ ] 筛选功能正常
- [ ] 分页功能正常
- [ ] 空列表显示友好提示
- [ ] 网络错误时显示错误提示

---

### 📋 阶段四：集成测试与验证

---

#### 任务 4.1：端到端集成测试

- **优先级**: P1
- **预估工时**: 30 分钟
- **前置依赖**: 所有前后端任务
- **负责人**: code_agent

**功能描述**:  
验证完整用户流程。

**测试流程**:
1. 启动后端服务
2. 启动前端服务
3. 验证 API 健康检查
4. 通过 API 创建测试数据
5. 验证列表和筛选
6. 验证更新和删除
7. 验证前端页面

**验收标准**:
- [ ] 后端所有 API 端点工作正常
- [ ] 前端页面正确渲染
- [ ] 前后端数据交互正常
- [ ] CRUD 全流程可用

---

#### 任务 4.2：编写 README.md

- **优先级**: P1
- **预估工时**: 15 分钟
- **前置依赖**: 任务 4.1
- **负责人**: code_agent
- **文件**: `README.md`

**功能描述**:  
编写项目说明文档（项目简介、技术栈、项目结构、快速启动指南、API 文档链接、环境要求）。

**验收标准**:
- [ ] README 内容完整
- [ ] 启动步骤可复现

---

## 五、执行顺序与依赖关系

```
阶段一：初始化
├── 1.1 创建目录结构         ← 最先执行
├── 1.2 初始化后端            ← 可与 1.3 并行
└── 1.3 初始化前端            ← 可与 1.2 并行

阶段二：后端开发
├── 2.1 数据库层             ← 依赖 1.2
├── 2.2 Pydantic 模型        ← 依赖 2.1
├── 2.3 CRUD 操作层          ← 依赖 2.1, 2.2
├── 2.4 API 路由             ← 依赖 2.3
├── 2.5 应用入口 & CORS      ← 依赖 2.4
└── 2.6 API 测试             ← 依赖 2.5

阶段三：前端开发
├── 3.1 静态服务器           ← 依赖 1.3
├── 3.2 HTML 结构            ← 依赖 3.1
├── 3.3 CSS 样式             ← 依赖 3.2
├── 3.4 JS 交互逻辑          ← 依赖 3.3, 2.5

阶段四：集成
├── 4.1 E2E 测试             ← 依赖所有前后端任务
└── 4.2 README               ← 依赖 4.1
```

---

## 六、任务统计

| 阶段 | 任务数 | 预估总工时 |
|------|--------|-----------|
| 阶段一：初始化 | 3 | 40 分钟 |
| 阶段二：后端 | 6 | 190 分钟 |
| 阶段三：前端 | 4 | 150 分钟 |
| 阶段四：集成 | 2 | 45 分钟 |
| **合计** | **15** | **~7 小时** |

---

## 七、注意事项

1. **安全性**: 所有 SQL 操作必须使用参数化查询防止注入
2. **错误处理**: 后端 API 需统一错误响应格式，前端需处理网络异常
3. **数据校验**: 前后端均需进行输入校验（后端为主，前端为辅）
4. **编码规范**: Python 使用 PEP8，JavaScript 使用 ES6+ 语法
5. **API 文档**: 后端自动生成 OpenAPI 文档（FastAPI 内置 `/docs`）
6. **数据库**: 使用 SQLite，无需额外安装数据库服务
7. **端口约定**: 后端 8000，前端 3000
8. **前后端分离**: 前端通过 Fetch API 调用后端，无模板渲染

---

> **状态**: ⏳ 待执行  
> **下一步**: 将本任务清单交由 code_agent 按顺序执行各任务
