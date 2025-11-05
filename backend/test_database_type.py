#!/usr/bin/env python
"""
Vérifier le type de base de données utilisée
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from django.conf import settings

print("🔍 VÉRIFICATION BASE DE DONNÉES")
print("="*50)

# Informations de configuration
db_config = settings.DATABASES['default']
print(f"📊 Configuration:")
print(f"   Engine: {db_config['ENGINE']}")
print(f"   Nom: {db_config['NAME']}")
print(f"   Utilisateur: {db_config['USER']}")
print(f"   Hôte: {db_config['HOST']}")
print(f"   Port: {db_config['PORT']}")

# Test de connexion
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"\n✅ CONNEXION RÉUSSIE")
        print(f"📋 Version PostgreSQL: {version}")
        
        # Vérifier quelques tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE '%pointage%'
            LIMIT 5;
        """)
        tables = cursor.fetchall()
        print(f"\n📋 Tables pointage trouvées:")
        for table in tables:
            print(f"   • {table[0]}")
            
except Exception as e:
    print(f"\n❌ ERREUR CONNEXION: {e}")
    print("Vérifiez que PostgreSQL est démarré")

print(f"\n💡 RÉSULTAT:")
if 'postgresql' in db_config['ENGINE']:
    print("✅ Vous utilisez bien PostgreSQL !")
else:
    print("❌ Vous n'utilisez pas PostgreSQL")
