#!/usr/bin/env python
"""
Script pour corriger l'assignation des projets aux clients
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

def fix_client_projects():
    """Corriger l'assignation des projets aux clients"""
    print("=== Correction de l'Assignation des Projets ===")
    
    # 1. Vérifier les clients existants
    print("1. Vérification des clients...")
    clients = User.objects.filter(role='client')
    print(f"   Clients trouvés: {clients.count()}")
    
    for client in clients:
        projects_count = Project.objects.filter(client=client).count()
        print(f"   - {client.email} ({client.first_name} {client.last_name}): {projects_count} projet(s)")
    
    # 2. Vérifier les projets sans client
    print("\n2. Vérification des projets sans client...")
    projects_without_client = Project.objects.filter(client__isnull=True)
    print(f"   Projets sans client: {projects_without_client.count()}")
    
    for project in projects_without_client:
        print(f"   - {project.name} (ID: {project.id})")
    
    # 3. Assigner les projets existants au client Marie si nécessaire
    print("\n3. Assignation des projets au client Marie...")
    
    try:
        marie_client = User.objects.get(email="client@example.com", role="client")
        print(f"   Client Marie trouvé: {marie_client.email}")
        
        # Assigner les projets sans client à Marie
        if projects_without_client.exists():
            updated_count = projects_without_client.update(client=marie_client)
            print(f"   ✅ {updated_count} projet(s) assigné(s) à Marie")
        
        # Vérifier le résultat
        marie_projects = Project.objects.filter(client=marie_client)
        print(f"   Marie a maintenant {marie_projects.count()} projet(s)")
        
    except User.DoesNotExist:
        print("   ❌ Client Marie non trouvé")
        
        # Créer le client Marie si nécessaire
        print("   Création du client Marie...")
        marie_client = User.objects.create_user(
            username="marie_client",
            email="client@example.com",
            first_name="Marie",
            last_name="Client",
            role="client",
            password="client123"
        )
        print(f"   ✅ Client Marie créé: {marie_client.email}")
        
        # Assigner les projets
        if projects_without_client.exists():
            updated_count = projects_without_client.update(client=marie_client)
            print(f"   ✅ {updated_count} projet(s) assigné(s) à Marie")
    
    # 4. Créer des projets de démonstration si nécessaire
    print("\n4. Création de projets de démonstration...")
    
    marie_projects = Project.objects.filter(client=marie_client)
    if marie_projects.count() < 2:
        # Trouver un chef de projet
        project_manager = User.objects.filter(role='developer').first()
        if not project_manager:
            project_manager = User.objects.filter(role='admin').first()
        
        # Créer des projets de démonstration
        demo_projects = [
            {
                'name': 'Site Web Vitrine',
                'description': 'Développement d\'un site web vitrine pour présenter l\'entreprise',
                'status': 'EN_COURS',
                'priority': 'HAUTE',
                'start_date': '2025-10-01',
                'end_date': '2025-12-15',
                'budget': 25000,
                'progress': 35
            },
            {
                'name': 'Application Mobile',
                'description': 'Développement d\'une application mobile pour les clients',
                'status': 'PLANIFIE',
                'priority': 'MOYENNE',
                'start_date': '2025-11-01',
                'end_date': '2026-03-31',
                'budget': 45000,
                'progress': 0
            }
        ]
        
        created_count = 0
        for project_data in demo_projects:
            # Vérifier si le projet existe déjà
            if not Project.objects.filter(name=project_data['name'], client=marie_client).exists():
                project = Project.objects.create(
                    client=marie_client,
                    project_manager=project_manager,
                    **project_data
                )
                print(f"   ✅ Projet créé: {project.name}")
                created_count += 1
        
        print(f"   Total projets créés: {created_count}")
    
    # 5. Résumé final
    print("\n5. Résumé final...")
    
    # Statistiques finales
    total_clients = User.objects.filter(role='client').count()
    total_projects = Project.objects.count()
    projects_with_client = Project.objects.filter(client__isnull=False).count()
    
    print(f"   - Total clients: {total_clients}")
    print(f"   - Total projets: {total_projects}")
    print(f"   - Projets avec client assigné: {projects_with_client}")
    
    # Détail par client
    for client in User.objects.filter(role='client'):
        client_projects = Project.objects.filter(client=client)
        print(f"   - {client.email}: {client_projects.count()} projet(s)")
        for project in client_projects:
            print(f"     * {project.name} ({project.status})")
    
    print("\n🎉 Correction terminée!")
    print("\nMaintenant, le client Marie devrait voir ses projets quand elle se connecte.")
    print("Testez avec: python test_client_projects.py")

if __name__ == '__main__':
    fix_client_projects()
