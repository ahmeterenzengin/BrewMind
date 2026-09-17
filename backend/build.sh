#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python -c "from fastembed import TextEmbedding; TextEmbedding(model_name='sentence-transformers/all-MiniLM-L6-v2')"
python manage.py collectstatic --no-input
python manage.py migrate
