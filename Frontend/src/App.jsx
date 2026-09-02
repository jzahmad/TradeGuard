import React from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, RequireAuth } from './AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Orders from './pages/Orders'
import Trade from './pages/Trade'
import Admin from './pages/Admin'

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
        <Route path="/orders" element={<RequireAuth><Orders /></RequireAuth>} />
        <Route path="/buy" element={<RequireAuth><Trade side="buy" /></RequireAuth>} />
        <Route path="/sell" element={<RequireAuth><Trade side="sell" /></RequireAuth>} />
        <Route path="/admin" element={<RequireAuth adminOnly><Admin /></RequireAuth>} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </AuthProvider>
  )
}
