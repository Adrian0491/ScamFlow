#!/bin/bash

###########################################
# ScamFlow Archival Timer Installer
# -----------------------------------------
# Creates systemd service and timer for
# JSON cleanup every 30 minutes after boot
###########################################

echo "[INFO] Installing ScamFlow Archival Timer..."

SERVICE_FILE="/etc/systemd/system/scamflow_archival.service"
TIMER_FILE="/etc/systemd/system/scamflow_archival.timer"
SCRIPT_PATH="/home/adi/Desktop/codingStuff/ScamFlow-Reporting/scamFlow/cron/archival.sh"

# Validate script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "[ERROR] Archival script not found at $SCRIPT_PATH"
    exit 1sudo
fi

# Create .service file
echo "[INFO] Creating $SERVICE_FILE"
sudo bash -c "cat > $SERVICE_FILE" <<EOLsu
[Unit]
Description=ScamFlow JSON Archival Script
After=network.target

[Service]
Type=oneshot
ExecStart=$SCRIPT_PATH
EOL

# Create .timer file
echo "[INFO] Creating $TIMER_FILE"
sudo bash -c "cat > $TIMER_FILE" <<EOL
[Unit]
Description=Run ScamFlow Archival Script every 30 minutes after boot

[Timer]
OnBootSec=5min
OnUnitActiveSec=30min
Persistent=true

[Install]
WantedBy=timers.target
EOL

# Reload systemd, enable and start timer
echo "[INFO] Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "[INFO] Enabling and starting ScamFlow Archival Timer..."
sudo systemctl enable $(basename "$TIMER_FILE")
sudo systemctl start $(basename "$TIMER_FILE")

# Optional: enable service to run on every boot (only needed if you want both boot + timer triggers)
# echo "[INFO] Enabling ScamFlow Archival Service to run on every boot..."
# sudo systemctl enable $(basename "$SERVICE_FILE")

echo "[SUCCESS] ScamFlow Archival Timer is installed and active."