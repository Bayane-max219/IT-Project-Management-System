#!/usr/bin/env python
"""
Script pour réinitialiser le mot de passe d'un utilisateur
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User

def reset_password():
    """Réinitialiser le mot de passe d'un utilisateur"""
    print("\n" + "="*80)
    print("  RÉINITIALISATION DE MOT DE PASSE")
    print("="*80)
    
    # Afficher tous les utilisateurs
    print("\nUtilisateurs disponibles :\n")
    users = User.objects.all().order_by('role', 'email')
    
    for i, user in enumerate(users, 1):
        role_icon = {
            'admin': '👑',
            'developer': '💻',
            'client': '👤'
        }.get(user.role, '👤')
        
        print(f"{i}. {role_icon} {user.email} - {user.first_name} {user.last_name} ({user.role})")
    
    print("\n" + "─"*80)
    
    # Demander quel utilisateur
    try:
        choix = input("\nNuméro de l'utilisateur (ou 'q' pour quitter) : ").strip()
        
        if choix.lower() == 'q':
            print("\n❌ Annulé\n")
            return
        
        choix = int(choix)
        if choix < 1 or choix > len(users):
            print(f"\n❌ Erreur : Choisissez un numéro entre 1 et {len(users)}\n")
            return
        
        user = list(users)[choix - 1]
        
        print(f"\n✅ Utilisateur sélectionné : {user.email}")
        print(f"   Nom : {user.first_name} {user.last_name}")
        print(f"   Rôle : {user.role}")
        
        # Demander le nouveau mot de passe
        print("\n" + "─"*80)
        new_password = input("\nNouveau mot de passe (minimum 6 caractères) : ").strip()
        
        if len(new_password) < 6:
            print("\n❌ Erreur : Le mot de passe doit contenir au moins 6 caractères\n")
            return
        
        # Confirmer
        confirm = input(f"\n⚠️  Confirmer le changement de mot de passe pour {user.email} ? (oui/non) : ").strip().lower()
        
        if confirm not in ['oui', 'o', 'yes', 'y']:
            print("\n❌ Annulé\n")
            return
        
        # Changer le mot de passe
        user.set_password(new_password)
        user.save()
        
        print("\n" + "="*80)
        print("✅ MOT DE PASSE RÉINITIALISÉ AVEC SUCCÈS !")
        print("="*80)
        print(f"\nEmail : {user.email}")
        print(f"Nouveau mot de passe : {new_password}")
        print("\n⚠️  IMPORTANT : Notez bien ce mot de passe !\n")
        
    except ValueError:
        print("\n❌ Erreur : Veuillez entrer un numéro valide\n")
    except Exception as e:
        print(f"\n❌ Erreur : {str(e)}\n")

if __name__ == '__main__':
    reset_password()
