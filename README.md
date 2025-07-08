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

### Portainer extension

The stack ships with a Portainer extension for the control panel. It is mounted
into Portainer automatically so no manual import is required. Once the stack
starts, the **Proxy Control** tab will appear in Portainer using the same Flask
app on port 5000. The extension also adds a **DNS Provider** item under
Portainer's **Settings** side menu where you can manage API credentials and the
target IP. When exposing a container, leaving the subdomain blank will default
it to the container name.

**Important:** Starting with Portainer 2.19, the Community Edition no longer
loads local extensions. This stack pins `portainer/portainer-ce:2.18.4` so the
Proxy Control extension remains visible. If you need a newer Portainer release,
consider the Business Edition instead.

If you started Portainer previously without the extension mounted, the
`portainer_data` volume may cache the old state and hide the extension even
after updating the stack. Run `./start.sh` and choose the option to purge
volumes (or manually `docker compose down -v && docker volume rm
aircstack_portainer_data`) to recreate the volume and load the extension.


If the extension still doesn't show up after purging, exec into the
`portainer` container and check that `/extensions/reverse-proxy/metadata.json`
exists. If it doesn't, ensure the `portainer-extension` folder is accessible
and the `EXTENSIONS` variable in `docker-compose.yml` points to that path.

