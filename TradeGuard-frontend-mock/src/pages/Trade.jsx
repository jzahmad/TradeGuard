import React, { useEffect, useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import { dashboardApi, ordersApi, stocksApi } from '../api'

const money = value => Number(value).toLocaleString('en-US', { style: 'currency', currency: 'USD' })

export default function Trade({ side }) {
  const isBuy = side === 'buy'
  const navigate = useNavigate()

  const [symbol, setSymbol] = useState('')
  const [quote, setQuote] = useState(null)
  const [quoteError, setQuoteError] = useState('')
  const [quoting, setQuoting] = useState(false)

  const [holdings, setHoldings] = useState([])
  const [selectedHolding, setSelectedHolding] = useState('')

  const [quantity, setQuantity] = useState(isBuy ? 10 : 1)
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState('')

  useEffect(() => {
    if (!isBuy) {
      dashboardApi.get().then(data => {
        setHoldings(data.holdings)
        if (data.holdings.length > 0) setSelectedHolding(data.holdings[0].symbol)
      })
    }
  }, [isBuy])

  const fetchQuote = async () => {
    if (!symbol.trim()) return
    setQuoting(true)
    setQuoteError('')
    try {
      const data = await stocksApi.price(symbol.trim())
      setQuote(data)
    } catch (err) {
      setQuote(null)
      setQuoteError(err.message)
    } finally {
      setQuoting(false)
    }
  }

  const holding = holdings.find(h => h.symbol === selectedHolding)
  const activeSymbol = isBuy ? (quote ? quote.symbol : symbol.trim().toUpperCase()) : selectedHolding
  const activePrice = isBuy ? (quote ? quote.current_price : 0) : (holding ? holding.current_price : 0)
  const maxShares = isBuy ? Infinity : (holding ? holding.quantity : 0)

  const submit = async event => {
    event.preventDefault()
    setFormError('')

    const qty = Number(quantity)
    if (!Number.isInteger(qty) || qty <= 0) {
      setFormError('Enter a valid quantity.')
      return
    }
    if (!isBuy && qty > maxShares) {
      setFormError(`You only own ${maxShares} shares of ${activeSymbol}.`)
      return
    }
    if (!activeSymbol) {
      setFormError(isBuy ? 'Look up a stock symbol first.' : 'Select a holding to sell.')
      return
    }
    if (!window.confirm(`Submit ${side.toUpperCase()} order for ${qty} shares of ${activeSymbol}?`)) return

    setSubmitting(true)
    try {
      await ordersApi.create({ symbol: activeSymbol, order_type: side.toUpperCase(), quantity: qty })
      window.alert(`${isBuy ? 'Buy' : 'Sell'} order submitted. Status: Pending`)
      navigate('/orders')
    } catch (err) {
      setFormError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <>
      <Header />
      <main className="container trade-page">
        <NavLink className="back-link" to="/dashboard">← Back to dashboard</NavLink>
        <div className="trade-page-header">
          <div>
            <p className="eyebrow">NEW ORDER</p>
            <h1>{isBuy ? 'Buy' : 'Sell'} Stock</h1>
            <p className="muted">{isBuy ? 'Create a new purchase order.' : 'Sell an existing portfolio position.'}</p>
          </div>
          <span className={`side-pill ${side}-side`}>{side.toUpperCase()}</span>
        </div>

        <div className="trade-layout">
          <section className="panel trade-form">
            {isBuy ? (
              <div className="form-section">
                <label htmlFor="ticker">Stock Symbol</label>
                <div className="quote-lookup">
                  <input
                    id="ticker"
                    value={symbol}
                    onChange={e => { setSymbol(e.target.value.toUpperCase()); setQuote(null) }}
                    placeholder="e.g. AAPL"
                  />
                  <button type="button" className="primary-btn" onClick={fetchQuote} disabled={quoting}>
                    {quoting ? 'Looking up…' : 'Get Quote'}
                  </button>
                </div>
                {quoteError && <p className="form-error">{quoteError}</p>}
                {quote && (
                  <div className="ticker-result">
                    <div><strong>{quote.symbol}</strong><span>Live quote</span></div>
                    <div className="quote">{money(quote.current_price)}</div>
                  </div>
                )}
              </div>
            ) : (
              <div className="form-section">
                <label htmlFor="ticker">Select Holding</label>
                <select id="ticker" value={selectedHolding} onChange={e => setSelectedHolding(e.target.value)}>
                  {holdings.length === 0 && <option value="">No holdings available</option>}
                  {holdings.map(h => (
                    <option key={h.symbol} value={h.symbol}>{h.symbol} — {h.quantity} shares</option>
                  ))}
                </select>
                {holding && (
                  <div className="ticker-result">
                    <div><strong>{holding.symbol}</strong><span>Current market price</span></div>
                    <div className="quote">{money(holding.current_price)}</div>
                  </div>
                )}
              </div>
            )}

            <div className="form-section">
              <label htmlFor="quantity">Quantity</label>
              <input
                id="quantity"
                type="number"
                min="1"
                max={isBuy ? undefined : maxShares}
                value={quantity}
                onChange={e => setQuantity(e.target.value)}
              />
              {!isBuy && <small>{maxShares} shares available</small>}
            </div>

            <div className="estimate-card">
              <div>
                <span>Market Price</span>
                <strong>{activePrice ? money(activePrice) : '—'}</strong>
              </div>
              <div>
                <span>Estimated {isBuy ? 'Cost' : 'Proceeds'}</span>
                <strong>{money(activePrice * (Number(quantity) || 0))}</strong>
              </div>
            </div>

            {formError && <p className="form-error">{formError}</p>}

            <button className={`${side}-btn full-width`} onClick={submit} disabled={submitting}>
              {submitting ? 'Submitting…' : `Submit ${isBuy ? 'Buy' : 'Sell'} Order`}
            </button>
          </section>
        </div>
      </main>
    </>
  )
}
