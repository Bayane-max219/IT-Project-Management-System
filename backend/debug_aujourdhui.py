#!/usr/bin/env python
"""
Vérifier les pointages d'aujourd'hui vs hier
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()
today = date.today()
yesterday = today - timedelta(days=1)

print("🔍 DIAGNOSTIC POINTAGES PAR DATE")
print("="*50)

# Total développeurs
total_devs = User.objects.filter(role='developer').count()
print(f"👥 Total développeurs: {total_devs}")

# Pointages aujourd'hui
pointages_today = Pointage.objects.filter(date=today)
print(f"\n📅 AUJOURD'HUI ({today}):")
print(f"   Pointages: {pointages_today.count()}")
for p in pointages_today:
    print(f"   • {p.employee.first_name}: {p.arrival_status} à {p.arrival_time}")

# Pointages hier
pointages_yesterday = Pointage.objects.filter(date=yesterday)
print(f"\n📅 HIER ({yesterday}):")
print(f"   Pointages: {pointages_yesterday.count()}")
for p in pointages_yesterday:
    print(f"   • {p.employee.first_name}: {p.arrival_status} à {p.arrival_time}")

# Tous les pointages récents
all_recent = Pointage.objects.filter(date__gte=yesterday).order_by('-date', '-arrival_time')
print(f"\n📋 TOUS LES POINTAGES RÉCENTS:")
for p in all_recent:
    print(f"   • {p.date} - {p.employee.first_name}: {p.arrival_status}")

# Statistiques calculées pour aujourd'hui
present_today = pointages_today.count()
late_today = pointages_today.filter(arrival_status='late').count()
attendance_rate = (present_today / total_devs * 100) if total_devs > 0 else 0

print(f"\n📊 STATISTIQUES CORRECTES POUR AUJOURD'HUI:")
print(f"   Total employés: {total_devs}")
print(f"   Présents: {present_today}")
print(f"   En retard: {late_today}")
print(f"   Taux présence: {attendance_rate:.1f}%")

# Statistiques calculées pour hier
present_yesterday = pointages_yesterday.count()
late_yesterday = pointages_yesterday.filter(arrival_status='late').count()
attendance_rate_yesterday = (present_yesterday / total_devs * 100) if total_devs > 0 else 0

print(f"\n📊 STATISTIQUES HIER (pour comparaison):")
print(f"   Total employés: {total_devs}")
print(f"   Présents: {present_yesterday}")
print(f"   En retard: {late_yesterday}")
print(f"   Taux présence: {attendance_rate_yesterday:.1f}%")
