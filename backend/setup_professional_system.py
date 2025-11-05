#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User, RegistrationKey
from apps.projects.models import Project, ProjectTeam
from apps.tasks.models import Task
from apps.pointage.models import Pointage

def setup_professional_system():
    print("🔧 Configuration du système professionnel...")
    
    # 1. Supprimer tous les comptes de test (sauf l'admin principal)
    print("\n🗑️ Suppression des comptes de test...")
    
    # Garder seulement l'admin principal
    admin_email = 'miguelsingcol@gmail.com'
    test_users = User.objects.exclude(email=admin_email)
    
    print(f"📊 Comptes à supprimer: {test_users.count()}")
    for user in test_users:
        print(f"  - Suppression: {user.email} ({user.get_role_display()})")
    
    # Supprimer les données liées en cascade
    test_users.delete()
    
    # 2. Nettoyer les données de test
    print("\n🧹 Nettoyage des données de test...")
    Task.objects.all().delete()
    ProjectTeam.objects.all().delete()
    Project.objects.all().delete()
    Pointage.objects.all().delete()
    RegistrationKey.objects.all().delete()
    
    # 3. Vérifier l'admin principal
    print("\n👤 Vérification de l'administrateur principal...")
    try:
        admin = User.objects.get(email=admin_email)
        admin.role = 'admin'
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        print(f"✅ Admin configuré: {admin.email}")
    except User.DoesNotExist:
        print(f"❌ Admin {admin_email} non trouvé!")
        return
    
    # 4. Créer les paramètres de pointage par défaut
    print("\n⏰ Configuration du système de pointage...")
    from apps.pointage.models import PointageSettings
    
    # Supprimer les anciens paramètres
    PointageSettings.objects.all().delete()
    
    # Créer les nouveaux paramètres
    from datetime import time
    settings = PointageSettings.objects.create(
        expected_arrival_time=time(8, 0),  # 8h00
        expected_departure_time=time(17, 0),  # 17h00
        break_duration_minutes=60,  # 1 heure de pause
        tolerance_minutes=15,  # 15 minutes de tolérance
        working_days='1,2,3,4,5'  # Lundi à Vendredi
    )
    print(f"✅ Paramètres de pointage créés:")
    print(f"   - Horaires: {settings.expected_arrival_time} - {settings.expected_departure_time}")
    print(f"   - Pause: {settings.break_duration_minutes} minutes")
    print(f"   - Tolérance: {settings.tolerance_minutes} minutes")
    
    print("\n🎉 Système professionnel configuré avec succès!")
    print("\n📋 État final:")
    print(f"   - Administrateurs: {User.objects.filter(role='admin').count()}")
    print(f"   - Développeurs: {User.objects.filter(role='developer').count()}")
    print(f"   - Clients: {User.objects.filter(role='client').count()}")
    print(f"   - Projets: {Project.objects.count()}")
    print(f"   - Tâches: {Task.objects.count()}")
    
    print("\n🚀 Le système est maintenant prêt pour la production!")
    print("   - Plus de comptes de test")
    print("   - Interface de connexion professionnelle")
    print("   - Système d'invitation par email")
    print("   - Pointage avec heures normales")

if __name__ == '__main__':
    setup_professional_system()
