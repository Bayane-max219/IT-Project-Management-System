#!/usr/bin/env python
"""
Tester un nouveau pointage avec justification
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from django.contrib.auth import get_user_model
from datetime import date, time
import json

User = get_user_model()

print("🧪 TEST NOUVEAU POINTAGE AVEC JUSTIFICATION")
print("="*60)

# Nettoyer tous les pointages
today = date.today()
Pointage.objects.filter(date=today).delete()
print("🧹 Pointages existants supprimés")

# Trouver un développeur
dev = User.objects.filter(role='developer').first()
if not dev:
    print("❌ Aucun développeur trouvé")
    exit(1)

print(f"👤 Développeur: {dev.first_name} {dev.last_name}")

# Créer un pointage en retard avec justification
pointage = Pointage.objects.create(
    employee=dev,
    date=today,
    arrival_time=time(10, 45),  # 10h45 = retard
    arrival_status=Pointage.STATUS_LATE,
    late_minutes=165,  # 2h45 de retard
    late_reason="Transport en panne - Réparation urgente",
    is_justified=True
)

print(f"\n✅ POINTAGE CRÉÉ:")
print(f"   ID: {pointage.id}")
print(f"   Arrivée: {pointage.arrival_time}")
print(f"   Statut: {pointage.arrival_status}")
print(f"   Minutes retard: {pointage.late_minutes}")
print(f"   Raison: '{pointage.late_reason}'")
print(f"   Justifié: {pointage.is_justified}")

# Vérifier en relisant depuis la DB
pointage_db = Pointage.objects.get(id=pointage.id)
print(f"\n🔍 VÉRIFICATION DEPUIS LA DB:")
print(f"   Raison DB: '{pointage_db.late_reason}'")
print(f"   Type: {type(pointage_db.late_reason)}")

# Simuler l'API
late_employees = []
for p in Pointage.objects.filter(date=today, arrival_status=Pointage.STATUS_LATE):
    emp = {
        'id': p.employee.id,
        'full_name': f"{p.employee.first_name} {p.employee.last_name}",
        'late_reason': p.late_reason,
        'late_minutes': p.late_minutes,
        'is_justified': p.is_justified
    }
    late_employees.append(emp)

print(f"\n📊 DONNÉES API:")
print(json.dumps(late_employees, indent=2, default=str))

if late_employees and late_employees[0]['late_reason']:
    print(f"\n✅ SUCCESS: La raison est bien sauvegardée !")
    print(f"   Rafraîchissez l'admin, la raison devrait apparaître")
else:
    print(f"\n❌ ÉCHEC: La raison n'est pas sauvegardée")
    print(f"   Il y a un bug dans le processus de sauvegarde")
