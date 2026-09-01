import React, { useEffect, useState } from 'react'
import { NavLink } from 'react-router-dom'
import Header from '../components/Header'
import { dashboardApi, ordersApi } from '../api'

const money = value =>
  Number(value).toLocaleString('en-US', { style: 'currency', currency: 'USD' })

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [pendingCount, setPendingCount] = useState(0)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    Promise.all([dashboardApi.get(), ordersApi.list()])
      .then(([dashboard, ordersResp]) => {
        if (cancelled) return
        setData(dashboard)
        setPendingCount(ordersResp.orders.filter(o => o.status === 'PENDING').length)
      })
      .catch(err => !cancelled && setError(err.message))
      .finally(() => !cancelled && setLoading(false))

    return () => { cancelled = true }
  }, [])

  if (loading) return <><Header /><main className="container"><p className="muted">Loading dashboard…</p></main></>
  if (error) return <><Header /><main className="container"><p className="form-error">{error}</p></main></>

  const holdingsValue = data.holdings.reduce((sum, h) => sum + h.current_value, 0)
  const totalValue = data.cash_balance + holdingsValue
  const unrealizedPl = data.holdings.reduce(
    (sum, h) => sum + (h.current_price - h.average_price) * h.quantity,
    0
  )
  const largest = data.holdings.reduce(
    (best, h) => (!best || h.current_value > best.current_value ? h : best),
    null
  )

  const metrics = [
    ['Cash Available', money(data.cash_balance), null],
    ['Pending Orders', String(pendingCount), 'Awaiting admin review'],
    [
      'Largest Position',
      largest ? largest.symbol : '—',
      largest ? `${((largest.current_value / totalValue) * 100 || 0).toFixed(0)}% of portfolio` : 'No holdings yet',
    ],
    ['Unrealized P/L', money(unrealizedPl), null, unrealizedPl >= 0 ? 'positive' : 'negative'],
  ]

  return (
    <>
      <Header />
      <main className="container">
        <div className="page-heading">
          <p className="eyebrow">OVERVIEW</p>
          <h1>Portfolio Dashboard</h1>
          <p className="muted">Live positions and cash balance from your account.</p>
        </div>

        <div className="hero-grid">
          <section className="portfolio-hero">
            <p className="card-label">Total Account Value</p>
            <h2>{money(totalValue)}</h2>
            <div className="hero-stats">
              <div><span>Holdings</span><strong>{money(holdingsValue)}</strong></div>
              <div><span>Cash</span><strong>{money(data.cash_balance)}</strong></div>
            </div>
          </section>
        </div>

        <div className="metric-grid">
          {metrics.map(([label, value, sub, cls]) => (
            <div className="metric-card" key={label}>
              <span>{label}</span>
              <strong className={cls || ''}>{value}</strong>
              {sub && <small>{sub}</small>}
            </div>
          ))}
        </div>

        <div className="trade-actions">
          <NavLink to="/buy" className="buy-btn">+ Buy Stock</NavLink>
          <NavLink to="/sell" className="sell-btn">− Sell Stock</NavLink>
        </div>

        <section className="panel">
          <div className="panel-header">
            <div>
              <h2>Current Holdings</h2>
              <p>Live portfolio positions</p>
            </div>
          </div>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  {['Ticker', 'Quantity', 'Avg Price', 'Market Price', 'Value', 'Return'].map(h => (
                    <th key={h}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.holdings.length === 0 && (
                  <tr><td colSpan={6} className="muted">No holdings yet — place a buy order to get started.</td></tr>
                )}
                {data.holdings.map(h => {
                  const returnPct = ((h.current_price - h.average_price) / h.average_price) * 100
                  const positive = returnPct >= 0
                  return (
                    <tr key={h.symbol}>
                      <td>
                        <div className="ticker-cell">
                          <div className="ticker-logo">{h.symbol[0]}</div>
                          <strong>{h.symbol}</strong>
                        </div>
                      </td>
                      <td>{h.quantity}</td>
                      <td>{money(h.average_price)}</td>
                      <td>{money(h.current_price)}</td>
                      <td>{money(h.current_value)}</td>
                      <td className={positive ? 'positive' : 'negative'}>
                        {positive ? '+' : ''}{returnPct.toFixed(2)}%
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </>
  )
}
