#!/bin/bash

python3 -m venv ./.venv
source ./.venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --host "0.0.0.0" --port 8000 --forwarded-allow-ips "*" --proxy-headers --reload

