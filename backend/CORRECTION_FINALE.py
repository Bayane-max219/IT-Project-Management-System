#!/usr/bin/env python
"""
CORRECTION FINALE - Force l'assignation des projets à Marie
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

def correction_finale():
    print("🚨 CORRECTION FINALE MARIE CLIENT 🚨")
    print("=" * 50)
    
    # 1. S'assurer que Marie existe
    print("\n1. VÉRIFICATION/CRÉATION DE MARIE...")
    marie, created = User.objects.get_or_create(
        email="client@example.com",
        defaults={
            'username': 'marie_client',
            'first_name': 'Marie',
            'last_name': 'Client',
            'role': 'client',
            'is_active': True
        }
    )
    
    if created:
        marie.set_password('client123')
        marie.save()
        print(f"✅ Marie créée: {marie.email}")
    else:
        print(f"✅ Marie existe: {marie.email} (ID: {marie.id})")
    
    # 2. Supprimer TOUS les projets existants de Marie
    print(f"\n2. NETTOYAGE DES PROJETS DE MARIE...")
    old_projects = Project.objects.filter(client=marie)
    count = old_projects.count()
    old_projects.delete()
    print(f"✅ {count} anciens projets supprimés")
    
    # 3. Créer 2 nouveaux projets pour Marie
    print(f"\n3. CRÉATION DE NOUVEAUX PROJETS...")
    
    # Trouver un chef de projet
    manager = User.objects.filter(role__in=['admin', 'developer']).first()
    
    # Projet 1
    project1 = Project.objects.create(
        name="Site Web Vitrine Marie",
        description="Site web vitrine pour l'entreprise de Marie Client",
        client=marie,
        project_manager=manager,
        status="in_progress",
        priority="medium",
        start_date="2025-10-01",
        end_date="2025-12-31",
        budget=10000000,  # 10 millions Ar
        progress=45
    )
    print(f"✅ Projet 1 créé: {project1.name} (ID: {project1.id})")
    
    # Projet 2  
    project2 = Project.objects.create(
        name="Application Mobile Marie",
        description="Application mobile pour les clients de Marie",
        client=marie,
        project_manager=manager,
        status="planning",
        priority="high",
        start_date="2025-11-01", 
        end_date="2026-03-31",
        budget=18000000,  # 18 millions Ar
        progress=10
    )
    print(f"✅ Projet 2 créé: {project2.name} (ID: {project2.id})")
    
    # 4. Vérification finale
    print(f"\n4. VÉRIFICATION FINALE...")
    marie_projects = Project.objects.filter(client=marie)
    print(f"✅ Marie a maintenant {marie_projects.count()} projets:")
    
    for project in marie_projects:
        print(f"   - {project.name}")
        print(f"     ID: {project.id}")
        print(f"     Status: {project.status}")
        print(f"     Client ID: {project.client_id}")
        print(f"     Client Email: {project.client.email}")
    
    # 5. Test de la vue
    print(f"\n5. TEST DE LA VUE...")
    from apps.projects.views import ProjectListCreateView
    
    class MockRequest:
        def __init__(self, user):
            self.user = user
    
    mock_request = MockRequest(marie)
    view = ProjectListCreateView()
    view.request = mock_request
    
    queryset = view.get_queryset()
    print(f"✅ Vue retourne {queryset.count()} projets pour Marie")
    
    # 6. Instructions finales
    print(f"\n" + "=" * 50)
    print(f"🎉 CORRECTION TERMINÉE!")
    print(f"")
    print(f"Marie Client a maintenant {marie_projects.count()} projets garantis!")
    print(f"")
    print(f"POUR TESTER:")
    print(f"1. Démarrez le serveur: python manage.py runserver")
    print(f"2. Allez sur: http://localhost:3000")  
    print(f"3. Connectez-vous avec:")
    print(f"   Email: client@example.com")
    print(f"   Mot de passe: client123")
    print(f"")
    print(f"Marie DOIT maintenant voir ses {marie_projects.count()} projets!")
    print(f"Si elle ne les voit toujours pas, le problème vient du FRONTEND.")
    print(f"=" * 50)

if __name__ == '__main__':
    correction_finale()
