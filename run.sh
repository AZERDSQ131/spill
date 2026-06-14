#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
export MISTRAL_API_KEY="${MISTRAL_API_KEY:-}"
echo "🎤 Démarrage de Wispr Flow Clone..."
cd "$DIR" && exec "$DIR/.venv/bin/python3" main.py
