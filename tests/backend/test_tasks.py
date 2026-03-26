import pytest
from fastapi import status
from datetime import datetime, timedelta


class TestCreateTask:
    def test_create_task_success(self, client, auth_headers):
        response = client.post("/api/tasks/", json={
            "title": "Test Task",
            "description": "A test task",
            "priority": "high",
            "status": "todo",
            "due_date": (datetime.utcnow() + timedelta(days=7)).isoformat()
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "A test task"
        assert data["priority"] == "high"
        assert data["status"] == "todo"
        assert "id" in data

    def test_create_task_minimal(self, client, auth_headers):
        response = client.post("/api/tasks/", json={
            "title": "Minimal Task"
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["priority"] == "medium"
        assert data["status"] == "todo"

    def test_create_task_unauthenticated(self, client):
        response = client.post("/api/tasks/", json={"title": "Test"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_task_empty_title(self, client, auth_headers):
        response = client.post("/api/tasks/", json={
            "title": ""
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestListTasks:
    def _create_tasks(self, client, auth_headers):
        tasks = [
            {"title": "Task 1", "priority": "high", "status": "todo"},
            {"title": "Task 2", "priority": "medium", "status": "in_progress"},
            {"title": "Task 3", "priority": "low", "status": "done"},
            {"title": "Urgent Task", "priority": "high", "status": "todo",
             "due_date": (datetime.utcnow() - timedelta(days=1)).isoformat()},
            {"title": "Future Task", "priority": "medium", "status": "todo",
             "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat()},
        ]
        for t in tasks:
            client.post("/api/tasks/", json=t, headers=auth_headers)

    def test_list_tasks(self, client, auth_headers):
        self._create_tasks(client, auth_headers)
        response = client.get("/api/tasks/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 5

    def test_list_tasks_filter_status(self, client, auth_headers):
        self._create_tasks(client, auth_headers)
        response = client.get("/api/tasks/?status=todo", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(t["status"] == "todo" for t in data)

    def test_list_tasks_filter_priority(self, client, auth_headers):
        self._create_tasks(client, auth_headers)
        response = client.get("/api/tasks/?priority=high", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(t["priority"] == "high" for t in data)

    def test_list_tasks_search(self, client, auth_headers):
        self._create_tasks(client, auth_headers)
        response = client.get("/api/tasks/?search=Urgent", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Urgent Task"

    def test_list_tasks_empty(self, client, auth_headers):
        response = client.get("/api/tasks/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_tasks_isolation(self, client, auth_headers, second_auth_headers):
        # Create task for first user
        client.post("/api/tasks/", json={"title": "User1 Task"}, headers=auth_headers)
        # Second user should not see it
        response = client.get("/api/tasks/", headers=second_auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0


class TestGetTask:
    def test_get_task_success(self, client, auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "My Task"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "My Task"

    def test_get_task_not_found(self, client, auth_headers):
        response = client.get("/api/tasks/9999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_task_other_user(self, client, auth_headers, second_auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "Private"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.get(f"/api/tasks/{task_id}", headers=second_auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateTask:
    def test_update_task_success(self, client, auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "Original"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.put(f"/api/tasks/{task_id}", json={
            "title": "Updated",
            "priority": "high",
            "status": "in_progress"
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated"
        assert data["priority"] == "high"
        assert data["status"] == "in_progress"

    def test_update_task_partial(self, client, auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "Original", "priority": "low"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.put(f"/api/tasks/{task_id}", json={
            "status": "done"
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Original"  # unchanged
        assert data["priority"] == "low"  # unchanged
        assert data["status"] == "done"  # updated

    def test_update_task_not_found(self, client, auth_headers):
        response = client.put("/api/tasks/9999", json={"title": "X"}, headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task_other_user(self, client, auth_headers, second_auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "Mine"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.put(f"/api/tasks/{task_id}", json={"title": "Hacked"}, headers=second_auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteTask:
    def test_delete_task_success(self, client, auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "To Delete"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Verify deleted
        get_resp = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_not_found(self, client, auth_headers):
        response = client.delete("/api/tasks/9999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_other_user(self, client, auth_headers, second_auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "Mine"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.delete(f"/api/tasks/{task_id}", headers=second_auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
