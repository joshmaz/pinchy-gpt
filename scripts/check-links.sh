#!/usr/bin/env sh
# Check links using lychee if available. This script prefers a local lychee install.

if command -v lychee >/dev/null 2>&1; then
  lychee .
  exit $?
fi

echo "lychee not found. You can install it via 'cargo install lychee-cli' or use the Docker image."
echo "Alternatively: docker run --rm -v $(pwd):/work --workdir /work lycheeverse/lychee lychee ."
exit 0
