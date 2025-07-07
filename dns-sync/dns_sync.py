import os
import time
import docker
import requests

IONOS_API_KEY = os.getenv("IONOS_API_KEY")
ROOT_DOMAIN = os.getenv("ROOT_DOMAIN")
TARGET_IP = os.getenv("TARGET_IP")
HEADERS = {"X-API-Key": IONOS_API_KEY, "Content-Type": "application/json"}

def get_zone_id():
    r = requests.get("https://api.hosting.ionos.com/dns/v1/zones", headers=HEADERS)
    zones = r.json()
    for z in zones:
        if z["name"] == ROOT_DOMAIN:
            return z["id"]
    raise Exception("Zone not found")

def sync_dns():
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
    r = requests.get(f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}", headers=HEADERS)
    current_records = r.json()["records"]
    current_subs = {r["name"]: r["id"] for r in current_records if r["type"] == "A" and r["content"] == TARGET_IP}

    # Create missing records
    for sub in subdomains:
        if sub not in current_subs:
            print(f"Creating A record for {sub}")
            payload = [{
                "name": sub,
                "type": "A",
                "content": TARGET_IP,
                "ttl": 3600,
                "prio": 0,
                "disabled": False
            }]
            requests.post(f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}/records", headers=HEADERS, json=payload)

    # Remove stale records
    for name, rid in current_subs.items():
        if name not in subdomains:
            print(f"Deleting stale DNS record {name}")
            requests.delete(f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}/records/{rid}", headers=HEADERS)

if __name__ == "__main__":
    while True:
        try:
            sync_dns()
        except Exception as e:
            print("ERROR:", e)
        time.sleep(60)
