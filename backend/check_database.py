#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from django.conf import settings

def check_database():
    """Vérifier la connexion à la base de données"""
    print("🔍 VÉRIFICATION DE LA BASE DE DONNÉES")
    print("="*50)
    
    # Configuration
    db_config = settings.DATABASES['default']
    print(f"📊 ENGINE: {db_config['ENGINE']}")
    print(f"📊 NAME: {db_config['NAME']}")
    print(f"📊 USER: {db_config['USER']}")
    print(f"📊 HOST: {db_config['HOST']}")
    print(f"📊 PORT: {db_config['PORT']}")
    
    # Test de connexion
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"\n✅ CONNEXION RÉUSSIE !")
            print(f"🐘 Version PostgreSQL: {version}")
            
            # Informations sur la base
            cursor.execute("SELECT current_database();")
            current_db = cursor.fetchone()[0]
            print(f"📁 Base de données actuelle: {current_db}")
            
            # Liste des tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            print(f"\n📋 TABLES DANS LA BASE ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]}")
                
    except Exception as e:
        print(f"\n❌ ERREUR DE CONNEXION: {e}")
        print("\n🔧 VÉRIFIEZ :")
        print("   1. PostgreSQL est-il installé et démarré ?")
        print("   2. La base 'it_project_management' existe-t-elle ?")
        print("   3. L'utilisateur 'postgres' a-t-il les bonnes permissions ?")

if __name__ == '__main__':
    check_database()
