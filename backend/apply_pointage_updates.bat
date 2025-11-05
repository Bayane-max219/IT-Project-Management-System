@echo off
echo ========================================
echo   MISE A JOUR SYSTEME DE POINTAGE
echo ========================================
echo.

echo [1/4] Creation des migrations...
python manage.py makemigrations pointage
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR lors de la creation des migrations!
    pause
    exit /b 1
)
echo.

echo [2/4] Application des migrations...
python manage.py migrate pointage
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR lors de l'application des migrations!
    pause
    exit /b 1
)
echo.

echo [3/4] Application de toutes les migrations...
python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR lors de l'application des migrations!
    pause
    exit /b 1
)
echo.

echo [4/4] Verification de la base de donnees...
python manage.py check
if %ERRORLEVEL% NEQ 0 (
    echo ATTENTION: Des problemes ont ete detectes!
    pause
    exit /b 1
)
echo.

echo ========================================
echo   MISE A JOUR TERMINEE AVEC SUCCES!
echo ========================================
echo.
echo Le systeme de pointage est maintenant a jour avec :
echo - Gestion complete des retards (arrivee, pause, retour, depart)
echo - Demande automatique de justification
echo - Statistiques detaillees pour l'admin
echo - Historique visible pour developpeurs et admin
echo.
echo Vous pouvez maintenant demarrer le serveur avec:
echo   python manage.py runserver
echo.
pause
