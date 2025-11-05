#!/usr/bin/env python
"""
Nettoyage complet pour redémarrer les tests
"""
import os
import sys
import django
from datetime import date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage

print("🧹 NETTOYAGE COMPLET")

# Supprimer tous les pointages d'aujourd'hui
today = date.today()
pointages_today = Pointage.objects.filter(date=today)

print(f"📅 Date: {today}")
print(f"📊 Pointages à supprimer: {pointages_today.count()}")

if pointages_today.exists():
    for p in pointages_today:
        print(f"   • {p.employee.first_name} {p.employee.last_name}")
    
    pointages_today.delete()
    print("✅ Pointages supprimés")
else:
    print("✅ Aucun pointage à supprimer")

print("\n🎉 Nettoyage terminé !")
print("Vous pouvez maintenant tester le pointage normalement.")
