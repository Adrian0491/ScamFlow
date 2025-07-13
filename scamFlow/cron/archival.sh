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

# --- Function: To delete all existing JSON files ---
delete_json_files() {
    if [ -d "$TARGET_DIR" ]; then
        JSON_COUNT=$(find "$TARGET_DIR" -type f -name "*.json" | wc -l)
        if [ "$JSON_COUNT" -eq 0]; then
            log_message "No JSON files found in $TARGET_DIR. Nothing to delete."
        else
            log_message "Starting cleanup: Found $JSON_COUNT files in $TARGET_DIR"
            find "$TARGET_DIR" -type f -name "*.json" -exec rm -f {} \;
            log_message "Cleanup completed. All files deleted."
        fi
    else
        log_message "[ERROR] Directory not found: $TARGET_DIR"
}

# --- Function: Prune old cleanup.log if older than 7 days ---
prune_log_file() {
    if [ -f "$LOG_FILE" ]; then
        if [ "$(find "$LOG_FILE" -mtime +7)" ]; then
            rm -f "$LOG_FILE"
            echo "Old cleanup.log removed (older than 7 days)"
        fi
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