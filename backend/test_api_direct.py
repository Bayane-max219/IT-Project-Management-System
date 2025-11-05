#!/usr/bin/env python
"""
Test API direct sans serveur
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from apps.authentication.models import User
from apps.projects.models import Project
import json

print("=== TEST API DIRECT ===")

# 1. Créer un client de test Django
client = Client()

# 2. Vérifier Marie en base
print("\n1. Vérification Marie en base...")
try:
    marie = User.objects.get(email="client@example.com")
    projects = Project.objects.filter(client=marie)
    print(f"✅ Marie: {marie.email} (ID: {marie.id})")
    print(f"✅ Projets: {projects.count()}")
    
    for project in projects:
        print(f"   - {project.name} (Status: {project.status})")
        
except User.DoesNotExist:
    print("❌ Marie non trouvée")
    sys.exit(1)

# 3. Test de connexion via API Django
print("\n2. Test de connexion API...")
login_data = {
    "email": "client@example.com",
    "password": "client123"
}

response = client.post('/api/auth/login/', 
                     data=json.dumps(login_data),
                     content_type='application/json')

print(f"Status connexion: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print("✅ Connexion API réussie")
    
    user_data = data.get('user', {})
    print(f"User ID: {user_data.get('id')}")
    print(f"Email: {user_data.get('email')}")
    print(f"Role: {user_data.get('role')}")
    
    # Récupérer le token
    token = data.get('access')
    
    # 4. Test API projets
    print("\n3. Test API projets...")
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    response = client.get('/api/projects/', **headers)
    print(f"Status projets: {response.status_code}")
    
    if response.status_code == 200:
        projects_data = response.json()
        print(f"✅ Projets API: {len(projects_data)}")
        
        if len(projects_data) > 0:
            print("PROJETS RETOURNÉS PAR L'API:")
            for project in projects_data:
                print(f"   - {project.get('name')} (ID: {project.get('id')})")
                print(f"     Status: {project.get('status')}")
                print(f"     Client: {project.get('client', {})}")
            
            print("\n🎉 SUCCESS! L'API retourne les projets de Marie!")
            print("\n🔍 Le problème vient donc du FRONTEND, pas du backend")
            print("\nSolutions possibles:")
            print("1. Vider le cache du navigateur")
            print("2. Redémarrer le serveur frontend")
            print("3. Vérifier la console du navigateur pour les erreurs")
            
        else:
            print("\n❌ L'API ne retourne aucun projet")
            print("Le problème vient du backend - filtrage incorrect")
            
    else:
        print(f"❌ Erreur API projets: {response.content}")
        
else:
    print(f"❌ Erreur connexion: {response.content}")

# 5. Test direct du filtrage
print("\n4. Test direct du filtrage...")
from apps.projects.views import ProjectListCreateView

# Simuler la requête
class MockRequest:
    def __init__(self, user):
        self.user = user

mock_request = MockRequest(marie)
view = ProjectListCreateView()
view.request = mock_request

queryset = view.get_queryset()
print(f"Queryset direct: {queryset.count()} projets")

for project in queryset:
    print(f"   - {project.name}")

print(f"\n🎯 DIAGNOSTIC COMPLET TERMINÉ")
print(f"Marie devrait voir {queryset.count()} projets dans l'interface")
