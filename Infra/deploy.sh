```bash
#!/bin/bash
set -euxo pipefail

# ============================================================
# TradeGuard Flask Application Deployment
# ============================================================

REPO_URL="https://github.com/jzahmad/tradeguard.git"
REPO_DIR="/Backend"
BRANCH="main"
APP_PORT="5000"

# ============================================================
# 1. Install system dependencies
# ============================================================

apt-get update -y

apt-get install -y \
  git \
  python3 \
  python3-pip \
  python3-venv

# ============================================================
# 2. Clone application
# ============================================================

if [ -d "$REPO_DIR" ]; then
    rm -rf "$REPO_DIR"
fi

git clone \
  --branch "$BRANCH" \
  "$REPO_URL" \
  "$REPO_DIR"

cd "$REPO_DIR"

# ============================================================
# 3. Create Python virtual environment
# ============================================================

python3 -m venv "$REPO_DIR/venv"

source "$REPO_DIR/venv/bin/activate"

# ============================================================
# 4. Install Python dependencies
# ============================================================

pip install --upgrade pip

pip install -r requirements.txt

pip install gunicorn

# ============================================================
# 5. Create systemd service
# ============================================================

cat > /etc/systemd/system/tradeguard.service <<EOF
[Unit]
Description=TradeGuard Flask Application
After=network.target

[Service]
User=root
WorkingDirectory=$REPO_DIR

ExecStart=$REPO_DIR/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:$APP_PORT \
    app:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# ============================================================
# 6. Enable and start TradeGuard
# ============================================================

systemctl daemon-reload

systemctl enable tradeguard

systemctl restart tradeguard

# ============================================================
# 7. Check service status
# ============================================================

systemctl --no-pager status tradeguard

# ============================================================
# 8. Deployment status
# ============================================================

echo "TradeGuard deployment completed successfully." \
    > /var/log/user-data-status.log
```
