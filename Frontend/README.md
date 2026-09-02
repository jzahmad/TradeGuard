# TradeGuard Frontend

React (Vite) single-page app, wired to the TradeGuard backend API.

## Run locally

```bash
cd Frontend
npm install
npm run dev
```

Runs at `http://localhost:5173` by default. Points at
`http://127.0.0.1:5000/api` unless `VITE_API_URL` is set.

Routes: `/login`, `/register`, `/dashboard`, `/orders`, `/buy`, `/sell`, and
`/admin` (visible to ADMIN-role accounts only).
