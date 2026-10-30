#!/usr/bin/env bash
set -e

# Миграцияларды қолдану
alembic upgrade head

# Пайдаланушы жоқ болса — әдепкі admin жасау (demo үшін)
python -m app.scripts.seed_admin

exec "$@"