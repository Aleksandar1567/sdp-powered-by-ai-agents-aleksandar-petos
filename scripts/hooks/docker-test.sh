#!/usr/bin/env bash
# Builds the kata Docker image and runs the test suite before every commit.
# Fail fast: any non-zero exit aborts the commit.
set -euo pipefail

echo "🐳 Building kata-tests image..."
docker build -t kata-tests . 1>/dev/null

echo "🧪 Running tests inside container..."
docker run --rm kata-tests

echo "✅ All tests passed — proceeding with commit."
