#!/usr/bin/env bash
set -eu

IMAGE="ghcr.io/typst/typst:latest"
WORKDIR="$(pwd)"
SRC_DIR="$WORKDIR/src"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker not found." >&2
  exit 2
fi

if [ ! -d "$SRC_DIR" ]; then
  echo "src/ directory not found." >&2
  exit 2
fi

INPUT="$SRC_DIR/main.typ"
OUTPUT="$WORKDIR/result.pdf"

# Build a simple watcher container that runs watchexec + typst
docker run --rm -it \
  -v "$WORKDIR":/work \
  -w /work \
  alpine:3.20 sh -c "
    apk add --no-cache watchexec typst >/dev/null &&
    watchexec -r -e typ -w src \
      'typst compile src/main.typ result.pdf'
  "
