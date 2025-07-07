import os
from flask import Flask, render_template, request, redirect
import docker

app = Flask(__name__)
client = docker.from_env()
DNS_WATCHER_NAME = os.getenv("DNS_WATCHER_NAME", "dns-watcher")
ROOT_DOMAIN = os.getenv("DOMAIN")


def get_containers():
    containers = []
    for c in client.containers.list():
        labels = c.labels or {}
        enabled = labels.get("traefik.enable", "false") == "true"
        containers.append({
            "id": c.id,
            "name": c.name,
            "enabled": enabled,
            "subdomain": labels.get("traefik.domain", ""),
        })
    return containers


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", containers=get_containers())


@app.route("/update", methods=["POST"])
def update():
    for c in client.containers.list():
        labels = c.labels or {}
        enable = request.form.get(f"enable_{c.id}")
        sub = request.form.get(f"sub_{c.id}", "").strip()
        if enable:
            labels["traefik.enable"] = "true"
            if sub and ROOT_DOMAIN and not sub.endswith(ROOT_DOMAIN):
                sub = f"{sub}.{ROOT_DOMAIN}"
            if sub:
                labels["traefik.domain"] = sub
                labels[
                    f"traefik.http.routers.{c.name}.rule"
                ] = f"Host(`{sub}`)"
                labels[
                    f"traefik.http.routers.{c.name}.entrypoints"
                ] = "websecure"
                labels[
                    f"traefik.http.routers.{c.name}.tls.certresolver"
                ] = "le"
        else:
            labels.pop("traefik.enable", None)
            labels.pop("traefik.domain", None)
            labels.pop(f"traefik.http.routers.{c.name}.rule", None)
            labels.pop(f"traefik.http.routers.{c.name}.entrypoints", None)
            labels.pop(f"traefik.http.routers.{c.name}.tls.certresolver", None)
        c.update(labels=labels)
        c.restart()
    return redirect("/")


@app.route("/logs")
def logs():
    try:
        container = client.containers.get(DNS_WATCHER_NAME)
        return container.logs(tail=100).decode()
    except docker.errors.NotFound:
        return "dns-watcher container not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
