# Todo App - DevOps Guide

A full-stack To-Do application with JWT authentication, CRUD tasks, filterable dashboard, and Swagger API documentation.

**Stack:** FastAPI + SQLite + React 18 + Vite

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Quick Start with Docker](#quick-start-with-docker)
4. [Manual Setup (Development)](#manual-setup-development)
5. [Running Tests](#running-tests)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Environment Variables](#environment-variables)
8. [API Documentation](#api-documentation)

---

## Prerequisites

- **Docker** >= 24.0 and **Docker Compose** >= 2.20 (for containerized setup)
- **Python** >= 3.11 (for local backend development)
- **Node.js** >= 20.x and **npm** >= 10.x (for local frontend development)
- **Git** >= 2.40

---

## Project Structure

```
.
├── src/
│   ├── backend/              # FastAPI backend (Python)
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py       # Application entry point (FastAPI app)
│   │   │   ├── models.py     # SQLAlchemy models (User, Task)
│   │   │   ├── schemas.py    # Pydantic schemas
│   │   │   ├── database.py   # Database configuration (SQLite + SQLAlchemy)
│   │   │   ├── auth.py       # JWT authentication (bcrypt + python-jose)
│   │   │   ├── config.py     # Settings (pydantic-settings)
│   │   │   └── routers/
│   │   │       ├── auth_router.py
│   │   │       ├── task_router.py
│   │   │       └── dashboard_router.py
│   │   └── requirements.txt
│   └── frontend/             # React + Vite frontend
│       ├── index.html
│       ├── package.json
│       ├── vite.config.js
│       └── src/
│           ├── main.jsx
│           ├── App.jsx
│           ├── api.js
│           ├── index.css
│           └── components/
│               ├── Login.jsx
│               ├── Register.jsx
│               ├── Dashboard.jsx
│               └── TaskModal.jsx
├── tests/
│   └── backend/              # Backend pytest tests
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_tasks.py
│       ├── test_dashboard.py
│       └── test_root.py
├── devops/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml
│   ├── nginx.conf
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── .github/workflows/ci.yml
│   └── README.md             # This file
```

---

## Quick Start with Docker

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-root>
```

### 2. Configure environment variables

```bash
# Create a .env file in the devops/ directory
cp devops/.env.example devops/.env

# Or create manually:
cat > devops/.env << 'EOF'
SECRET_KEY=your-super-secret-key-change-this
DATABASE_URL=sqlite:///./data/todo.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
EOF
```

### 3. Build and start all services

```bash
cd devops
docker compose up --build -d
```

### 4. Verify services are running

```bash
# Check container status
docker compose ps

# Backend health check
curl http://localhost:8000/health

# Frontend health check
curl http://localhost:3000
```

### 5. Access the application

| Service          | URL                          |
|------------------|------------------------------|
| Frontend (React) | http://localhost:3000         |
| Backend API      | http://localhost:8000/api/    |
| Swagger Docs     | http://localhost:8000/docs    |
| ReDoc            | http://localhost:8000/redoc   |

### 6. Stop all services

```bash
cd devops
docker compose down

# To also remove volumes (database data):
docker compose down -v
```

---

## Manual Setup (Development)

### Backend Setup

```bash
# 1. Create and activate virtual environment
python -m venv venv

# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r devops/requirements.txt

# 3. Set environment variables
export SECRET_KEY="dev-secret-key"
export DATABASE_URL="sqlite:///./todo.db"
export ACCESS_TOKEN_EXPIRE_MINUTES=30
export ALGORITHM="HS256"

# 4. Run the backend server
cd src/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000
Swagger docs at http://localhost:8000/docs

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd src/frontend

# 2. Install dependencies
npm install

# 3. Start Vite development server
npm run dev
```

The frontend will be available at http://localhost:3000
Vite proxy is configured to forward `/api` requests to `http://localhost:8000`.

---

## Running Tests

### Backend Tests

```bash
# Activate virtual environment first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install test dependencies
pip install -r devops/requirements.txt

# Run all backend tests from project root
cd src/backend
python -m pytest ../../tests/backend/ -v

# Run with coverage report
python -m pytest ../../tests/backend/ -v --cov=app --cov-report=term-missing --cov-report=html

# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Frontend Tests

```bash
cd src/frontend

# Run tests (if test runner is configured)
npm test
```

> Note: The frontend currently uses Vite. To add testing, install vitest:
> `npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom`
> Then add to package.json scripts: `"test": "vitest run"`

### Run All Tests via Docker

```bash
# Backend tests in container
docker compose -f devops/docker-compose.yml run --rm backend \
  python -m pytest /app/tests/ -v --cov=/app/app --cov-report=term-missing
```

---

## CI/CD Pipeline

The CI/CD pipeline is defined in `devops/.github/workflows/ci.yml` and runs on GitHub Actions.

### Pipeline Stages

1. **Backend Tests** — Installs Python deps, runs pytest with coverage
2. **Frontend Build** — Installs Node deps, builds production bundle with Vite
3. **Docker Build** — Builds both Docker images and tests docker-compose startup

### Triggers

- **Push** to `main` or `develop` branches
- **Pull requests** targeting `main`

### To use the CI pipeline:

```bash
# Copy the workflow file to your repo root
mkdir -p .github/workflows
cp devops/.github/workflows/ci.yml .github/workflows/ci.yml

# Commit and push
git add .github/workflows/ci.yml
git commit -m "Add CI/CD pipeline"
git push origin main
```

---

## Environment Variables

| Variable                     | Description                        | Default                              | Required |
|------------------------------|------------------------------------|--------------------------------------|----------|
| `SECRET_KEY`                 | JWT signing secret key             | `super-secret-key-change-in-production` | Yes      |
| `DATABASE_URL`               | SQLite connection string           | `sqlite:///./todo.db`                | Yes      |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| JWT token expiration in minutes    | `30`                                 | No       |
| `ALGORITHM`                  | JWT signing algorithm              | `HS256`                              | No       |

---

## API Documentation

Once the backend is running, interactive API documentation is available:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key API Endpoints

| Method | Endpoint              | Description                  | Auth Required |
|--------|-----------------------|------------------------------|---------------|
| POST   | `/api/auth/register`  | Register a new user          | No            |
| POST   | `/api/auth/login`     | Login and get JWT token      | No            |
| GET    | `/api/auth/me`        | Get current user profile     | Yes           |
| GET    | `/api/tasks/`         | List all tasks (filterable)  | Yes           |
| POST   | `/api/tasks/`         | Create a new task            | Yes           |
| GET    | `/api/tasks/{id}`     | Get task by ID               | Yes           |
| PUT    | `/api/tasks/{id}`     | Update a task                | Yes           |
| DELETE | `/api/tasks/{id}`     | Delete a task                | Yes           |
| GET    | `/api/dashboard/stats`| Dashboard summary stats      | Yes           |
| GET    | `/health`             | Health check                 | No            |

### Task Filters (query parameters on GET /api/tasks/)

- `status` — Filter by status (`todo`, `in_progress`, `done`)
- `priority` — Filter by priority (`low`, `medium`, `high`)
- `due_before` — Filter tasks due before a date (ISO format)
- `due_after` — Filter tasks due after a date (ISO format)
- `search` — Search in title and description

---

## Troubleshooting

### Port already in use

```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or change ports in docker-compose.yml
```

### Database reset

```bash
# Remove SQLite database
rm -f src/backend/todo.db

# Or with Docker volumes
docker compose -f devops/docker-compose.yml down -v
```

### Rebuild containers from scratch

```bash
cd devops
docker compose down -v --rmi all
docker compose up --build -d
```
