import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { authAPI } from '../api'

function Register({ onLogin }) {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await authAPI.register({ username, email, password })
      // Auto-login after registration using email
      const res = await authAPI.login({ email, password })
      onLogin(res.data.access_token)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <div className="auth-form">
      <h2>Register</h2>
      {error && <div className="error-msg">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="text" placeholder="Username" value={username}
          onChange={(e) => setUsername(e.target.value)} required
        />
        <input
          type="email" placeholder="Email" value={email}
          onChange={(e) => setEmail(e.target.value)} required
        />
        <input
          type="password" placeholder="Password (min 6 chars)" value={password}
          onChange={(e) => setPassword(e.target.value)} required
        />
        <button type="submit">Register</button>
      </form>
      <div className="toggle">
        Already have an account? <Link to="/login">Login</Link>
      </div>
    </div>
  )
}

export default Register
