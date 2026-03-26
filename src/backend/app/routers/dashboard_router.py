from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task, User, TaskStatus, TaskPriority
from app.schemas import DashboardStats
from app.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    base_query = db.query(Task).filter(Task.owner_id == current_user.id)

    total_tasks = base_query.count()
    todo_count = base_query.filter(Task.status == TaskStatus.TODO).count()
    in_progress_count = base_query.filter(Task.status == TaskStatus.IN_PROGRESS).count()
    done_count = base_query.filter(Task.status == TaskStatus.DONE).count()
    overdue_count = base_query.filter(
        Task.due_date < datetime.utcnow(),
        Task.status != TaskStatus.DONE
    ).count()
    high_priority_count = base_query.filter(Task.priority == TaskPriority.HIGH).count()

    return DashboardStats(
        total_tasks=total_tasks,
        todo_count=todo_count,
        in_progress_count=in_progress_count,
        done_count=done_count,
        overdue_count=overdue_count,
        high_priority_count=high_priority_count,
    )
