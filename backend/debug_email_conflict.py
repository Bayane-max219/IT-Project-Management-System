#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User

def debug_email_conflict():
    """Débugger le conflit d'email"""
    email = 'singcolmiguel9@gmail.com'
    
    print(f"🔍 RECHERCHE EMAIL: {email}")
    print("="*60)
    
    # Recherche exacte
    users = User.objects.filter(email=email)
    print(f"📧 Utilisateurs trouvés avec cet email: {users.count()}")
    
    for user in users:
        print(f"\n👤 UTILISATEUR TROUVÉ:")
        print(f"   - ID: {user.id}")
        print(f"   - Username: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Prénom: {user.first_name}")
        print(f"   - Nom: {user.last_name}")
        print(f"   - Rôle: {user.role}")
        print(f"   - Actif: {user.is_active}")
        print(f"   - Créé le: {user.created_at}")
        print(f"   - Modifié le: {user.updated_at}")
    
    # Recherche insensible à la casse
    users_icase = User.objects.filter(email__iexact=email)
    print(f"\n📧 Recherche insensible à la casse: {users_icase.count()}")
    
    # Recherche avec LIKE
    users_like = User.objects.filter(email__icontains='singcolmiguel9')
    print(f"📧 Recherche avec LIKE: {users_like.count()}")
    
    for user in users_like:
        print(f"   - {user.email} ({user.username})")
    
    # Tous les utilisateurs pour comparaison
    all_users = User.objects.all()
    print(f"\n📊 TOTAL UTILISATEURS: {all_users.count()}")
    
    print(f"\n📋 LISTE COMPLÈTE DES EMAILS:")
    for user in all_users.order_by('email'):
        status = "✅ Actif" if user.is_active else "❌ Inactif"
        print(f"   - {user.email} ({user.username}) - {status}")

if __name__ == '__main__':
    debug_email_conflict()
