import React, { useEffect, useState } from 'react'
import Header from '../components/Header'
import { adminApi } from '../api'

const money = value => Number(value).toLocaleString('en-US', { style: 'currency', currency: 'USD' })

export default function Admin() {
  const [orders, setOrders] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [busyId, setBusyId] = useState(null)

  const load = () => {
    setLoading(true)
    adminApi.listOrders()
      .then(resp => setOrders(resp.orders))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const act = async (action, id) => {
    setBusyId(id)
    try {
      await adminApi[action](id)
      load()
    } catch (err) {
      window.alert(err.message)
    } finally {
      setBusyId(null)
    }
  }

  if (loading) return <><Header /><main className="container"><p className="muted">Loading orders…</p></main></>
  if (error) return <><Header /><main className="container"><p className="form-error">{error}</p></main></>

  return (
    <>
      <Header />
      <main className="container">
        <div className="page-heading">
          <p className="eyebrow">ADMIN</p>
          <h1>Order Review</h1>
          <p className="muted">Approve, reject, or flag pending trade orders across all accounts.</p>
        </div>

        <section className="panel">
          <div className="panel-header">
            <div><h2>All Orders</h2><p>Most recent activity first</p></div>
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
                  <tr><td colSpan={8} className="muted">No orders.</td></tr>
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
                      {o.status === 'PENDING' ? (
                        <div className="admin-actions">
                          <button
                            className="buy-btn"
                            disabled={busyId === o.id}
                            onClick={() => act('approve', o.id)}
                          >Approve</button>
                          <button
                            className="cancel-btn"
                            disabled={busyId === o.id}
                            onClick={() => act('reject', o.id)}
                          >Reject</button>
                          <button
                            className="sell-btn"
                            disabled={busyId === o.id}
                            onClick={() => act('flag', o.id)}
                          >Flag</button>
                        </div>
                      ) : <span className="muted">—</span>}
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
