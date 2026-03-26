import React, { useState } from 'react'

function TaskModal({ task, onSave, onClose }) {
  const [title, setTitle] = useState(task?.title || '')
  const [description, setDescription] = useState(task?.description || '')
  const [priority, setPriority] = useState(task?.priority || 'medium')
  const [status, setStatus] = useState(task?.status || 'todo')
  const [dueDate, setDueDate] = useState(
    task?.due_date ? task.due_date.slice(0, 16) : ''
  )

  const handleSubmit = (e) => {
    e.preventDefault()
    const data = { title, description, priority, status }
    if (dueDate) data.due_date = new Date(dueDate).toISOString()
    onSave(data)
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>{task ? 'Edit Task' : 'New Task'}</h2>
        <form onSubmit={handleSubmit}>
          <label>Title</label>
          <input
            type="text" value={title}
            onChange={(e) => setTitle(e.target.value)} required
          />
          <label>Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          <label>Priority</label>
          <select value={priority} onChange={(e) => setPriority(e.target.value)}>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <label>Status</label>
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
          <label>Due Date</label>
          <input
            type="datetime-local" value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
          />
          <div className="modal-actions">
            <button type="button" className="cancel" onClick={onClose}>Cancel</button>
            <button type="submit" className="save">Save</button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default TaskModal
