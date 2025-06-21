#!/bin/bash

# === CONFIGURATION ===
BRANCH="scamFlow_log_archive"
TARGET_DIR="scamFlow/JSON_Output"
GIT_USER="Adi Pircalaboiu"
GIT_EMAIL="pircalaboiu.adrian@yahoo.com"
COMMIT_MESSAGE="Auto-archival of JSON files to $BRANCH"

# === FUNCTIONS ===

configure_git() {
    git config user.name "$GIT_USER"
    git config user.email "$GIT_EMAIL"
}

commit_changes_main() {
    echo "Committing changes on main..."
    git add "$TARGET_DIR"/*.json
    git commit -m "$COMMIT_MESSAGE"
}

switch_to_branch() {
    echo "Switching to branch: $BRANCH"
    git checkout "$BRANCH" 2>/dev/null || git checkout -b "$BRANCH"
    git pull origin "$BRANCH"
}

copy_json_files() {
    echo "Copying JSON files to $BRANCH branch..."
    git checkout main -- "$TARGET_DIR"/*.json
}

commit_and_push_archive() {
    echo "Committing and pushing archived JSON files..."
    git add "$TARGET_DIR"/*.json
    git commit -m "$COMMIT_MESSAGE"
    git push origin "$BRANCH"
}

cleanup_json_files() {
    echo "Cleaning up local JSON files..."
    rm -f "$TARGET_DIR"/*.json
}

switch_back_main() {
    echo "Switching back to main branch..."
    git checkout main
    git pull origin main
}

# === MAIN ===

main() {
    cd "$(dirname "$0")"/../.. || exit 1

    echo "Starting archival process..."
    configure_git
    commit_changes_main
    switch_to_branch
    copy_json_files
    commit_and_push_archive
    cleanup_json_files
    switch_back_main
    echo "Archival complete."
}

main
