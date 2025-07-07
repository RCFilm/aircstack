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

### Control panel

The stack now includes a small control panel served at
`https://control.${DOMAIN}`. Use it to toggle public routing for your running
containers and inspect the live log from the DNS watcher.

### Portainer extension

A Portainer extension is available in `portainer-extension/`. Import its
`metadata.json` in Portainer to install the control panel directly inside the
Portainer UI. The extension builds the same Flask app and exposes it on port
5000.
