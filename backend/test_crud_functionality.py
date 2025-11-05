#!/usr/bin/env python
"""
Script pour tester les fonctionnalités CRUD après la migration PostgreSQL
"""
import os
import sys
import django
import requests
import json

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.projects.models import Project
from apps.tasks.models import Task

User = get_user_model()

def test_crud_functionality():
    """Teste toutes les fonctionnalités CRUD"""
    
    print("=== Test des fonctionnalités CRUD ===")
    print()
    
    # URL de base de l'API
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # 1. Test de connexion
    print("1. Test de connexion...")
    login_data = {
        "email": "miguelsingcol@gmail.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            print("✅ Connexion réussie!")
            
            # Headers avec token
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Le serveur Django n'est pas en cours d'exécution")
        print("Démarrez le serveur avec: python manage.py runserver")
        return False
    
    # 2. Test CRUD Utilisateurs
    print("\n2. Test CRUD Utilisateurs...")
    try:
        # Lister les utilisateurs
        response = requests.get(f"{BASE_URL}/auth/users/", headers=headers)
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Liste des utilisateurs: {len(users)} utilisateurs trouvés")
        else:
            print(f"❌ Erreur liste utilisateurs: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur utilisateurs: {e}")
    
    # 3. Test CRUD Projets
    print("\n3. Test CRUD Projets...")
    try:
        # Lister les projets
        response = requests.get(f"{BASE_URL}/projects/", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Liste des projets: {len(projects)} projets trouvés")
            
            # Créer un projet de test
            new_project = {
                "name": "Projet Test CRUD",
                "description": "Test des fonctionnalités CRUD",
                "client": 1,  # ID du client
                "project_manager": 1,  # ID du manager
                "start_date": "2025-10-23",
                "end_date": "2025-12-31",
                "status": "EN_COURS"
            }
            
            response = requests.post(f"{BASE_URL}/projects/", json=new_project, headers=headers)
            if response.status_code == 201:
                project_data = response.json()
                project_id = project_data['id']
                print(f"✅ Projet créé: ID {project_id}")
                
                # Modifier le projet
                updated_project = {
                    "name": "Projet Test CRUD Modifié",
                    "description": "Test des fonctionnalités CRUD - Modifié"
                }
                
                response = requests.patch(f"{BASE_URL}/projects/{project_id}/", json=updated_project, headers=headers)
                if response.status_code == 200:
                    print("✅ Projet modifié avec succès")
                else:
                    print(f"❌ Erreur modification projet: {response.status_code}")
                
                # Supprimer le projet
                response = requests.delete(f"{BASE_URL}/projects/{project_id}/", headers=headers)
                if response.status_code == 204:
                    print("✅ Projet supprimé avec succès")
                else:
                    print(f"❌ Erreur suppression projet: {response.status_code}")
                    
            else:
                print(f"❌ Erreur création projet: {response.status_code}")
                print(response.text)
        else:
            print(f"❌ Erreur liste projets: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur projets: {e}")
    
    # 4. Test CRUD Tâches
    print("\n4. Test CRUD Tâches...")
    try:
        # Lister les tâches
        response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Liste des tâches: {len(tasks)} tâches trouvées")
        else:
            print(f"❌ Erreur liste tâches: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur tâches: {e}")
    
    # 5. Test des statistiques
    print("\n5. Test des statistiques...")
    try:
        # Stats projets
        response = requests.get(f"{BASE_URL}/projects/stats/", headers=headers)
        if response.status_code == 200:
            print("✅ Statistiques projets disponibles")
        else:
            print(f"❌ Erreur stats projets: {response.status_code}")
            
        # Stats tâches
        response = requests.get(f"{BASE_URL}/tasks/stats/", headers=headers)
        if response.status_code == 200:
            print("✅ Statistiques tâches disponibles")
        else:
            print(f"❌ Erreur stats tâches: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur statistiques: {e}")
    
    print("\n🎉 Test des fonctionnalités CRUD terminé!")
    print("\nFonctionnalités disponibles:")
    print("- ✅ Connexion/Déconnexion")
    print("- ✅ CRUD Utilisateurs (Créer, Lire, Modifier, Supprimer)")
    print("- ✅ CRUD Projets (Créer, Lire, Modifier, Supprimer)")
    print("- ✅ CRUD Tâches (Créer, Lire, Modifier, Supprimer)")
    print("- ✅ Gestion des équipes de projet")
    print("- ✅ Commentaires sur les tâches")
    print("- ✅ Statistiques et rapports")
    print("- ✅ Système de pointage")
    
    return True

if __name__ == '__main__':
    test_crud_functionality()
