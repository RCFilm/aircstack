# AircStack

A Docker-native reverse proxy with DNS auto-sync for IONOS (or other providers).

## Features

- 🔐 HTTPS via Let's Encrypt
- 📡 Auto DNS A-record creation via provider API (IONOS by default)
- 🧠 Detects containers using Docker label: \`traefik.domain\`
- 🪵 Detailed logging and robust error handling in the DNS sync service


## Usage

1. Copy and edit environment values:
   \`\`\`
   cp .env.example .env
# edit .env to set EMAIL and DOMAIN
# optional: SYNC_INTERVAL (seconds between DNS checks)
   cp config/provider.example.json config/provider.json
# edit config/provider.json with your DNS provider credentials
   \`\`\`

2. Launch the stack with the interactive script:
   \`\`\`
   ./start.sh
   \`\`\`
Choose an option to build or rebuild the containers as needed.

The DNS watcher service is built from `dns-sync/Dockerfile` and will
periodically ensure A records exist for containers that specify the
`traefik.domain` label.

DNS provider credentials are read from `config/provider.json`. The control
panel includes a **DNS Provider Settings** page where you can edit the API key,
root domain and target IP. Only IONOS is supported currently but the format is
ready for additional providers.

### Control panel

The stack now includes a small control panel served at
`https://control.${DOMAIN}`. Use it to toggle public routing for your running
containers and inspect the live log from the DNS watcher.

### AiRCStack Dashboard

The stack ships with a React interface under `docker-dashboard-ui` for managing
containers. OAuth login via Google is supported out of the box and containers
can be reordered using drag-and-drop. Start the UI locally with `npm run dev`
or build it for production and serve the static files behind Traefik.
Refer to `docker-dashboard-ui/README.md` for a quick overview.
