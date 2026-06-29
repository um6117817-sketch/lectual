# Todo App — 待办事项管理应用

一个简单的待办事项管理应用，支持创建、查看、编辑、删除待办事项。前后端分离架构。

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | Python 3.11 + FastAPI + SQLite |
| 前端 | Node.js + 原生 HTML/CSS/JS |

## 项目结构

```
todo-app/
├── TASKS.md
├── README.md
├── backend/
│   ├── requirements.txt
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routers/todos.py
│   └── tests/test_api.py
└── frontend/
    ├── package.json
    ├── server.js
    └── public/
        ├── index.html
        ├── style.css
        └── app.js
```

## 快速启动

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

后端运行在 http://localhost:8000，API 文档 http://localhost:8000/docs

### 2. 启动前端

```bash
cd frontend
npm install
node server.js
```

前端运行在 http://localhost:3000

### 3. 运行测试

```bash
cd backend
python -m pytest tests/ -v
```

## API 接口

Base URL: `http://localhost:8000/api/v1`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /todos | 获取事项列表（支持分页和筛选） |
| GET | /todos/{id} | 获取单个事项 |
| POST | /todos | 创建事项 |
| PUT | /todos/{id} | 更新事项 |
| DELETE | /todos/{id} | 删除事项 |
| GET | /health | 健康检查 |

查询参数：status（todo/in_progress/done）、priority（low/medium/high）、page、size

## 环境要求

- Python >= 3.9
- Node.js >= 16
