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
# - @reboot (run on VM boot)
###########################################

# Get absolute path to JSON_Output one level above script location
TARGET_DIR="$(realpath "$(dirname "$0")/../JSON_Output")"
LOG_FILE="$(realpath "$(dirname "$0")/cleanup.log")"

# --- Function: Log Message ---
log_message() {
    echo "[$(date '+%m-%d-%Y %H:%M')] $1" >> "$LOG_FILE"
}

# --- Function: Delete files ---
delete_json_files() {
    if [ -d "$TARGET_DIR" ]; then
        log_message "Starting cleanup in $TARGET_DIR"
        find "$TARGET_DIR" -type f -name "*.json" -exec rm -f {} \;
        log_message "Cleanup completed. All JSON files removed."
    else
        log_message "ERROR: Directory not found: $TARGET_DIR or no files to delete"
    fi
}

# --- Main Function ---
main() {
    log_message "--- ScamFlow JSON Cleanup Started ---"
    delete_json_files
    log_message "--- ScamFlow JSON Cleanup Completed ---"
    echo "Done. See $LOG_FILE for details"
}

main "$@"