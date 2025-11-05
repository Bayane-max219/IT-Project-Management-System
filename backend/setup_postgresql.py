#!/usr/bin/env python
"""
Script simple pour configurer PostgreSQL
"""
import psycopg2
from psycopg2 import sql
import os

def setup_postgresql():
    """Configure PostgreSQL pour le projet"""
    
    # Configuration
    DB_NAME = 'it_project_management'
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    
    print("=== Configuration PostgreSQL ===")
    print(f"Base de données: {DB_NAME}")
    print(f"Utilisateur: {DB_USER}")
    print(f"Hôte: {DB_HOST}:{DB_PORT}")
    print()
    
    try:
        # Connexion au serveur PostgreSQL
        print("Connexion au serveur PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Vérifier si la base de données existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Création de la base de données '{DB_NAME}'...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print("✅ Base de données créée!")
        else:
            print("✅ Base de données existe déjà!")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Configuration PostgreSQL terminée!")
        print("\nMaintenant, exécutez:")
        print("python manage.py migrate")
        print("python manage.py runserver")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\nVérifiez que PostgreSQL est installé et en cours d'exécution.")
        print("Utilisateur par défaut: postgres")
        print("Mot de passe par défaut: postgres")
        return False

if __name__ == '__main__':
    setup_postgresql()
