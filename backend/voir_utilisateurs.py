#!/usr/bin/env python
"""
Script pour voir tous les utilisateurs dans la base de données
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User

def afficher_utilisateurs():
    """Afficher tous les utilisateurs avec leurs informations"""
    print("\n" + "="*80)
    print("  LISTE DES UTILISATEURS")
    print("="*80)
    
    users = User.objects.all().order_by('role', 'email')
    
    if not users:
        print("❌ Aucun utilisateur trouvé dans la base de données")
        return
    
    print(f"\nTotal : {users.count()} utilisateur(s)\n")
    
    # Grouper par rôle
    roles = {
        'admin': [],
        'developer': [],
        'client': []
    }
    
    for user in users:
        roles[user.role].append(user)
    
    # Afficher les admins
    if roles['admin']:
        print("\n" + "─"*80)
        print("👑 ADMINISTRATEURS")
        print("─"*80)
        for user in roles['admin']:
            print(f"\n  ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Username: {user.username}")
            print(f"  Nom: {user.first_name} {user.last_name}")
            print(f"  Actif: {'✅ Oui' if user.is_active else '❌ Non'}")
            print(f"  Dernière connexion: {user.last_login or 'Jamais'}")
    
    # Afficher les développeurs
    if roles['developer']:
        print("\n" + "─"*80)
        print("💻 DÉVELOPPEURS")
        print("─"*80)
        for user in roles['developer']:
            print(f"\n  ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Username: {user.username}")
            print(f"  Nom: {user.first_name} {user.last_name}")
            print(f"  Actif: {'✅ Oui' if user.is_active else '❌ Non'}")
            print(f"  Dernière connexion: {user.last_login or 'Jamais'}")
    
    # Afficher les clients
    if roles['client']:
        print("\n" + "─"*80)
        print("👤 CLIENTS")
        print("─"*80)
        for user in roles['client']:
            print(f"\n  ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Username: {user.username}")
            print(f"  Nom: {user.first_name} {user.last_name}")
            print(f"  Actif: {'✅ Oui' if user.is_active else '❌ Non'}")
            print(f"  Dernière connexion: {user.last_login or 'Jamais'}")
    
    print("\n" + "="*80)
    print("\n⚠️  NOTE: Les mots de passe sont hashés et ne peuvent pas être affichés.")
    print("   Pour réinitialiser un mot de passe, utilisez le script 'reset_password.py'\n")

if __name__ == '__main__':
    afficher_utilisateurs()
