#!/usr/bin/env python
"""
Vérifier si la justification utilisateur est sauvegardée
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from datetime import date

today = date.today()

print("🔍 VÉRIFICATION JUSTIFICATION UTILISATEUR")
print("="*50)

pointages = Pointage.objects.filter(date=today)
print(f"📊 Pointages trouvés: {pointages.count()}")

for p in pointages:
    print(f"\n👤 {p.employee.first_name} {p.employee.last_name}")
    print(f"   Arrivée: {p.arrival_time}")
    print(f"   Statut: {p.arrival_status}")
    print(f"   Raison: '{p.late_reason}' (type: {type(p.late_reason)})")
    print(f"   Justifié: {p.is_justified}")
    
    if p.late_reason == "panne moto":
        print(f"   ✅ PARFAIT: La vraie justification est sauvegardée !")
    elif p.late_reason is None:
        print(f"   ❌ PROBLÈME: Justification non sauvegardée")
    else:
        print(f"   ⚠️  ATTENTION: Justification différente de celle saisie")

if pointages.count() == 0:
    print("❌ Aucun pointage trouvé")
    print("Faites d'abord un pointage avec justification")
