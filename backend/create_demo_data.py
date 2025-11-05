#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User
from apps.projects.models import Project, ProjectTeam
from apps.tasks.models import Task

def create_demo_data():
    print("📊 Création des données de démonstration...")
    
    # Récupérer les utilisateurs
    try:
        admin = User.objects.get(email='miguelsingcol@gmail.com')
        developer = User.objects.get(email='rakoto@company.com')
        client = User.objects.get(email='client@example.com')
    except User.DoesNotExist:
        print("❌ Erreur: Exécutez d'abord recreate_admin_and_demo.py")
        return
    
    # 1. Créer des projets
    print("\n🏗️ Création des projets...")
    
    # Projet 1
    project1 = Project.objects.create(
        name="Site E-commerce Moderne",
        description="Développement d'un site e-commerce avec React et Django",
        client=client,
        project_manager=admin,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=60),
        budget=50000.00,
        status='in_progress'
    )
    
    # Ajouter le développeur à l'équipe
    ProjectTeam.objects.create(
        project=project1,
        developer=developer,
        role='fullstack'
    )
    
    print(f"✅ Projet créé: {project1.name}")
    
    # Projet 2
    project2 = Project.objects.create(
        name="Application Mobile Gestion",
        description="App mobile pour la gestion des stocks",
        client=client,
        project_manager=admin,
        start_date=date.today() + timedelta(days=10),
        end_date=date.today() + timedelta(days=90),
        budget=75000.00,
        status='planning'
    )
    
    ProjectTeam.objects.create(
        project=project2,
        developer=developer,
        role='mobile'
    )
    
    print(f"✅ Projet créé: {project2.name}")
    
    # 2. Créer des tâches
    print("\n✅ Création des tâches...")
    
    # Tâches pour projet 1
    task1 = Task.objects.create(
        title="Setup Architecture Backend",
        description="Configurer Django REST Framework et base de données",
        project=project1,
        assigned_to=developer,
        created_by=admin,
        status='in_progress',
        priority='high',
        estimated_hours=16,
        start_date=date.today(),
        due_date=date.today() + timedelta(days=5)
    )
    
    task2 = Task.objects.create(
        title="Interface Utilisateur React",
        description="Développer les composants React pour le frontend",
        project=project1,
        assigned_to=developer,
        created_by=admin,
        status='todo',
        priority='medium',
        estimated_hours=24,
        start_date=date.today() + timedelta(days=3),
        due_date=date.today() + timedelta(days=10)
    )
    
    # Tâches pour projet 2
    task3 = Task.objects.create(
        title="Analyse des Besoins Mobile",
        description="Analyser les besoins pour l'application mobile",
        project=project2,
        assigned_to=developer,
        created_by=admin,
        status='todo',
        priority='high',
        estimated_hours=8,
        start_date=date.today() + timedelta(days=10),
        due_date=date.today() + timedelta(days=15)
    )
    
    print(f"✅ Tâche créée: {task1.title}")
    print(f"✅ Tâche créée: {task2.title}")
    print(f"✅ Tâche créée: {task3.title}")
    
    # 3. Statistiques
    print("\n📊 Données créées:")
    print(f"   - Projets: {Project.objects.count()}")
    print(f"   - Tâches: {Task.objects.count()}")
    print(f"   - Tâches assignées à {developer.first_name}: {Task.objects.filter(assigned_to=developer).count()}")
    
    print("\n🎯 MAINTENANT VOUS POUVEZ TESTER:")
    print("=" * 50)
    print("1. Connectez-vous comme ADMIN:")
    print("   Email: miguelsingcol@gmail.com")
    print("   Mot de passe: admin123")
    print("   → Voir tous les projets et tâches")
    print("   → Créer de nouveaux utilisateurs avec email")
    print()
    print("2. Connectez-vous comme DÉVELOPPEUR:")
    print("   Email: rakoto@company.com")
    print("   Mot de passe: dev123")
    print("   → Voir ses tâches assignées")
    print("   → Faire du pointage")
    print()
    print("3. Connectez-vous comme CLIENT:")
    print("   Email: client@example.com")
    print("   Mot de passe: client123")
    print("   → Voir ses projets")
    print()
    print("🚀 Le système est maintenant FONCTIONNEL avec des données de test !")

if __name__ == '__main__':
    create_demo_data()
