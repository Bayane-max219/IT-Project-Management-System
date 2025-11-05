#!/usr/bin/env python
"""
Script pour corriger les statuts des projets
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.projects.models import Project
from apps.authentication.models import User

def fix_project_status():
    """Corriger les statuts des projets"""
    print("=== Correction des Statuts des Projets ===")
    
    # 1. Vérifier les statuts actuels
    print("1. Vérification des statuts actuels...")
    projects = Project.objects.all()
    
    status_mapping = {
        'PLANIFIE': 'planning',
        'EN_COURS': 'in_progress', 
        'TERMINEE': 'completed',
        'EN_PAUSE': 'on_hold',
        'ANNULE': 'cancelled',
        'TESTS': 'testing'
    }
    
    print(f"Total projets: {projects.count()}")
    for project in projects:
        print(f"- {project.name}: '{project.status}'")
    
    # 2. Corriger les statuts
    print("\n2. Correction des statuts...")
    updated_count = 0
    
    for project in projects:
        old_status = project.status
        new_status = status_mapping.get(old_status, old_status.lower())
        
        if old_status != new_status:
            project.status = new_status
            project.save()
            print(f"✅ {project.name}: '{old_status}' -> '{new_status}'")
            updated_count += 1
        else:
            print(f"✓ {project.name}: '{old_status}' (déjà correct)")
    
    print(f"\nTotal projets mis à jour: {updated_count}")
    
    # 3. Corriger les priorités aussi
    print("\n3. Correction des priorités...")
    
    priority_mapping = {
        'BASSE': 'low',
        'MOYENNE': 'medium',
        'HAUTE': 'high', 
        'CRITIQUE': 'urgent',
        'URGENTE': 'urgent'
    }
    
    priority_updated = 0
    for project in projects:
        old_priority = project.priority
        new_priority = priority_mapping.get(old_priority, old_priority.lower())
        
        if old_priority != new_priority:
            project.priority = new_priority
            project.save()
            print(f"✅ {project.name}: priorité '{old_priority}' -> '{new_priority}'")
            priority_updated += 1
    
    print(f"Total priorités mises à jour: {priority_updated}")
    
    # 4. Vérifier le client Marie et ses projets
    print("\n4. Vérification du client Marie...")
    try:
        marie = User.objects.get(email="client@example.com")
        marie_projects = Project.objects.filter(client=marie)
        
        print(f"Marie Client (ID: {marie.id}):")
        print(f"- Email: {marie.email}")
        print(f"- Rôle: {marie.role}")
        print(f"- Projets: {marie_projects.count()}")
        
        for project in marie_projects:
            print(f"  * {project.name} (ID: {project.id})")
            print(f"    - Statut: {project.status}")
            print(f"    - Priorité: {project.priority}")
            print(f"    - Client ID: {project.client_id}")
            
    except User.DoesNotExist:
        print("❌ Client Marie non trouvé")
    
    # 5. Résumé final
    print("\n5. Résumé final...")
    
    # Compter par statut
    status_counts = {}
    for project in Project.objects.all():
        status = project.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("Répartition par statut:")
    for status, count in status_counts.items():
        print(f"  - {status}: {count} projet(s)")
    
    # Vérifier les statuts valides
    valid_statuses = [choice[0] for choice in Project.STATUS_CHOICES]
    print(f"\nStatuts valides: {valid_statuses}")
    
    invalid_projects = Project.objects.exclude(status__in=valid_statuses)
    if invalid_projects.exists():
        print(f"❌ Projets avec statuts invalides: {invalid_projects.count()}")
        for project in invalid_projects:
            print(f"  - {project.name}: '{project.status}'")
    else:
        print("✅ Tous les statuts sont valides")
    
    print("\n🎉 Correction des statuts terminée!")

if __name__ == '__main__':
    fix_project_status()
