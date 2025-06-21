#!/bin/bash

#absolute path to the repo root
REPO_DIR="/home/adi/Desktop/codingStuff/ScamFlow-Reporting"
JSON_DIR= "$REPO_DIR/scamFlow/JSON_Output"

# git username and password setting
GIT_USER="Adi"
GIT_EMAIL="pircalaboiu.adrian@yahoo.com"

git config user.name "$GIT_USER"
git config user.email "$GIT_EMAIL"

cd "$REPO_DIR" || exit 1

# Switching to archival branch and pull the latest
git checkout scamFlow_log_archive
git pull origin scamFlow_log_archive

# Copying the JSON files from the output folder
# to the repo root and/or adjusting the targtet folder

cp "$JSON_DIR"/*.json 2>/dev/null


# Adding a commmit only if there are any changes

git add *.json
git commit -m "Archiving JSON output files!" || echo "No new files to commit"
git push origin scamFlow_log_archive

# Switching back to the main branch
# and deleting any existing or new JSON files

git checout main
rm -f "$JSON_DIR"/*.json
git add "$JSON_DIR"/*.json
git commit -m "Cleanup of JSON output after archival" || echo "No new files deleted!"
git push origin main