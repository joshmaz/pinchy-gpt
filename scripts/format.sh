#!/usr/bin/env sh
set -e

echo "Running markdownlint and yamllint..."
markdownlint-cli2 "**/*.md" || true
yamllint -c .yamllint.yaml . || true
