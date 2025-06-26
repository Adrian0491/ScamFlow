#!/bin/bash

###########################################
# ScamFlow JSON Cleanup Script
# -----------------------------------------
# Deletes all .json files from JSON_Output
# directory and logs each action
#
# Suitable for:
# - Manual runs or usage
# - Cronjob automation
# - @reboot(run on VM boot)
###########################################

TARGE_DIR="/home/adi/Desktop/codingStuff/ScamFlow-Reporting/scamFlow/JSON_Output"
LOG_FILE="/home/adi/Desktop/codingStuff/ScamFlow-Reporting/scamFlow/cron/cleanup.log"


# --- Function: Log Message ---
log_message() {
    echo "[$(date '+%m-%d-%Y %H:%M')] $1" >> "$LOG_FILE"
}

# --- Function: Delete files ---
delete_json_files() {
    if [ -d "$TARGE_DIR"]; then
        log_message "Starting cleanup in $TARGE_DIR"
        find "$TARGE_DIR" -type f -name "*.json" -exec rm -f {} \;
        log_message "Cleanup completed. All json files removed."
    else
        log_message "ERROR: Directory not found: $TARGE_DIR or no files to delete"
    fi
}

# --- Main Function ---
main() {
    log_message "--- ScamFlow JSON Cleanup Started ---"
    delete_json_files
    log_message "--- ScamFlow JSON Cleanup Completed ---"
    echo "Done. See $LOG_FILE for details"
}

main("@")