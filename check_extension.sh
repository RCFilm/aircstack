#!/usr/bin/env bash
set -euo pipefail

# Check Portainer extension volume mount
CONTAINER=${1:-portainer}
EXT_DIR=/extensions/proxycontrol

if ! command -v docker >/dev/null; then
  echo "Docker is not installed" >&2
  exit 1
fi

if ! docker ps -q -f name="^${CONTAINER}$" | grep -q .; then
  echo "Container '$CONTAINER' is not running" >&2
  exit 1
fi

if docker exec "$CONTAINER" /bin/sh -c "test -f $EXT_DIR/metadata.json"; then
  echo "Extension is mounted"
else
  echo "Extension not found at $EXT_DIR" >&2
  exit 1
fi
