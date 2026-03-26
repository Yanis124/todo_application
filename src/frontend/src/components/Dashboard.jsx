import React, { useState, useEffect, useCallback } from 'react'
import { dashboardAPI, tasksAPI } from '../api'
import TaskModal from './TaskModal'

function Dashboard({ onLogout }) {
  const [stats, setStats] = useState(null)
  const [tasks, setTasks] = useState([])
  const [filters, setFilters] = useState({ status: '', priority: '', search: '' })
  const [showModal, setShowModal] = useState(false)
  const [editingTask, setEditingTask] = useState(null)

  const loadStats = useCallback(async () => {
    try {
      const res = await dashboardAPI.getStats()
      setStats(res.data)
    } catch (err) {
      console.error('Failed to load stats', err)
    }
  }, [])

  const loadTasks = useCallback(async () => {
    try {
      const params = {}
      if (filters.status) params.status = filters.status
      if (filters.priority) params.priority = filters.priority
      if (filters.search) params.search = filters.search
      const res = await tasksAPI.list(params)
      setTasks(res.data)
    } catch (err) {
      console.error('Failed to load tasks', err)
    }
  }, [filters])

  useEffect(() => { loadStats() }, [loadStats])
  useEffect(() => { loadTasks() }, [loadTasks])

  const handleSaveTask = async (taskData) => {
    try {
      if (editingTask) {
        await tasksAPI.update(editingTask.id, taskData)
      } else {
        await tasksAPI.create(taskData)
      }
      setShowModal(false)
      setEditingTask(null)
      loadTasks()
      loadStats()
    } catch (err) {
      console.error('Failed to save task', err)
    }
  }

  const handleDeleteTask = async (id) => {
    if (!window.confirm('Delete this task?')) return
    try {
      await tasksAPI.delete(id)
      loadTasks()
      loadStats()
    } catch (err) {
      console.error('Failed to delete task', err)
    }
  }

  const handleEdit = (task) => {
    setEditingTask(task)
    setShowModal(true)
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return new Date(dateStr).toLocaleDateString()
  }

  return (
    <div>
      <div className="navbar">
        <h1>📋 Todo App</h1>
        <button onClick={onLogout}>Logout</button>
      </div>
      <div className="container">
        {stats && (
          <div className="dashboard-stats">
            <div className="stat-card">
              <div className="number">{stats.total_tasks}</div>
              <div className="label">Total Tasks</div>
            </div>
            <div className="stat-card">
              <div className="number">{stats.todo_count}</div>
              <div className="label">To Do</div>
            </div>
            <div className="stat-card">
              <div className="number">{stats.in_progress_count}</div>
              <div className="label">In Progress</div>
            </div>
            <div className="stat-card">
              <div className="number">{stats.done_count}</div>
              <div className="label">Done</div>
            </div>
            <div className="stat-card">
              <div className="number">{stats.overdue_count}</div>
              <div className="label">Overdue</div>
            </div>
            <div className="stat-card">
              <div className="number">{stats.high_priority_count}</div>
              <div className="label">High Priority</div>
            </div>
          </div>
        )}

        <button className="add-task-btn" onClick={() => { setEditingTask(null); setShowModal(true) }}>
          + Add Task
        </button>

        <div className="filters">
          <select value={filters.status} onChange={(e) => setFilters({...filters, status: e.target.value})}>
            <option value="">All Statuses</option>
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
          <select value={filters.priority} onChange={(e) => setFilters({...filters, priority: e.target.value})}>
            <option value="">All Priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          <input
            type="text" placeholder="Search tasks..."
            value={filters.search}
            onChange={(e) => setFilters({...filters, search: e.target.value})}
          />
        </div>

        <div className="task-list">
          {tasks.length === 0 && <p>No tasks found.</p>}
          {tasks.map((task) => (
            <div key={task.id} className="task-card">
              <div className="task-info">
                <h3>{task.title}</h3>
                <p>{task.description}</p>
                {task.due_date && <p>Due: {formatDate(task.due_date)}</p>}
              </div>
              <div className="task-meta">
                <span className={`badge ${task.priority}`}>{task.priority}</span>
                <span className={`badge ${task.status}`}>{task.status.replace('_', ' ')}</span>
                <div className="task-actions">
                  <button onClick={() => handleEdit(task)}>Edit</button>
                  <button className="delete" onClick={() => handleDeleteTask(task.id)}>Delete</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {showModal && (
        <TaskModal
          task={editingTask}
          onSave={handleSaveTask}
          onClose={() => { setShowModal(false); setEditingTask(null) }}
        />
      )}
    </div>
  )
}

export default Dashboard
