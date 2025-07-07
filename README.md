# AircStack

A Docker-native reverse proxy with DNS auto-sync for IONOS.

## Features

- 🔐 HTTPS via Let's Encrypt
- 📡 Auto DNS A-record creation via IONOS API
- 🧠 Detects containers using Docker label: \`traefik.domain\`

## SSH Key for GitHub

This script checks for or generates \`~/.ssh/aircstack\` for SSH-based GitHub access. Add \`aircstack.pub\` to your GitHub SSH keys.

## Usage

1. Copy and edit:
   \`\`\`
   cp .env.example .env
   \`\`\`

2. Launch:
   \`\`\`
   docker compose up --build -d
   \`\`\`
