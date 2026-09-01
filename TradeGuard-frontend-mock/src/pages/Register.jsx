import React, { useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', username: '', email: '', password: '', address: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const update = field => event => setForm({ ...form, [field]: event.target.value })

  const submit = async event => {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await register(form)
      window.alert('Account created successfully.')
      navigate('/login')
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="auth-body">
      <div className="auth-card">
        <h1>Create Account</h1>
        <form onSubmit={submit}>
          <label htmlFor="name">Full Name</label>
          <input id="name" value={form.name} onChange={update('name')} required />
          <label htmlFor="email">Email</label>
          <input id="email" type="email" value={form.email} onChange={update('email')} required />
          <label htmlFor="username">Username</label>
          <input id="username" value={form.username} onChange={update('username')} required />
          <label htmlFor="password">Password</label>
          <input id="password" type="password" value={form.password} onChange={update('password')} required />
          {error && <p className="form-error">{error}</p>}
          <button className="primary-btn" type="submit" disabled={submitting}>
            {submitting ? 'Creating…' : 'Register'}
          </button>
        </form>
        <p className="auth-link">
          Already have an account? <NavLink to="/login">Login</NavLink>
        </p>
      </div>
    </main>
  )
}
