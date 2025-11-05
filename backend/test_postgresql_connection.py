#!/usr/bin/env python
"""
Script pour tester la connexion PostgreSQL
"""
import os
import sys
import django

# Configuration du chemin Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from django.core.management.color import no_style
from django.db.utils import OperationalError
import psycopg2
from psycopg2 import sql

def test_postgresql_connection():
    """Teste la connexion PostgreSQL et crée la base de données si nécessaire"""
    
    print("=== Test de connexion PostgreSQL ===")
    
    # Configuration par défaut
    DB_NAME = 'it_project_management'
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    
    print(f"Configuration:")
    print(f"- Base de données: {DB_NAME}")
    print(f"- Utilisateur: {DB_USER}")
    print(f"- Hôte: {DB_HOST}")
    print(f"- Port: {DB_PORT}")
    print()
    
    # Test 1: Connexion au serveur PostgreSQL (sans base de données spécifique)
    try:
        print("1. Test de connexion au serveur PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'  # Base de données par défaut
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Connexion au serveur PostgreSQL réussie!")
        
        # Vérifier si la base de données existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"2. Création de la base de données '{DB_NAME}'...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"✅ Base de données '{DB_NAME}' créée avec succès!")
        else:
            print(f"✅ Base de données '{DB_NAME}' existe déjà!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ Erreur de connexion PostgreSQL: {e}")
        print("\nVérifiez que:")
        print("- PostgreSQL est installé et en cours d'exécution")
        print("- L'utilisateur 'postgres' existe avec le mot de passe 'postgres'")
        print("- Le serveur écoute sur localhost:5432")
        return False
    
    # Test 2: Connexion Django à la base de données
    try:
        print("3. Test de connexion Django...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"✅ Connexion Django réussie!")
            print(f"Version PostgreSQL: {version}")
        
    except OperationalError as e:
        print(f"❌ Erreur de connexion Django: {e}")
        return False
    
    print("\n🎉 Tous les tests de connexion PostgreSQL ont réussi!")
    return True

if __name__ == '__main__':
    test_postgresql_connection()
