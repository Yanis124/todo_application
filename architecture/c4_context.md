# C4 Model - Level 1: System Context Diagram

## To-Do Application - System Context

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM CONTEXT                            │
│                                                             │
│  ┌──────────┐         ┌──────────────────────┐              │
│  │          │  HTTPS  │                      │              │
│  │   User   │────────>│   To-Do Application  │              │
│  │ (Person) │<────────│   (Software System)  │              │
│  │          │  JSON   │                      │              │
│  └──────────┘         └──────────────────────┘              │
│                                                             │
│  Description:                                               │
│  - User authenticates via JWT                               │
│  - User manages tasks (CRUD)                                │
│  - User views filterable dashboard                          │
│  - User interacts via React SPA                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Actors
| Actor | Description |
|-------|-------------|
| User  | End user who registers, logs in, and manages their personal to-do tasks |

## External Systems
| System | Description |
|--------|-------------|
| None   | Self-contained application with no external dependencies |

## Key Interactions
1. User registers/logs in → receives JWT token
2. User creates, reads, updates, deletes tasks
3. User filters tasks by priority, status, due date
4. API documentation available via Swagger UI
