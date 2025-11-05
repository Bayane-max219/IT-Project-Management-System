#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User
from django.contrib.auth.hashers import make_password

def recreate_admin_and_demo():
    print("🔧 Recréation de l'admin et comptes de démonstration...")
    
    # 1. Créer l'admin principal
    print("\n👤 Création de l'administrateur principal...")
    
    # Supprimer l'ancien s'il existe
    User.objects.filter(email='miguelsingcol@gmail.com').delete()
    
    admin = User.objects.create_user(
        username='admin_miguel',
        email='miguelsingcol@gmail.com',
        first_name='Miguel',
        last_name='Admin',
        role='admin',
        password='admin123'  # Mot de passe simple pour test
    )
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    
    print(f"✅ Admin créé: {admin.email}")
    print(f"🔑 Mot de passe: admin123")
    
    # 2. Créer un développeur de démonstration
    print("\n👨‍💻 Création d'un développeur de démonstration...")
    
    User.objects.filter(email='rakoto@company.com').delete()
    
    developer = User.objects.create_user(
        username='rakoto_dev',
        email='rakoto@company.com',
        first_name='Rakoto',
        last_name='Developer',
        role='developer',
        password='dev123',
        phone='+261 34 12 345 67'
    )
    
    print(f"✅ Développeur créé: {developer.email}")
    print(f"🔑 Mot de passe: dev123")
    
    # 3. Créer un client de démonstration
    print("\n👤 Création d'un client de démonstration...")
    
    User.objects.filter(email='client@example.com').delete()
    
    client = User.objects.create_user(
        username='client_demo',
        email='client@example.com',
        first_name='Marie',
        last_name='Client',
        role='client',
        password='client123',
        phone='+261 34 98 765 43'
    )
    
    print(f"✅ Client créé: {client.email}")
    print(f"🔑 Mot de passe: client123")
    
    # 4. Statistiques
    print("\n📊 État du système:")
    print(f"   - Administrateurs: {User.objects.filter(role='admin').count()}")
    print(f"   - Développeurs: {User.objects.filter(role='developer').count()}")
    print(f"   - Clients: {User.objects.filter(role='client').count()}")
    
    print("\n🎯 COMPTES DE CONNEXION DISPONIBLES:")
    print("=" * 50)
    print("🔴 ADMINISTRATEUR:")
    print("   Email: miguelsingcol@gmail.com")
    print("   Mot de passe: admin123")
    print()
    print("🟡 DÉVELOPPEUR:")
    print("   Email: rakoto@company.com")
    print("   Mot de passe: dev123")
    print()
    print("🟢 CLIENT:")
    print("   Email: client@example.com")
    print("   Mot de passe: client123")
    print()
    print("🚀 Maintenant vous pouvez vous connecter !")
    print("   L'admin peut créer de nouveaux comptes via l'interface")
    print("   Et envoyer des emails avec les identifiants")

if __name__ == '__main__':
    recreate_admin_and_demo()
