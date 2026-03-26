from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth_router, task_router, dashboard_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo App API",
    description="A To-Do application with JWT authentication, CRUD tasks, and filterable dashboard",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (routers already have /api prefix)
app.include_router(auth_router.router)
app.include_router(task_router.router)
app.include_router(dashboard_router.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Todo App API", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
