#!/bin/bash
set -e

# Tunggu database siap
echo "Menunggu database PostgreSQL siap..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database siap ✅"

# Jalankan konfigurasi Alembic
echo "Menjalankan konfigurasi Alembic..."
python env_config.py

# Jalankan migrasi Alembic
echo "Menjalankan migrasi Alembic..."
alembic upgrade head

# Jalankan seed data (opsional)
if python -m app.seeds.seed_data; then
  echo "Seed data berhasil dijalankan ✅"
else
  echo "Seed data gagal, lanjutkan tanpa error 🚫"
fi

# Jalankan aplikasi FastAPI
echo "Menjalankan aplikasi FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
