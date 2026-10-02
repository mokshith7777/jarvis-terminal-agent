#!/usr/bin/env bash
set -euo pipefail
REPO_URL="${1:?Usage: ./scripts/push-to-github.sh https://github.com/USER/jarvis-terminal-agent.git}"
git init
git branch -M main
git add .
git commit -m 'Initial JARVIS Terminal Agent release'
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
git push -u origin main
