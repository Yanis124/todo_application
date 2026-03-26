# C4 Model - Level 3: Component Diagram

## FastAPI Backend - Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND - COMPONENTS                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        API Layer (Routers)                          │   │
│  │                                                                     │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ auth_router  │  │ task_router  │  │ health_router            │  │   │
│  │  │              │  │              │  │                          │  │   │
│  │  │ POST /auth/  │  │ GET /tasks/  │  │ GET /health              │  │   │
│  │  │   register   │  │ POST /tasks/ │  │                          │  │   │
│  │  │ POST /auth/  │  │ GET /tasks/  │  └──────────────────────────┘  │   │
│  │  │   login      │  │   {id}       │                                │   │
│  │  │ GET /auth/me │  │ PUT /tasks/  │                                │   │
│  │  │              │  │   {id}       │                                │   │
│  │  │              │  │ DELETE       │                                │   │
│  │  │              │  │   /tasks/{id}│                                │   │
│  │  └──────┬───────┘  └──────┬───────┘                                │   │
│  └─────────┼─────────────────┼────────────────────────────────────────┘   │
│            │                 │                                             │
│            ▼                 ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Service Layer                                  │   │
│  │                                                                     │   │
│  │  ┌──────────────────┐    ┌──────────────────┐                      │   │
│  │  │   AuthService     │    │   TaskService     │                      │   │
│  │  │                  │    │                  │                      │   │
│  │  │ - register_user()│    │ - create_task()  │                      │   │
│  │  │ - login_user()   │    │ - get_tasks()    │                      │   │
│  │  │ - get_current_   │    │ - get_task()     │                      │   │
│  │  │   user()         │    │ - update_task()  │                      │   │
│  │  │ - hash_password()│    │ - delete_task()  │                      │   │
│  │  │ - verify_        │    │ - filter_tasks() │                      │   │
│  │  │   password()     │    │                  │                      │   │
│  │  └──────┬───────────┘    └──────┬───────────┘                      │   │
│  └─────────┼────────────────────────┼─────────────────────────────────┘   │
│            │                        │                                     │
│            ▼                        ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Security Layer                                   │   │
│  │                                                                     │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │  JWTManager                                                  │   │   │
│  │  │  - create_access_token(data, expires_delta)                  │   │   │
│  │  │  - decode_token(token) -> payload                            │   │   │
│  │  │  - get_current_user(token) -> User  [Dependency]             │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │  PasswordHasher                                              │   │   │
│  │  │  - hash(password) -> hashed                                  │   │   │
│  │  │  - verify(plain, hashed) -> bool                             │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Data Layer                                     │   │
│  │                                                                     │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │   │
│  │  │  User Model       │  │  Task Model       │  │  Database        │  │   │
│  │  │  (SQLAlchemy)     │  │  (SQLAlchemy)     │  │  (engine/session)│  │   │
│  │  │                  │  │                  │  │                  │  │   │
│  │  │  - id (PK)       │  │  - id (PK)       │  │  - engine        │  │   │
│  │  │  - email (unique)│  │  - title         │  │  - SessionLocal  │  │   │
│  │  │  - username      │  │  - description   │  │  - get_db()      │  │   │
│  │  │  - hashed_       │  │  - priority      │  │  - Base          │  │   │
│  │  │    password      │  │  - status        │  │  - create_tables │  │   │
│  │  │  - created_at    │  │  - due_date      │  │                  │  │   │
│  │  │                  │  │  - owner_id (FK) │  │                  │  │   │
│  │  │                  │  │  - created_at    │  │                  │  │   │
│  │  │                  │  │  - updated_at    │  │                  │  │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Schema Layer (Pydantic)                           │   │
│  │                                                                     │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │   │
│  │  │  UserCreate      │  │  TaskCreate      │  │  Token           │  │   │
│  │  │  UserResponse    │  │  TaskUpdate      │  │  TokenData       │  │   │
│  │  │  UserLogin       │  │  TaskResponse    │  │                  │  │   │
│  │  │                  │  │  TaskFilter      │  │                  │  │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Config Layer                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │  Settings (pydantic-settings)                                │   │   │
│  │  │  - SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES       │   │   │
│  │  │  - DATABASE_URL, CORS_ORIGINS                                │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## React SPA - Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     REACT SPA - COMPONENTS                                 │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Pages                                        │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ LoginPage    │  │ RegisterPage │  │ DashboardPage            │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     UI Components                                   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ TaskList     │  │ TaskForm     │  │ TaskFilter               │  │   │
│  │  │ TaskCard     │  │ TaskEditModal│  │ (priority/status/date)   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Services / Hooks                                │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ apiClient    │  │ useAuth()    │  │ useTasks()               │  │   │
│  │  │ (Axios)      │  │ (context)    │  │ (hook)                   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     State Management                                │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │ AuthContext (React Context)                                  │   │   │
│  │  │ - user, token, login(), logout(), register()                 │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Interactions

| From | To | Method | Description |
|------|----|--------|-------------|
| auth_router | AuthService | Function call | Delegates auth logic |
| task_router | TaskService | Function call | Delegates task CRUD |
| AuthService | JWTManager | Function call | Token creation/validation |
| AuthService | PasswordHasher | Function call | Password hashing/verification |
| AuthService | User Model | SQLAlchemy query | User CRUD operations |
| TaskService | Task Model | SQLAlchemy query | Task CRUD operations |
| Routers | get_current_user | FastAPI Depends | JWT auth dependency injection |
| React Pages | apiClient | Import | HTTP requests to backend |
| React Pages | useAuth | Hook | Authentication state |
| React Pages | useTasks | Hook | Task data management |
