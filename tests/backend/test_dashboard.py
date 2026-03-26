import pytest
from fastapi import status
from datetime import datetime, timedelta


class TestDashboard:
    def _create_tasks(self, client, auth_headers):
        tasks = [
            {"title": "Task 1", "priority": "high", "status": "todo"},
            {"title": "Task 2", "priority": "medium", "status": "in_progress"},
            {"title": "Task 3", "priority": "low", "status": "done"},
            {"title": "Task 4", "priority": "high", "status": "todo",
             "due_date": (datetime.utcnow() - timedelta(days=1)).isoformat()},
            {"title": "Task 5", "priority": "medium", "status": "todo",
             "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat()},
        ]
        for t in tasks:
            client.post("/api/tasks/", json=t, headers=auth_headers)

    def test_dashboard_stats(self, client, auth_headers):
        self._create_tasks(client, auth_headers)
        response = client.get("/api/dashboard/stats", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_tasks"] == 5
        assert data["todo_count"] == 3
        assert data["in_progress_count"] == 1
        assert data["done_count"] == 1
        assert data["overdue_count"] == 1
        assert data["high_priority_count"] == 2

    def test_dashboard_empty(self, client, auth_headers):
        response = client.get("/api/dashboard/stats", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_tasks"] == 0
        assert data["todo_count"] == 0
        assert data["in_progress_count"] == 0
        assert data["done_count"] == 0
        assert data["overdue_count"] == 0
        assert data["high_priority_count"] == 0

    def test_dashboard_unauthenticated(self, client):
        response = client.get("/api/dashboard/stats")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_dashboard_isolation(self, client, auth_headers, second_auth_headers):
        # Create tasks for first user
        self._create_tasks(client, auth_headers)
        # Second user should see empty stats
        response = client.get("/api/dashboard/stats", headers=second_auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_tasks"] == 0
