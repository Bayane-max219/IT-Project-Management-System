#!/usr/bin/env python
"""
Corriger les pointages existants sans raison
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from datetime import date

today = date.today()

print("🔧 CORRECTION DES POINTAGES EXISTANTS")
print("="*50)

# Trouver les pointages en retard sans raison
pointages_sans_raison = Pointage.objects.filter(
    date=today,
    arrival_status=Pointage.STATUS_LATE,
    late_reason__isnull=True
)

print(f"📊 Pointages sans raison: {pointages_sans_raison.count()}")

raisons_test = [
    "Problème de transport public",
    "Embouteillages exceptionnels", 
    "Urgence familiale résolue",
    "Panne de réveil - excuses",
    "Retard médical justifié"
]

for i, pointage in enumerate(pointages_sans_raison):
    raison = raisons_test[i % len(raisons_test)]
    
    print(f"\n🔧 Correction {pointage.employee.first_name}:")
    print(f"   AVANT: late_reason = {pointage.late_reason}")
    
    pointage.late_reason = raison
    pointage.is_justified = True
    pointage.save()
    
    # Vérifier la sauvegarde
    pointage.refresh_from_db()
    print(f"   APRÈS: late_reason = '{pointage.late_reason}'")
    
    if pointage.late_reason == raison:
        print(f"   ✅ Sauvegarde réussie")
    else:
        print(f"   ❌ Échec sauvegarde")

print(f"\n🎉 CORRECTION TERMINÉE")
print("Rafraîchissez l'admin pour voir les changements")
