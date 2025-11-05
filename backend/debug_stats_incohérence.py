#!/usr/bin/env python
"""
Diagnostic des incohérences entre les statistiques
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from django.contrib.auth import get_user_model
from datetime import date
import json

User = get_user_model()
today = date.today()

print("🔍 DIAGNOSTIC INCOHÉRENCES STATISTIQUES")
print("="*60)

# 1. Données de base
total_employees = User.objects.filter(role='developer').count()
print(f"👥 Total développeurs: {total_employees}")

# 2. Pointages aujourd'hui
today_pointages = Pointage.objects.filter(date=today)
present_today = today_pointages.count()
print(f"📊 Pointages aujourd'hui: {present_today}")

# 3. Détail des pointages
print(f"\n📋 DÉTAIL DES POINTAGES:")
for p in today_pointages:
    print(f"   • {p.employee.first_name} {p.employee.last_name}")
    print(f"     - Arrivée: {p.arrival_time}")
    print(f"     - Statut: {p.arrival_status}")
    print(f"     - Retard: {p.late_minutes} min")
    print(f"     - Raison: '{p.late_reason}'")
    print(f"     - Justifié: {p.is_justified}")

# 4. Statistiques calculées
late_today = today_pointages.filter(arrival_status=Pointage.STATUS_LATE).count()
absent_today = total_employees - present_today
attendance_rate = round((present_today / total_employees * 100) if total_employees > 0 else 0, 1)

print(f"\n📊 STATISTIQUES CALCULÉES:")
print(f"   • Présents: {present_today}")
print(f"   • En retard: {late_today}")
print(f"   • Absents: {absent_today}")
print(f"   • Taux présence: {attendance_rate}%")

# 5. Employés en retard
late_employees = []
for p in today_pointages.filter(arrival_status=Pointage.STATUS_LATE):
    late_employees.append({
        'full_name': f"{p.employee.first_name} {p.employee.last_name}",
        'late_minutes': p.late_minutes,
        'late_reason': p.late_reason,
        'is_justified': p.is_justified
    })

print(f"\n🚨 EMPLOYÉS EN RETARD:")
if late_employees:
    for emp in late_employees:
        print(f"   • {emp['full_name']}: {emp['late_minutes']} min - '{emp['late_reason']}'")
else:
    print("   Aucun employé en retard")

# 6. Simulation de l'API response
api_response = {
    'total_employees': total_employees,
    'present_today': present_today,
    'late_today': late_today,
    'absent_today': absent_today,
    'attendance_rate': attendance_rate,
    'late_employees': late_employees
}

print(f"\n🔍 RÉPONSE API SIMULÉE:")
print(json.dumps(api_response, indent=2, default=str))

# 7. Vérifications logiques
print(f"\n✅ VÉRIFICATIONS LOGIQUES:")
print(f"   • Présents + Absents = Total ? {present_today + absent_today} = {total_employees} → {'✅' if present_today + absent_today == total_employees else '❌'}")
print(f"   • En retard ≤ Présents ? {late_today} ≤ {present_today} → {'✅' if late_today <= present_today else '❌'}")
print(f"   • Taux présence cohérent ? {attendance_rate}% = {present_today}/{total_employees}*100 → {'✅' if abs(attendance_rate - (present_today/total_employees*100)) < 0.1 else '❌'}")

if late_today != len(late_employees):
    print(f"   ❌ INCOHÉRENCE: late_today={late_today} mais len(late_employees)={len(late_employees)}")
else:
    print(f"   ✅ Cohérence: late_today={late_today} = len(late_employees)={len(late_employees)}")
