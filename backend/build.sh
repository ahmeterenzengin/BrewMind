#!/usr/bin/env bash
set -o errexit

pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
