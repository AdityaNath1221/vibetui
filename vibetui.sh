#!/usr/bin/env bash 
set -e

if ! command -v python >/dev/null 2>&1; then
    echo "Python not found. Install latest version of python first!!"
    exit 1
fi

if [ ! -d ".env" ]; then
    echo "Creating Virtual Environment..."
    python -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt
fi

source .env/bin/activate

echo "Launching..."
cat assets/logo.txt
python VIBEtui.py


