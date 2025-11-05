#!/usr/bin/env python
"""
Script pour voir et gérer les mots de passe des développeurs
Projet IT Management - PostgreSQL
"""
import os
import sys
import django
from getpass import getpass

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

User = get_user_model()

def afficher_tous_les_developpeurs():
    """Afficher tous les développeurs avec leurs informations"""
    print("\n" + "="*80)
    print("  LISTE DES DÉVELOPPEURS")
    print("="*80)
    
    developers = User.objects.filter(role='developer')
    
    if not developers.exists():
        print("❌ Aucun développeur trouvé")
        return
    
    print(f"Total: {developers.count()} développeur(s)\n")
    
    for i, dev in enumerate(developers, 1):
        print(f"{i}. {dev.first_name} {dev.last_name}")
        print(f"   📧 Email: {dev.email}")
        print(f"   👤 Username: {dev.username}")
        print(f"   🔑 Mot de passe hashé: {dev.password[:50]}...")
        print(f"   📅 Créé le: {dev.date_joined.strftime('%d/%m/%Y %H:%M')}")
        print(f"   ✅ Actif: {'Oui' if dev.is_active else 'Non'}")
        print("-" * 60)

def tester_mot_de_passe():
    """Tester si un mot de passe correspond à un utilisateur"""
    print("\n" + "="*80)
    print("  TEST DE MOT DE PASSE")
    print("="*80)
    
    # Choisir l'utilisateur
    developers = User.objects.filter(role='developer')
    
    if not developers.exists():
        print("❌ Aucun développeur trouvé")
        return
    
    print("Développeurs disponibles:")
    for i, dev in enumerate(developers, 1):
        print(f"{i}. {dev.first_name} {dev.last_name} ({dev.email})")
    
    try:
        choix = int(input("\nChoisissez un développeur (numéro): ")) - 1
        if choix < 0 or choix >= len(developers):
            print("❌ Choix invalide")
            return
        
        user = developers[choix]
        print(f"\n👤 Utilisateur sélectionné: {user.first_name} {user.last_name}")
        
        # Demander le mot de passe à tester
        password_test = getpass("🔑 Entrez le mot de passe à tester: ")
        
        # Tester le mot de passe
        if user.check_password(password_test):
            print("✅ MOT DE PASSE CORRECT !")
        else:
            print("❌ MOT DE PASSE INCORRECT")
            
    except (ValueError, IndexError):
        print("❌ Entrée invalide")

def reinitialiser_mot_de_passe():
    """Réinitialiser le mot de passe d'un développeur"""
    print("\n" + "="*80)
    print("  RÉINITIALISATION DE MOT DE PASSE")
    print("="*80)
    
    # Choisir l'utilisateur
    developers = User.objects.filter(role='developer')
    
    if not developers.exists():
        print("❌ Aucun développeur trouvé")
        return
    
    print("Développeurs disponibles:")
    for i, dev in enumerate(developers, 1):
        print(f"{i}. {dev.first_name} {dev.last_name} ({dev.email})")
    
    try:
        choix = int(input("\nChoisissez un développeur (numéro): ")) - 1
        if choix < 0 or choix >= len(developers):
            print("❌ Choix invalide")
            return
        
        user = developers[choix]
        print(f"\n👤 Utilisateur sélectionné: {user.first_name} {user.last_name}")
        
        # Demander le nouveau mot de passe
        nouveau_mdp = getpass("🔑 Nouveau mot de passe: ")
        confirmation = getpass("🔑 Confirmez le mot de passe: ")
        
        if nouveau_mdp != confirmation:
            print("❌ Les mots de passe ne correspondent pas")
            return
        
        if len(nouveau_mdp) < 6:
            print("❌ Le mot de passe doit faire au moins 6 caractères")
            return
        
        # Changer le mot de passe
        user.set_password(nouveau_mdp)
        user.save()
        
        print(f"✅ Mot de passe changé avec succès pour {user.first_name} {user.last_name}")
        print(f"📧 Email: {user.email}")
        print(f"🔑 Nouveau mot de passe: {nouveau_mdp}")
        
    except (ValueError, IndexError):
        print("❌ Entrée invalide")

def creer_developpeur():
    """Créer un nouveau développeur"""
    print("\n" + "="*80)
    print("  CRÉER UN NOUVEAU DÉVELOPPEUR")
    print("="*80)
    
    try:
        # Informations de base
        first_name = input("Prénom: ").strip()
        last_name = input("Nom: ").strip()
        email = input("Email: ").strip()
        username = input("Username (optionnel, sinon = email): ").strip()
        
        if not username:
            username = email
        
        # Vérifier si l'email existe déjà
        if User.objects.filter(email=email).exists():
            print(f"❌ Un utilisateur avec l'email {email} existe déjà")
            return
        
        # Mot de passe
        password = getpass("Mot de passe: ")
        confirmation = getpass("Confirmez le mot de passe: ")
        
        if password != confirmation:
            print("❌ Les mots de passe ne correspondent pas")
            return
        
        if len(password) < 6:
            print("❌ Le mot de passe doit faire au moins 6 caractères")
            return
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='developer'
        )
        
        print(f"✅ Développeur créé avec succès !")
        print(f"👤 Nom: {user.first_name} {user.last_name}")
        print(f"📧 Email: {user.email}")
        print(f"👤 Username: {user.username}")
        print(f"🔑 Mot de passe: {password}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")

def menu_principal():
    """Menu principal"""
    while True:
        print("\n" + "="*80)
        print("  GESTION DES DÉVELOPPEURS - POSTGRESQL")
        print("="*80)
        print("1. 📋 Voir tous les développeurs")
        print("2. 🔍 Tester un mot de passe")
        print("3. 🔄 Réinitialiser un mot de passe")
        print("4. ➕ Créer un nouveau développeur")
        print("5. ❌ Quitter")
        print("-" * 80)
        
        choix = input("Votre choix (1-5): ").strip()
        
        if choix == '1':
            afficher_tous_les_developpeurs()
        elif choix == '2':
            tester_mot_de_passe()
        elif choix == '3':
            reinitialiser_mot_de_passe()
        elif choix == '4':
            creer_developpeur()
        elif choix == '5':
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide")
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == '__main__':
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
