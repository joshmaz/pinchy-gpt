#!/usr/bin/env sh
set -e

EXIT=0

echo "Running markdownlint..."
markdownlint-cli2 "**/*.md" || EXIT=1

echo "Running yamllint..."
yamllint -c .yamllint.yaml . || EXIT=1

echo "Running codespell..."
codespell || EXIT=1

echo "Running shellcheck on scripts..."
shellcheck scripts/*.sh || EXIT=1

if [ "$EXIT" -ne 0 ]; then
  echo "Validation failed"
  exit 1
fi

echo "All checks passed (or tools missing)."
exit 0
