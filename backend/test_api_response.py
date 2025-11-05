#!/usr/bin/env python
"""
Tester exactement ce que l'API renvoie
"""
import os
import sys
import django
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from django.contrib.auth import get_user_model

User = get_user_model()

print("🔍 TEST EXACT DE L'API")
print("="*80)

# Simuler l'API pointage_stats manuellement
from datetime import date
from django.db.models import Avg, Count, Sum, Q

today = date.today()
print(f"📅 Date: {today}")

# Récupérer les pointages comme le fait l'API
today_pointages = Pointage.objects.filter(date=today).select_related('employee')
print(f"📊 Pointages trouvés: {today_pointages.count()}")

# Récupérer les employés en retard comme le fait l'API
late_employees = []
for p in today_pointages.filter(arrival_status=Pointage.STATUS_LATE):
    employee_data = {
        'id': p.employee.id,
        'full_name': f"{p.employee.first_name} {p.employee.last_name}",
        'arrival_time': p.arrival_time.strftime('%H:%M') if p.arrival_time else None,
        'late_minutes': p.late_minutes,
        'late_reason': p.late_reason,
        'is_justified': p.is_justified,
        'justification_approved': p.justification_approved
    }
    late_employees.append(employee_data)

print(f"\n📋 DONNÉES EXACTES ENVOYÉES AU FRONTEND:")
print(json.dumps(late_employees, indent=2, default=str))

print(f"\n🔍 ANALYSE DÉTAILLÉE:")
for emp in late_employees:
    print(f"\n👤 {emp['full_name']}")
    print(f"   late_reason: '{emp['late_reason']}' (type: {type(emp['late_reason'])})")
    print(f"   is_justified: {emp['is_justified']}")
    
    # Vérifier si c'est None, vide, ou autre
    if emp['late_reason'] is None:
        print(f"   ❌ PROBLÈME: late_reason est None")
    elif emp['late_reason'] == '':
        print(f"   ❌ PROBLÈME: late_reason est vide")
    elif emp['late_reason']:
        print(f"   ✅ OK: late_reason contient '{emp['late_reason']}'")
    else:
        print(f"   ❌ PROBLÈME: late_reason est falsy: {repr(emp['late_reason'])}")

print(f"\n💡 SI late_reason CONTIENT LES BONNES DONNÉES:")
print("   Le problème est dans le frontend (AdminDashboard.js)")
print("   Vérifier que le frontend utilise bien 'late_reason'")

print(f"\n💡 SI late_reason EST None/vide:")
print("   Le problème est dans le backend")
print("   Les justifications ne sont pas sauvegardées correctement")
