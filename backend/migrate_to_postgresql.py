#!/usr/bin/env python
"""
Script pour migrer de SQLite vers PostgreSQL
"""
import os
import sys
import subprocess
import psycopg2
from psycopg2 import sql

def run_command(command, cwd=None):
    """Exécute une commande et retourne le résultat"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def create_postgresql_database():
    """Crée la base de données PostgreSQL si elle n'existe pas"""
    print("=== Création de la base de données PostgreSQL ===")
    
    # Configuration par défaut
    DB_NAME = 'it_project_management'
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    
    try:
        # Connexion au serveur PostgreSQL
        print("Connexion au serveur PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'  # Base de données par défaut
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Vérifier si la base de données existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Création de la base de données '{DB_NAME}'...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"✅ Base de données '{DB_NAME}' créée avec succès!")
        else:
            print(f"✅ Base de données '{DB_NAME}' existe déjà!")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Erreur PostgreSQL: {e}")
        print("\nAssurez-vous que:")
        print("- PostgreSQL est installé et en cours d'exécution")
        print("- L'utilisateur 'postgres' existe avec le mot de passe 'postgres'")
        print("- Le serveur écoute sur localhost:5432")
        return False

def migrate_to_postgresql():
    """Effectue la migration vers PostgreSQL"""
    print("\n=== Migration vers PostgreSQL ===")
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Créer la base de données PostgreSQL
    if not create_postgresql_database():
        return False
    
    # 2. Exécuter les migrations Django
    print("\n2. Exécution des migrations Django...")
    success, stdout, stderr = run_command("python manage.py migrate", backend_dir)
    
    if success:
        print("✅ Migrations Django exécutées avec succès!")
        if stdout:
            print("Sortie:", stdout)
    else:
        print("❌ Erreur lors des migrations Django:")
        print("Erreur:", stderr)
        return False
    
    # 3. Créer un superutilisateur (optionnel)
    print("\n3. Vérification du superutilisateur...")
    success, stdout, stderr = run_command(
        'python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(f\'Superusers: {User.objects.filter(is_superuser=True).count()}\')"',
        backend_dir
    )
    
    if success and "Superusers: 0" in stdout:
        print("Aucun superutilisateur trouvé. Vous devrez en créer un avec:")
        print("python manage.py createsuperuser")
    
    print("\n🎉 Migration vers PostgreSQL terminée avec succès!")
    print("\nPour tester la migration:")
    print("1. python manage.py runserver")
    print("2. Accédez à http://localhost:8000/admin")
    
    return True

if __name__ == '__main__':
    migrate_to_postgresql()
