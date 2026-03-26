import axios from 'axios'

const API_BASE = '/api'

const api = axios.create({
  baseURL: API_BASE,
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
}

// Tasks API
export const tasksAPI = {
  list: (params) => api.get('/tasks/', { params }),
  create: (data) => api.post('/tasks/', data),
  get: (id) => api.get(`/tasks/${id}`),
  update: (id, data) => api.put(`/tasks/${id}`, data),
  delete: (id) => api.delete(`/tasks/${id}`),
}

// Dashboard API
export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
}

export default api
