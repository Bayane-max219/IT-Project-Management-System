@echo off
echo 🗄️ EXPORTATION BASE DE DONNÉES POSTGRESQL
echo ==========================================

REM Configuration
set DB_HOST=127.0.0.1
set DB_PORT=5432
set DB_NAME=it_project_management
set DB_USER=postgres
set PGPASSWORD=postgres

REM Créer un nom de fichier avec timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%%MM%%DD%_%HH%%Min%%Sec%"

set BACKUP_FILE=it_project_management_backup_%timestamp%.sql
set STRUCTURE_FILE=it_project_management_structure_%timestamp%.sql

echo 📁 Fichier de sauvegarde : %BACKUP_FILE%
echo 📁 Fichier de structure : %STRUCTURE_FILE%
echo.

echo 🔄 Exportation complète (données + structure)...
pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f %BACKUP_FILE% --verbose --clean --if-exists --create

if %ERRORLEVEL% EQU 0 (
    echo ✅ Exportation complète réussie !
) else (
    echo ❌ Erreur lors de l'exportation complète
    goto :error
)

echo.
echo 🏗️ Exportation structure seulement...
pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f %STRUCTURE_FILE% --schema-only --clean --if-exists --create

if %ERRORLEVEL% EQU 0 (
    echo ✅ Exportation structure réussie !
) else (
    echo ❌ Erreur lors de l'exportation structure
    goto :error
)

echo.
echo 🎉 EXPORTATION TERMINÉE !
echo.
echo 📋 Fichiers créés :
echo - %BACKUP_FILE% (base complète)
echo - %STRUCTURE_FILE% (structure seulement)
echo.
echo 🚀 Pour GitHub :
echo 1. Créez un dossier 'database/' dans votre repo
echo 2. Copiez ces fichiers .sql dans ce dossier
echo 3. Ajoutez un README avec les instructions d'importation
echo.
goto :end

:error
echo.
echo ❌ ERREUR DÉTECTÉE !
echo 💡 Solutions possibles :
echo 1. Vérifiez que PostgreSQL est démarré
echo 2. Vérifiez que pg_dump est dans le PATH
echo 3. Vérifiez les paramètres de connexion
echo 4. Essayez avec le chemin complet :
echo    "C:\Program Files\PostgreSQL\16\bin\pg_dump.exe"

:end
pause
