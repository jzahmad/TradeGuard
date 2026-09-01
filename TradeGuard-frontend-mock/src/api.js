const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api'

const TOKEN_KEY = 'tradeguard_token'
const USER_KEY = 'tradeguard_user'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getStoredUser() {
  const raw = localStorage.getItem(USER_KEY)
  return raw ? JSON.parse(raw) : null
}

export function setSession(token, user) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function clearSession() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

async function request(path, { method = 'GET', body, auth = true } = {}) {
  const headers = { 'Content-Type': 'application/json' }

  if (auth) {
    const token = getToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })

  let data = null
  try {
    data = await response.json()
  } catch {
    data = null
  }

  if (!response.ok) {
    if (response.status === 401) clearSession()
    const message = (data && data.error) || `Request failed (${response.status})`
    throw new Error(message)
  }

  return data
}

export const authApi = {
  register: payload => request('/auth/register', { method: 'POST', body: payload, auth: false }),
  login: (username, password) =>
    request('/auth/login', { method: 'POST', body: { username, password }, auth: false }),
  me: () => request('/auth/me'),
}

export const dashboardApi = {
  get: () => request('/dashboard'),
}

export const ordersApi = {
  list: () => request('/orders'),
  get: id => request(`/orders/${id}`),
  create: ({ symbol, order_type, quantity }) =>
    request('/orders', { method: 'POST', body: { symbol, order_type, quantity } }),
  cancel: id => request(`/orders/${id}`, { method: 'DELETE' }),
}

export const stocksApi = {
  search: q => request(`/stocks/search?q=${encodeURIComponent(q)}`),
  price: symbol => request(`/stocks/${encodeURIComponent(symbol)}`),
}

export const adminApi = {
  listOrders: () => request('/admin/orders'),
  approve: id => request(`/admin/orders/${id}/approve`, { method: 'POST' }),
  reject: id => request(`/admin/orders/${id}/reject`, { method: 'POST' }),
  flag: id => request(`/admin/orders/${id}/flag`, { method: 'POST' }),
}
