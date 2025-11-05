#!/usr/bin/env python
"""
Debug de l'API pour le client Marie
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

def debug_client_api():
    """Debug complet de l'API client"""
    print("=== Debug API Client Marie ===")
    
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # 1. Test de connexion
    print("1. Test de connexion...")
    login_data = {
        "email": "client@example.com",
        "password": "client123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connexion réussie")
            print(f"User ID: {data.get('user', {}).get('id')}")
            print(f"Email: {data.get('user', {}).get('email')}")
            print(f"Role: {data.get('user', {}).get('role')}")
            
            token = data.get('access')
            headers = {"Authorization": f"Bearer {token}"}
            
            # 2. Test API projets
            print("\n2. Test API projets...")
            response = requests.get(f"{BASE_URL}/projects/", headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                projects = response.json()
                print(f"✅ Projets récupérés: {len(projects)}")
                for project in projects:
                    print(f"  - {project.get('name')} (ID: {project.get('id')})")
                    print(f"    Client: {project.get('client', {})}")
                    print(f"    Status: {project.get('status')}")
            else:
                print("❌ Erreur API projets")
            
            # 3. Test API profil
            print("\n3. Test API profil...")
            response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ Profil: {profile.get('email')} (ID: {profile.get('id')})")
            
        else:
            print(f"❌ Erreur de connexion: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Serveur non accessible. Démarrez avec: python manage.py runserver")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 4. Vérification directe en base
    print("\n4. Vérification directe en base...")
    from apps.authentication.models import User
    from apps.projects.models import Project
    
    try:
        marie = User.objects.get(email="client@example.com")
        projects = Project.objects.filter(client=marie)
        print(f"Marie ID en base: {marie.id}")
        print(f"Projets en base pour Marie: {projects.count()}")
        
        for project in projects:
            print(f"  - {project.name} (ID: {project.id}, Client ID: {project.client_id})")
            
        # Vérifier tous les projets
        all_projects = Project.objects.all()
        print(f"\nTous les projets en base: {all_projects.count()}")
        for project in all_projects:
            client_email = project.client.email if project.client else "Aucun"
            print(f"  - {project.name} -> Client: {client_email}")
            
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")

if __name__ == '__main__':
    debug_client_api()
