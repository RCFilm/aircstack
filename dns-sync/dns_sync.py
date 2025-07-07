"""Sync IONOS DNS A records with running Docker containers.

Environment variables:
    IONOS_API_KEY: API token for IONOS
    ROOT_DOMAIN:   domain zone to manage
    TARGET_IP:     IP address for created records
    SYNC_INTERVAL: optional default interval in seconds
"""

import os
import time
import logging
import argparse

import docker
import requests

IONOS_API_KEY = os.getenv("IONOS_API_KEY")
ROOT_DOMAIN = os.getenv("ROOT_DOMAIN")
TARGET_IP = os.getenv("TARGET_IP")
DEFAULT_INTERVAL = int(os.getenv("SYNC_INTERVAL", "60"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

if not all([IONOS_API_KEY, ROOT_DOMAIN, TARGET_IP]):
    raise RuntimeError("Missing one of IONOS_API_KEY, ROOT_DOMAIN or TARGET_IP environment variables")

HEADERS = {"X-API-Key": IONOS_API_KEY, "Content-Type": "application/json"}


def _request(method: str, url: str, **kwargs):
    """Helper performing HTTP requests with error handling."""
    resp = requests.request(method, url, headers=HEADERS, **kwargs)
    try:
        data = resp.json()
    except ValueError:
        resp.raise_for_status()
        raise RuntimeError(f"Invalid JSON response from {url}")

    if not resp.ok:
        msg = data.get("message", resp.text)
        raise RuntimeError(f"API error {resp.status_code}: {msg}")

    return data

def get_zone_id() -> str:
    """Return the zone id for ``ROOT_DOMAIN``."""
    zones = _request("GET", "https://api.hosting.ionos.com/dns/v1/zones")
    for zone in zones:
        if zone.get("name") == ROOT_DOMAIN:
            return zone.get("id")
    raise RuntimeError(f"Zone {ROOT_DOMAIN} not found")

def sync_dns():
    """Synchronize DNS records with running containers."""
    zone_id = get_zone_id()
    client = docker.from_env()
    containers = client.containers.list()
    subdomains = set()

    for container in containers:
        labels = container.labels
        domain = labels.get("traefik.domain")
        if domain and domain.endswith(ROOT_DOMAIN):
            subdomains.add(domain)

    # Get current DNS records
    zone_info = _request("GET", f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}")
    current_records = zone_info.get("records", [])
    current_subs = {
        rec.get("name"): rec.get("id")
        for rec in current_records
        if rec.get("type") == "A" and rec.get("content") == TARGET_IP
    }

    # Create missing records
    for sub in subdomains:
        if sub not in current_subs:
            logging.info("Creating A record for %s", sub)
            payload = [{
                "name": sub,
                "type": "A",
                "content": TARGET_IP,
                "ttl": 3600,
                "prio": 0,
                "disabled": False,
            }]
            _request(
                "POST",
                f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}/records",
                json=payload,
            )

    # Remove stale records
    for name, rid in current_subs.items():
        if name not in subdomains:
            logging.info("Deleting stale DNS record %s", name)
            _request(
                "DELETE",
                f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}/records/{rid}",
            )

def main() -> None:
    """Run the synchronization loop or a one-shot sync."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL,
        help="seconds between sync runs (default: %(default)s)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="run a single sync and exit",
    )
    args = parser.parse_args()

    if args.once:
        sync_dns()
        return

    while True:
        try:
            sync_dns()
        except Exception as exc:  # pragma: no cover - top-level loop
            logging.exception("Error during sync: %s", exc)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
