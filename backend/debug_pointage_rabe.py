#!/usr/bin/env python
"""
Script pour déboguer le pointage de Rabe Rasoamananas
"""
import os
import sys
import django
from datetime import date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.pointage.models import Pointage

User = get_user_model()

print("\n" + "="*80)
print("  DEBUG POINTAGE - RABE RASOAMANANAS")
print("="*80)

# Trouver Rabe
try:
    rabe = User.objects.get(email='rabe@company.com')
    print(f"✅ Utilisateur trouvé: {rabe.first_name} {rabe.last_name}")
    print(f"   📧 Email: {rabe.email}")
    print(f"   👤 Role: {rabe.role}")
    print(f"   ✅ Actif: {rabe.is_active}")
except User.DoesNotExist:
    print("❌ Rabe Rasoamananas non trouvé")
    print("\nUtilisateurs disponibles:")
    for user in User.objects.filter(role='developer'):
        print(f"  - {user.first_name} {user.last_name} ({user.email})")
    sys.exit(1)

print("\n" + "-"*80)
print("  POINTAGES D'AUJOURD'HUI")
print("-"*80)

today = date.today()
print(f"Date d'aujourd'hui: {today}")

# Vérifier les pointages d'aujourd'hui pour Rabe
pointages_today = Pointage.objects.filter(employee=rabe, date=today)

if pointages_today.exists():
    print(f"✅ {pointages_today.count()} pointage(s) trouvé(s) pour aujourd'hui:")
    
    for pointage in pointages_today:
        print(f"\n  📋 Pointage ID: {pointage.id}")
        print(f"     Date: {pointage.date}")
        print(f"     Arrivée: {pointage.arrival_time or '❌ Non pointé'}")
        print(f"     Départ: {pointage.departure_time or '❌ Non pointé'}")
        print(f"     Pause début: {pointage.break_start or '❌ Non pointé'}")
        print(f"     Pause fin: {pointage.break_end or '❌ Non pointé'}")
        
        if pointage.arrival_time:
            print("     ⚠️  PROBLÈME: Arrivée déjà pointée mais interface dit le contraire!")
else:
    print("❌ Aucun pointage aujourd'hui pour Rabe")

print("\n" + "-"*80)
print("  TOUS LES POINTAGES DE RABE")
print("-"*80)

all_pointages = Pointage.objects.filter(employee=rabe).order_by('-date')

if all_pointages.exists():
    print(f"Total: {all_pointages.count()} pointage(s)")
    
    for pointage in all_pointages[:5]:  # 5 derniers
        print(f"\n  📅 {pointage.date}")
        print(f"     Arrivée: {pointage.arrival_time or 'Non pointé'}")
        print(f"     Départ: {pointage.departure_time or 'Non pointé'}")
else:
    print("❌ Aucun pointage trouvé pour Rabe")

print("\n" + "="*80)
print("  SOLUTIONS")
print("="*80)

if pointages_today.exists():
    print("🔧 SOLUTION 1: Supprimer le pointage bloqué")
    print("   python manage.py shell")
    print("   >>> from apps.pointage.models import Pointage")
    print("   >>> from datetime import date")
    print(f"   >>> Pointage.objects.filter(employee__email='rabe@company.com', date=date.today()).delete()")
    
    print("\n🔧 SOLUTION 2: Compléter le pointage existant")
    print("   Le pointage existe mais l'interface ne le voit pas")
    print("   Problème de synchronisation frontend/backend")
else:
    print("🔧 Le problème vient d'ailleurs")
    print("   Vérifier les logs du serveur backend")
    print("   Vérifier la console du navigateur")

print("\n💡 COMMANDE RAPIDE POUR NETTOYER:")
print(f"   python -c \"import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); django.setup(); from apps.pointage.models import Pointage; from datetime import date; print(f'Supprimé: {{Pointage.objects.filter(employee__email=\\'rabe@company.com\\', date=date.today()).delete()[0]}} pointage(s)')\"")
