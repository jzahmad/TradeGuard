# TradeGuard

Trade order and portfolio management app.

- **`Backend/`** — Flask + MySQL API (auth, orders, portfolio, admin approval workflow). See [Backend/README.md](Backend/README.md).
- **`Frontend/`** — React (Vite) single-page app. See [Frontend/README.md](Frontend/README.md).
- **`Infra/`** — Terraform for AWS deployment (EC2, RDS, VPC, security groups).

## Quick start

```bash
# terminal 1
cd Backend && python run.py

# terminal 2
cd Frontend && npm run dev
```

Open `http://localhost:5173`.
