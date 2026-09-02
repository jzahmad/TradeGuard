#!/bin/bash
set -euxo pipefail

REPO_URL="https://github.com/jzahmad/TradeGuard.git"
REPO_DIR="/opt/tradeguard"
APP_DIR="/opt/tradeguard/Backend"
BRANCH="main"
APP_PORT="5000"

echo "=== TradeGuard deployment started ==="

# Update Amazon Linux
dnf update -y

# Install required packages
dnf install -y \
    git \
    python3 \
    python3-pip

# Create /opt directory
mkdir -p /opt

# Clone repository if it doesn't exist
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

# Verify Backend directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "ERROR: Backend directory does not exist!"
    exit 1
fi

cd "$APP_DIR"

# Create Python virtual environment
if [ ! -d "$APP_DIR/venv" ]; then
    python3 -m venv "$APP_DIR/venv"
fi

# Activate virtual environment
source "$APP_DIR/venv/bin/activate"

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Create systemd service
cat > /etc/systemd/system/tradeguard.service <<EOF
[Unit]
Description=TradeGuard Flask Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"

ExecStart=$APP_DIR/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:$APP_PORT \
    run:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

# Enable service on boot
systemctl enable tradeguard

# Start/restart application
systemctl restart tradeguard

# Show service status
systemctl --no-pager status tradeguard

# Save deployment status
echo "TradeGuard deployment completed successfully." \
    > /var/log/user-data-status.log

echo "=== TradeGuard deployment completed ==="