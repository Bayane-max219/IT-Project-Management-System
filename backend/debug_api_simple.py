#!/usr/bin/env python
"""
Test simple de l'API
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()
today = date.today()

print("🔍 TEST API SIMPLE")
print("="*40)

# Données de base
total_devs = User.objects.filter(role='developer').count()
pointages_today = Pointage.objects.filter(date=today)
present_count = pointages_today.count()
late_count = pointages_today.filter(arrival_status='late').count()

print(f"📊 BACKEND CALCULS:")
print(f"   Total développeurs: {total_devs}")
print(f"   Pointages aujourd'hui: {present_count}")
print(f"   En retard: {late_count}")
print(f"   Taux présence: {(present_count/total_devs*100) if total_devs > 0 else 0:.1f}%")

print(f"\n👥 DÉVELOPPEURS:")
for dev in User.objects.filter(role='developer'):
    pointage = pointages_today.filter(employee=dev).first()
    status = "Présent" if pointage else "Absent"
    print(f"   • {dev.first_name} {dev.last_name}: {status}")

print(f"\n📋 POINTAGES DÉTAILLÉS:")
for p in pointages_today:
    print(f"   • {p.employee.first_name}: {p.arrival_status} à {p.arrival_time}")
