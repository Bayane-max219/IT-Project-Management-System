@echo off
echo === Migration vers PostgreSQL ===
echo.

echo 1. Verification des migrations...
python manage.py showmigrations
echo.

echo 2. Execution des migrations...
python manage.py migrate
echo.

echo 3. Verification de la base de donnees...
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT version()'); print('PostgreSQL version:', cursor.fetchone()[0])"
echo.

echo Migration terminee!
pause
