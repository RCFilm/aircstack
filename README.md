# AircStack

A Docker-native reverse proxy with DNS auto-sync for IONOS.

## Features

- 🔐 HTTPS via Let's Encrypt
- 📡 Auto DNS A-record creation via IONOS API
- 🧠 Detects containers using Docker label: \`traefik.domain\`
- 🪵 Detailed logging and robust error handling in the DNS sync service

## SSH Key for GitHub

This script checks for or generates \`~/.ssh/aircstack\` for SSH-based GitHub access. Add \`aircstack.pub\` to your GitHub SSH keys.

## Usage

1. Copy and edit environment values:
   \`\`\`
   cp .env.example .env
# edit .env to set EMAIL, DOMAIN, IONOS_API_KEY and TARGET_IP
   \`\`\`

2. Launch the stack:
   \`\`\`
   docker compose up --build -d
   \`\`\`
