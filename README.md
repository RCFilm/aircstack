# AircStack

A Docker-native reverse proxy with DNS auto-sync for IONOS.

## Features

- 🔐 HTTPS via Let's Encrypt
- 📡 Auto DNS A-record creation via IONOS API
- 🧠 Detects containers using Docker label: \`traefik.domain\`
- 🪵 Detailed logging and robust error handling in the DNS sync service


## Usage

1. Copy and edit environment values:
   \`\`\`
   cp .env.example .env
# edit .env to set EMAIL, DOMAIN, IONOS_API_KEY and TARGET_IP
# optional: SYNC_INTERVAL (seconds between DNS checks)
   \`\`\`

2. Launch the stack:
   \`\`\`
   docker compose up --build -d
   \`\`\`

The DNS watcher service is built from `dns-sync/Dockerfile` and will
periodically ensure A records exist for containers that specify the
`traefik.domain` label.
