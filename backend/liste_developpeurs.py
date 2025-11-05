#!/usr/bin/env python
"""
Script simple pour lister tous les développeurs
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "="*80)
print("  LISTE DES DÉVELOPPEURS - POSTGRESQL")
print("="*80)

# Récupérer tous les développeurs
developers = User.objects.filter(role='developer')

if not developers.exists():
    print("❌ Aucun développeur trouvé dans la base PostgreSQL")
    print("\nPour créer un développeur, utilisez:")
    print("python voir_mot_de_passe_dev.py")
else:
    print(f"Total: {developers.count()} développeur(s)\n")
    
    for i, dev in enumerate(developers, 1):
        print(f"{i}. 👤 {dev.first_name} {dev.last_name}")
        print(f"   📧 Email: {dev.email}")
        print(f"   🔑 Username: {dev.username}")
        print(f"   📅 Créé: {dev.date_joined.strftime('%d/%m/%Y à %H:%M')}")
        print(f"   ✅ Actif: {'Oui' if dev.is_active else 'Non'}")
        print(f"   🔐 Hash mot de passe: {dev.password[:30]}...")
        print("-" * 60)

print("\n💡 Pour tester ou changer un mot de passe:")
print("   python voir_mot_de_passe_dev.py")

print("\n📋 Informations de connexion PostgreSQL:")
print("   Base: it_project_management")
print("   User: postgres")
print("   Pass: postgres")
print("   Host: 127.0.0.1:5432")
