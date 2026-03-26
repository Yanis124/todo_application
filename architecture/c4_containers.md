# C4 Model - Level 2: Container Diagram

## To-Do Application - Containers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CONTAINER DIAGRAM                               │
│                                                                         │
│  ┌──────────┐                                                           │
│  │          │                                                           │
│  │   User   │                                                           │
│  │ (Person) │                                                           │
│  │          │                                                           │
│  └────┬─────┘                                                           │
│       │ HTTPS                                                           │
│       ▼                                                                 │
│  ┌─────────────────────────┐                                            │
│  │   React SPA (Frontend)  │                                            │
│  │   [Container: React]    │                                            │
│  │                         │                                            │
│  │  - Login/Register pages │                                            │
│  │  - Task CRUD forms      │                                            │
│  │  - Filterable Dashboard │                                            │
│  │  - JWT token management │                                            │
│  └────────┬────────────────┘                                            │
│           │ HTTP/JSON (REST API)                                        │
│           ▼                                                             │
│  ┌─────────────────────────────────────────┐                            │
│  │   FastAPI Backend (API Server)          │                            │
│  │   [Container: Python/FastAPI]           │                            │
│  │                                         │                            │
│  │  - Auth endpoints (register/login)      │                            │
│  │  - Task CRUD endpoints                  │                            │
│  │  - Filter/search endpoints              │                            │
│  │  - JWT token generation/validation      │                            │
│  │  - Swagger UI (auto-generated)          │                            │
│  │  - Input validation (Pydantic)          │                            │
│  └────────┬────────────────────────────────┘                            │
│           │ SQL (SQLAlchemy ORM)                                        │
│           ▼                                                             │
│  ┌─────────────────────────┐                                            │
│  │   SQLite Database       │                                            │
│  │   [Container: SQLite]   │                                            │
│  │                         │                                            │
│  │  - users table          │                                            │
│  │  - tasks table          │                                            │
│  └─────────────────────────┘                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Container Details

| Container | Technology | Purpose |
|-----------|------------|----------|
| React SPA | React 18 + React Router + Axios | Single-page application for user interaction |
| FastAPI Backend | Python 3.11 + FastAPI + SQLAlchemy + python-jose | REST API server with JWT auth and Swagger docs |
| SQLite Database | SQLite 3 | Persistent data storage for users and tasks |

## Communication Protocols
| From | To | Protocol | Description |
|------|----|----------|-------------|
| User | React SPA | HTTPS | Browser loads SPA |
| React SPA | FastAPI Backend | HTTP/JSON | REST API calls with JWT Bearer token |
| FastAPI Backend | SQLite | SQL via SQLAlchemy | ORM-based database operations |

## Key Design Decisions
1. **SQLite** chosen for simplicity (single-file DB, no server needed)
2. **FastAPI** provides automatic Swagger/OpenAPI documentation
3. **React SPA** communicates exclusively via REST API (decoupled frontend)
4. **JWT tokens** stored in localStorage on the client side
5. **CORS** middleware configured on FastAPI to allow React dev server
