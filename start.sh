#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

COMPOSE="docker compose"

if ! command -v docker >/dev/null; then
    echo "Docker is required but not installed." >&2
    exit 1
fi

function start_build() {
    $COMPOSE up -d --build
}

function remove_and_rebuild() {
    $COMPOSE down
    $COMPOSE up -d --build
}

function build_only() {
    $COMPOSE build
}

function purge_build() {
    $COMPOSE down -v --rmi all --remove-orphans
    $COMPOSE up -d --build
}

function show_menu() {
    echo "AircStack start script"
    echo "======================"
    echo "1) Build and start"
    echo "2) Remove containers then rebuild"
    echo "3) Build images only"
    echo "4) Purge volumes/images then rebuild"
    echo "5) Quit"
    echo
    read -rp "Select an option [1-5]: " choice
    case "$choice" in
        1) start_build ;;
        2) remove_and_rebuild ;;
        3) build_only ;;
        4) purge_build ;;
        5) echo "Exiting." ; exit 0 ;;
        *) echo "Invalid option" ; exit 1 ;;
    esac
}

show_menu
