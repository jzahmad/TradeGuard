import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext'

export default function Header() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div>
        <div className="brand">Trade<span>Guard</span></div>
        <div className="brand-subtitle">Trade Order &amp; Risk Management</div>
      </div>
      <div className="nav-right">
        <div className="market-status"><span className="status-dot" />Market Open</div>
        <div className="nav-links">
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/orders">Orders</NavLink>
          {user?.role === 'ADMIN' && <NavLink to="/admin">Admin</NavLink>}
          <a href="#" onClick={e => { e.preventDefault(); handleLogout() }}>
            Logout ({user?.username})
          </a>
        </div>
      </div>
    </nav>
  )
}
