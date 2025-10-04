#!/usr/bin/env bash
set -e


# Start both services via docker-compose
DOCKER_BUILDKIT=1 docker compose up --build
