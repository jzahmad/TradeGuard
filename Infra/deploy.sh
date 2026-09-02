#!/bin/bash
set -euxo pipefail

# ============================================================
# TradeGuard Flask Application Deployment
# ============================================================

REPO_URL="https://github.com/jzahmad/tradeguard.git"
REPO_DIR="/opt/tradeguard"
APP_DIR="/opt/tradeguard/Backend"
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
# 2. Create application directory
# ============================================================

mkdir -p /opt

# ============================================================
# 3. Clone TradeGuard repository
# ============================================================

if [ ! -d "$REPO_DIR/.git" ]; then

    git clone \
        --branch "$BRANCH" \
        "$REPO_URL" \
        "$REPO_DIR"

else

    cd "$REPO_DIR"

    git fetch origin

    git checkout "$BRANCH"

    git reset --hard "origin/$BRANCH"

fi

# ============================================================
# 4. Verify Backend directory
# ============================================================

if [ ! -d "$APP_DIR" ]; then
    echo "ERROR: Backend directory does not exist!"
    exit 1
fi

cd "$APP_DIR"

# ============================================================
# 5. Create Python virtual environment
# ============================================================

if [ ! -d "$APP_DIR/venv" ]; then
    python3 -m venv "$APP_DIR/venv"
fi

source "$APP_DIR/venv/bin/activate"

# ============================================================
# 6. Install Python dependencies
# ============================================================

pip install --upgrade pip

pip install -r requirements.txt

pip install gunicorn

# ============================================================
# 7. Create systemd service
# ============================================================

cat > /etc/systemd/system/tradeguard.service <<EOF
[Unit]
Description=TradeGuard Flask Application
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR

ExecStart=$APP_DIR/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:$APP_PORT \
    run:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# ============================================================
# 8. Enable and start TradeGuard
# ============================================================

systemctl daemon-reload

systemctl enable tradeguard

systemctl restart tradeguard

# ============================================================
# 9. Check service
# ============================================================

systemctl --no-pager status tradeguard

# ============================================================
# 10. Save deployment status
# ============================================================

echo "TradeGuard deployment completed successfully." \
    > /var/log/user-data-status.log