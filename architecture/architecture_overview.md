# Architecture Overview - To-Do Application

## 1. Architecture Style
**Client-Server with REST API** — A decoupled React SPA communicates with a FastAPI backend via RESTful JSON endpoints. Authentication is stateless using JWT tokens.

## 2. Technology Stack
| Layer | Technology | Justification |
|-------|-----------|---------------|
| Frontend | React 18 + Vite | Modern SPA framework, fast dev experience |
| Backend | FastAPI (Python 3.11) | Auto Swagger docs, async support, Pydantic validation |
| ORM | SQLAlchemy 2.0 | Mature ORM, excellent SQLite support |
| Database | SQLite | Zero-config, file-based, perfect for single-server deployment |
| Auth | JWT (python-jose) + bcrypt (passlib) | Stateless auth, industry standard |
| HTTP Client | Axios | Interceptors for JWT, clean API |

## 3. Architecture Layers (Backend)

### 3.1 API Layer (Routers)
- `auth_router` — `/api/auth/register`, `/api/auth/login`, `/api/auth/me`
- `task_router` — `/api/tasks/` CRUD + filtering
- `health_router` — `/api/health`

### 3.2 Service Layer
- `AuthService` — Business logic for user registration, authentication
- `TaskService` — Business logic for task CRUD and filtering

### 3.3 Security Layer
- `JWTManager` — Token creation and validation
- `PasswordHasher` — bcrypt hashing and verification
- `get_current_user` — FastAPI dependency for route protection

### 3.4 Data Layer
- `User` model — SQLAlchemy ORM model for users table
- `Task` model — SQLAlchemy ORM model for tasks table
- `database.py` — Engine, session factory, `get_db` dependency

### 3.5 Schema Layer (Pydantic)
- Request/Response validation schemas for all endpoints
- Enums: `PriorityEnum` (low/medium/high/urgent), `StatusEnum` (todo/in_progress/done/cancelled)

### 3.6 Config Layer
- `Settings` class using pydantic-settings for environment variable management

## 4. Architecture Layers (Frontend)

### 4.1 Pages
- `LoginPage` — Email/password login form
- `RegisterPage` — Registration form
- `DashboardPage` — Main view with task list, filters, and create form

### 4.2 Components
- `TaskList` — Renders collection of TaskCard components
- `TaskCard` — Individual task display with edit/delete actions
- `TaskForm` — Create/edit task form (title, description, priority, status, due date)
- `TaskFilter` — Filter controls (priority, status, date range, search text)
- `ProtectedRoute` — HOC that redirects unauthenticated users to login
- `Navbar` — Top navigation with user info and logout button

### 4.3 Services/Hooks
- `apiClient` — Axios instance with base URL and JWT interceptor
- `useAuth()` — React Context hook for authentication state
- `useTasks()` — Custom hook for task data management

### 4.4 State Management
- `AuthContext` — React Context for global auth state (user, token, login/logout/register)

## 5. Data Flow

### Authentication Flow
```
User → LoginPage → POST /api/auth/login → JWT Token
     → Store token in localStorage
     → All subsequent requests include Authorization: Bearer <token>
     → Backend validates token via get_current_user dependency
```

### Task CRUD Flow
```
DashboardPage → useTasks() → apiClient → GET /api/tasks/?priority=high&status=todo
             → TaskService.get_tasks() → SQLAlchemy query with filters
             → Return List[TaskResponse] → Render TaskList → TaskCards
```

## 6. Security Considerations
- Passwords hashed with bcrypt (never stored in plain text)
- JWT tokens expire after 30 minutes (configurable)
- All task endpoints require authentication
- Users can only access their own tasks (owner_id check)
- CORS configured to allow only specific origins
- Input validation via Pydantic schemas on all endpoints

## 7. Key Design Decisions (ADR Summary)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ADR-001: Database | SQLite | Simplicity, no server needed, sufficient for single-user/small team |
| ADR-002: Auth | JWT (stateless) | No session storage needed, scales horizontally |
| ADR-003: API Style | REST | Simple CRUD operations, well-supported by FastAPI |
| ADR-004: Frontend State | React Context | Sufficient for auth state; no Redux needed for this scale |
| ADR-005: Password Hashing | bcrypt via passlib | Industry standard, built-in salt |
| ADR-006: API Documentation | Swagger (auto) | FastAPI generates OpenAPI docs automatically |
| ADR-007: Service Layer | Class-based services | Testable, separates business logic from routes |

## 8. Deployment Architecture
```
┌─────────────────────────────────────────┐
│           Docker Compose                │
│                                         │
│  ┌──────────────┐  ┌──────────────────┐ │
│  │  Frontend     │  │  Backend         │ │
│  │  (nginx:3000) │──│  (uvicorn:8000)  │ │
│  └──────────────┘  └────────┬─────────┘ │
│                             │            │
│                    ┌────────┴─────────┐  │
│                    │  SQLite (volume)  │  │
│                    └──────────────────┘  │
└─────────────────────────────────────────┘
```
