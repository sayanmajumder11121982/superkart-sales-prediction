#!/usr/bin/env bash
# Builds and starts the SuperKart backend (Flask, port 7860) and frontend (Streamlit, port 8501)
# as two Docker containers on one Docker network. Run from the repository root inside a Codespace.
set -e
docker network create superkart-network 2>/dev/null || true
docker rm -f backend frontend 2>/dev/null || true
docker build -t superkart-backend ./backend
docker build -t superkart-frontend ./frontend
docker run -d --name backend --network superkart-network -p 7860:7860 superkart-backend
docker run -d --name frontend --network superkart-network -p 8501:8501 superkart-frontend
echo "Backend:  port 7860 (set to Public in the Ports tab)"
echo "Frontend: port 8501"
