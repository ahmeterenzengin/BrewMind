#!/usr/bin/env bash
set -o errexit

pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
python manage.py collectstatic --no-input
python manage.py migrate
