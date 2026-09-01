import React, { useEffect, useState } from 'react'
import { NavLink } from 'react-router-dom'
import Header from '../components/Header'
import { ordersApi } from '../api'

const money = value => Number(value).toLocaleString('en-US', { style: 'currency', currency: 'USD' })

export default function Orders() {
  const [orders, setOrders] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const load = () => {
    setLoading(true)
    ordersApi.list()
      .then(resp => setOrders(resp.orders))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const cancel = async id => {
    if (!window.confirm('Are you sure you want to cancel this pending order?')) return
    try {
      await ordersApi.cancel(id)
      load()
    } catch (err) {
      window.alert(err.message)
    }
  }

  if (loading) return <><Header /><main className="container"><p className="muted">Loading orders…</p></main></>
  if (error) return <><Header /><main className="container"><p className="form-error">{error}</p></main></>

  const counts = {
    all: orders.length,
    pending: orders.filter(o => o.status === 'PENDING').length,
    approved: orders.filter(o => o.status === 'APPROVED').length,
    other: orders.filter(o => ['REJECTED', 'FLAGGED'].includes(o.status)).length,
  }

  return (
    <>
      <Header />
      <main className="container">
        <div className="page-heading order-heading">
          <div>
            <p className="eyebrow">ACTIVITY</p>
            <h1>Order History</h1>
            <p className="muted">Review and manage your trade orders.</p>
          </div>
          <div className="order-actions">
            <NavLink to="/buy" className="buy-btn">+ Buy</NavLink>
            <NavLink to="/sell" className="sell-btn">− Sell</NavLink>
          </div>
        </div>

        <div className="order-summary-grid">
          {[
            ['All Orders', counts.all, ''],
            ['Pending', counts.pending, 'warning-text'],
            ['Approved', counts.approved, 'positive'],
            ['Rejected / Flagged', counts.other, 'negative'],
          ].map(([label, value, cls]) => (
            <div className="order-summary" key={label}>
              <span>{label}</span>
              <strong className={cls}>{value}</strong>
            </div>
          ))}
        </div>

        <section className="panel">
          <div className="panel-header">
            <div><h2>Trade Orders</h2><p>Most recent activity first</p></div>
          </div>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  {['Order', 'Ticker', 'Side', 'Quantity', 'Price', 'Status', 'Submitted', 'Action'].map(h => (
                    <th key={h}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {orders.length === 0 && (
                  <tr><td colSpan={8} className="muted">No orders yet.</td></tr>
                )}
                {orders.map(o => (
                  <tr key={o.id}>
                    <td>#{o.id}</td>
                    <td><strong>{o.symbol}</strong></td>
                    <td><span className={`side-label ${o.order_type.toLowerCase()}-label`}>{o.order_type}</span></td>
                    <td>{o.quantity}</td>
                    <td>{money(o.price)}</td>
                    <td><span className={`status ${o.status.toLowerCase()}`}>{o.status}</span></td>
                    <td>{o.created_at ? new Date(o.created_at).toLocaleString() : '—'}</td>
                    <td>
                      {o.status === 'PENDING'
                        ? <button className="cancel-btn" onClick={() => cancel(o.id)}>Cancel</button>
                        : <span className="muted">—</span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </>
  )
}
