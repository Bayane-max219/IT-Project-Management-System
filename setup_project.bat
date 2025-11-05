@echo off
echo ========================================
echo   IT Project Management System
echo   Configuration initiale du projet
echo ========================================
echo.

echo 1. Verification des prerequis...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Node.js n'est pas installe ou pas dans le PATH
    echo Veuillez installer Node.js depuis https://nodejs.org
    pause
    exit /b 1
)

echo Python et Node.js detectes avec succes!
echo.

echo 2. Configuration du backend Django...
cd backend

echo Creation du fichier .env...
if not exist .env (
    copy .env.example .env
    echo Fichier .env cree. Modifiez les parametres de base de donnees si necessaire.
) else (
    echo Fichier .env deja existant.
)

echo Installation des dependances Python...
pip install -r requirements.txt

echo Creation des migrations...
python manage.py makemigrations

echo Application des migrations...
python manage.py migrate

echo Chargement des donnees initiales...
python manage.py loaddata initial_data.json

echo Creation du superutilisateur...
python manage.py shell -c "
from apps.authentication.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@company.com', 'admin123', first_name='Admin', last_name='System')
    print('Superutilisateur cree: admin@company.com / admin123')
else:
    print('Superutilisateur deja existant')
"

cd ..

echo.
echo 3. Configuration du frontend React...
cd frontend

echo Installation des dependances Node.js...
npm install

cd ..

echo.
echo ========================================
echo   Configuration terminee avec succes!
echo ========================================
echo.
echo COMPTES DE TEST:
echo - Admin: admin@company.com / admin123
echo - Developpeur: rakoto@company.com / dev123
echo - Client: client@example.com / client123
echo.
echo POUR DEMARRER L'APPLICATION:
echo 1. Lancez start_backend.bat (serveur Django)
echo 2. Lancez start_frontend.bat (serveur React)
echo 3. Ouvrez http://localhost:3000 dans votre navigateur
echo.
echo IMPORTANT: Assurez-vous que PostgreSQL est installe et configure
echo avec une base de donnees nommee 'it_project_management'
echo.
pause
