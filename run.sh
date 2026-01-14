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

# Build a simple watcher container that runs watchexec + typst
docker run --rm -i \
  -v "$WORKDIR":/work \
  -w /work \
  alpine:3.20 sh -c '
    apk add --no-cache watchexec typst >/dev/null &&
    watchexec -r -e typ -w src "
      for file in src/[!_]*.typ; do
        basename=\$(basename \"\$file\" .typ)
        echo \"Compiling \$basename.typ -> \$basename.pdf\"
        typst compile \"\$file\" \"\$basename.pdf\"
      done
    "
  '
