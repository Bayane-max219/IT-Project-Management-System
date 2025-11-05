#!/usr/bin/env python
"""
Diagnostic ultra-simple pour Marie Client
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User
from apps.projects.models import Project

print("=== DIAGNOSTIC SIMPLE MARIE CLIENT ===")

# 1. Trouver Marie
print("\n1. RECHERCHE DE MARIE...")
try:
    marie = User.objects.get(email="client@example.com")
    print(f"✅ Marie trouvée:")
    print(f"   ID: {marie.id}")
    print(f"   Email: {marie.email}")
    print(f"   Nom: {marie.first_name} {marie.last_name}")
    print(f"   Rôle: {marie.role}")
    print(f"   Active: {marie.is_active}")
except User.DoesNotExist:
    print("❌ Marie non trouvée!")
    print("\nCréation de Marie...")
    marie = User.objects.create_user(
        username="marie_client",
        email="client@example.com", 
        first_name="Marie",
        last_name="Client",
        role="client",
        password="client123"
    )
    print(f"✅ Marie créée: ID {marie.id}")

# 2. Chercher TOUS les projets
print(f"\n2. TOUS LES PROJETS EN BASE...")
all_projects = Project.objects.all()
print(f"Total projets: {all_projects.count()}")

for project in all_projects:
    client_info = f"{project.client.email}" if project.client else "AUCUN CLIENT"
    print(f"   - {project.name} (ID: {project.id})")
    print(f"     Client: {client_info}")
    print(f"     Status: '{project.status}'")

# 3. Projets de Marie spécifiquement
print(f"\n3. PROJETS DE MARIE (ID: {marie.id})...")
marie_projects = Project.objects.filter(client=marie)
print(f"Projets de Marie: {marie_projects.count()}")

for project in marie_projects:
    print(f"   ✅ {project.name}")
    print(f"      Status: '{project.status}'")
    print(f"      Client ID: {project.client_id}")

# 4. Si Marie n'a pas de projets, en assigner
if marie_projects.count() == 0:
    print(f"\n4. ASSIGNATION DE PROJETS À MARIE...")
    
    # Prendre les 2 premiers projets et les assigner à Marie
    projects_to_assign = Project.objects.all()[:2]
    
    for project in projects_to_assign:
        old_client = project.client.email if project.client else "Aucun"
        project.client = marie
        project.save()
        print(f"   ✅ {project.name}: {old_client} → {marie.email}")
    
    # Re-vérifier
    marie_projects = Project.objects.filter(client=marie)
    print(f"   Marie a maintenant {marie_projects.count()} projets")

# 5. Vérifier les statuts
print(f"\n5. VÉRIFICATION DES STATUTS...")
valid_statuses = ['planning', 'in_progress', 'testing', 'completed', 'on_hold', 'cancelled']

for project in marie_projects:
    if project.status not in valid_statuses:
        print(f"   ❌ {project.name}: statut invalide '{project.status}'")
        # Corriger le statut
        if project.status in ['PLANIFIE', 'planifie']:
            project.status = 'planning'
        elif project.status in ['EN_COURS', 'en_cours', 'in_progress']:
            project.status = 'in_progress'
        elif project.status in ['TERMINEE', 'terminee']:
            project.status = 'completed'
        else:
            project.status = 'planning'  # Par défaut
        
        project.save()
        print(f"   ✅ Corrigé vers: '{project.status}'")
    else:
        print(f"   ✅ {project.name}: statut OK '{project.status}'")

# 6. RÉSUMÉ FINAL
print(f"\n6. RÉSUMÉ FINAL...")
marie_final = Project.objects.filter(client=marie)
print(f"Marie Client (ID: {marie.id}) a {marie_final.count()} projets:")

for project in marie_final:
    print(f"   - {project.name} (ID: {project.id}, Status: {project.status})")

print(f"\n🎯 MARIE DEVRAIT MAINTENANT VOIR {marie_final.count()} PROJETS!")
print(f"\nPour tester:")
print(f"1. Démarrez le serveur: python manage.py runserver")
print(f"2. Connectez-vous avec: client@example.com / client123")
