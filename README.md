# AircStack

A Docker-native reverse proxy with DNS auto-sync for IONOS.

## Features

- 🔐 HTTPS via Let's Encrypt
- 📡 Auto DNS A-record creation via IONOS API
- 🧠 Detects containers using Docker label: \`traefik.domain\`
- 🪵 Detailed logging and robust error handling in the DNS sync service
- 📦 Lightweight image for the DNS watcher with configurable sync interval

## SSH Key for GitHub

This script checks for or generates \`~/.ssh/aircstack\` for SSH-based GitHub access. Add \`aircstack.pub\` to your GitHub SSH keys.

## Usage

1. Copy and edit environment values:
   \`\`\`
   cp .env.example .env
# edit .env to set EMAIL, DOMAIN, IONOS_API_KEY, TARGET_IP and optional SYNC_INTERVAL
   \`\`\`

2. Launch the stack:
   \`\`\`
   docker compose up --build -d
   \`\`\`

   The DNS watcher runs every `SYNC_INTERVAL` seconds (default 60). Override this value in `.env` if you need a different interval.

To run the watcher outside Docker for testing:
\`\`\`
python dns-sync/dns_sync.py --once
\`\`\`
