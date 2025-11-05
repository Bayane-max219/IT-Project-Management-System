#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User
from apps.tasks.models import Task

def check_task_assignments():
    print("🔍 Vérification des assignations de tâches...")
    
    # Lister tous les utilisateurs développeurs
    developers = User.objects.filter(role='developer')
    print(f"\n👨‍💻 Développeurs dans la base de données:")
    for dev in developers:
        print(f"  - ID: {dev.id}, Email: {dev.email}, Nom: {dev.first_name} {dev.last_name}")
    
    # Lister toutes les tâches et leurs assignations
    tasks = Task.objects.all().select_related('assigned_to', 'project')
    print(f"\n✅ Tâches dans la base de données ({tasks.count()}):")
    for task in tasks:
        assigned_name = f"{task.assigned_to.first_name} {task.assigned_to.last_name}" if task.assigned_to else "Non assigné"
        assigned_email = task.assigned_to.email if task.assigned_to else "N/A"
        print(f"  - {task.title}")
        print(f"    Projet: {task.project.name}")
        print(f"    Assigné à: {assigned_name} ({assigned_email})")
        print(f"    Statut: {task.status}")
        print()
    
    # Vérifier spécifiquement pour Rakoto
    rakoto_users = User.objects.filter(first_name__icontains='rakoto')
    print(f"🔍 Utilisateurs avec 'Rakoto' dans le nom:")
    for user in rakoto_users:
        print(f"  - ID: {user.id}, Email: {user.email}, Nom: {user.first_name} {user.last_name}")
        tasks_assigned = Task.objects.filter(assigned_to=user)
        print(f"    Tâches assignées: {tasks_assigned.count()}")
        for task in tasks_assigned:
            print(f"      * {task.title} ({task.status})")
        print()

if __name__ == '__main__':
    check_task_assignments()
