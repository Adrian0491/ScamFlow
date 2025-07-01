#!/bin/bash
set -e
set -x

echo "[INFO] Installing ScamFlow Cleanup Service..."

# Dynamically finds the JSON output absolute path
ScamFlow_Path=$(realpath "$(dirname "$0")/JSON_Output")

# Check that the folder exists
if [ ! -d "$ScamFlow_Path" ]; then
    echo "[ERROR] Folder not found at $ScamFlow_Path"
    exit 1
fi

echo "[INFO] Detected folder path: $ScamFlow_Path"

# Update .service file with the detected folder path
sed "s|/path/to/scamFlow/JSON_Output|${ScamFlow_Path}|g" scamFlow_cleanup.service > /tmp/scamFlow_cleanup.service

# Makes files executable
chmod +x /tmp/scamFlow_cleanup.service
chmod +x scamFlow_cleanup.timer

# Copy to system
sudo cp /tmp/scamFlow_cleanup.service /etc/systemd/system/scamFlow_cleanup.service
sudo cp scamFlow_cleanup.timer /etc/systemd/system/scamFlow_cleanup.timer

# Reload and enable
sudo systemctl daemon-reload
sudo systemctl enable scamFlow_cleanup.timer
sudo systemctl start scamFlow_cleanup.timer

echo "[SUCCESS] ScamFlow Cleanup Timer installed and running every 6 hours."

set +x
