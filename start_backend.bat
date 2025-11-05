@echo off
echo ========================================
echo   IT Project Management - Backend
echo ========================================
echo.

cd backend

echo Installation des dependances Python...
pip install -r requirements.txt

echo.
echo Creation de la base de donnees (si necessaire)...
python manage.py makemigrations
python manage.py migrate

echo.
echo Chargement des donnees initiales...
python manage.py loaddata initial_data.json

echo.
echo Creation d'un superutilisateur (si necessaire)...
python manage.py shell -c "
from apps.authentication.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@company.com', 'admin123', first_name='Admin', last_name='System')
    print('Superutilisateur cree: admin@company.com / admin123')
else:
    print('Superutilisateur deja existant')
"

echo.
echo ========================================
echo   Demarrage du serveur Django...
echo   URL: http://localhost:8000
echo ========================================
echo.

python manage.py runserver
