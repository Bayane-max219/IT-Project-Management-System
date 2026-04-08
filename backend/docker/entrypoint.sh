#!/bin/sh
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  IT Project Management — Django API Starting..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Attendre PostgreSQL
echo "⏳ Waiting for database..."
until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(
        dbname=os.environ.get('DB_NAME','it_project_management'),
        user=os.environ.get('DB_USER','postgres'),
        password=os.environ.get('DB_PASSWORD','postgres'),
        host=os.environ.get('DB_HOST','db'),
        port=os.environ.get('DB_PORT','5432')
    )
    sys.exit(0)
except:
    sys.exit(1)
"; do
    echo "   Database not ready, retrying in 3s..."
    sleep 3
done
echo "✅ Database connected!"

# Migrations
echo "📦 Running migrations..."
python manage.py migrate --no-input

echo "🚀 IT Project Management API is ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exec "$@"
