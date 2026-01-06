#!/usr/bin/env bash 
set -e

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python not found. Install latest version of python first!!"
    exit 1
fi

if [ ! -d ".env" ]; then
    echo "Creating Virtual Environment..."
    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt
fi

source .env/bin/activate

echo "Launching..."
cat assets/logo.txt
python3 VIBEtui.py


