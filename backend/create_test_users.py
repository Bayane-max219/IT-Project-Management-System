#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User

def create_test_users():
    # Admin
    if not User.objects.filter(email='admin@company.com').exists():
        User.objects.create_user(
            username='admin',
            email='admin@company.com',
            password='admin123',
            first_name='Admin',
            last_name='System',
            role='admin',
            is_superuser=True,
            is_staff=True
        )
        print("✅ Utilisateur Admin créé: admin@company.com / admin123")
    else:
        print("ℹ️ Utilisateur Admin existe déjà")

    # Développeur
    if not User.objects.filter(email='rakoto@company.com').exists():
        User.objects.create_user(
            username='rakoto',
            email='rakoto@company.com',
            password='dev123',
            first_name='Rakoto',
            last_name='Developer',
            role='developer'
        )
        print("✅ Utilisateur Développeur créé: rakoto@company.com / dev123")
    else:
        print("ℹ️ Utilisateur Développeur existe déjà")

    # Client
    if not User.objects.filter(email='client@example.com').exists():
        User.objects.create_user(
            username='client',
            email='client@example.com',
            password='client123',
            first_name='Client',
            last_name='Test',
            role='client'
        )
        print("✅ Utilisateur Client créé: client@example.com / client123")
    else:
        print("ℹ️ Utilisateur Client existe déjà")

    print("\n🎉 Tous les comptes de test sont prêts!")
    print("\n📋 Comptes disponibles:")
    print("👤 Admin: admin@company.com / admin123")
    print("👨‍💻 Développeur: rakoto@company.com / dev123")
    print("👥 Client: client@example.com / client123")

if __name__ == '__main__':
    create_test_users()
