#!/usr/bin/env python
"""
Script rapide pour supprimer les pointages d'aujourd'hui
"""
import os
import sys
import django
from datetime import date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage

print("🗑️  SUPPRESSION RAPIDE - POINTAGES D'AUJOURD'HUI")

today = date.today()
pointages_today = Pointage.objects.filter(date=today)

print(f"📅 Date: {today}")
print(f"📊 Pointages trouvés: {pointages_today.count()}")

if pointages_today.exists():
    print("\n📋 POINTAGES À SUPPRIMER:")
    for p in pointages_today:
        print(f"   • {p.employee.first_name} {p.employee.last_name} - {p.arrival_time or 'Non pointé'}")
    
    print(f"\n⚠️  Supprimer {pointages_today.count()} pointage(s) ?")
    confirmation = input("Tapez 'OUI' pour confirmer: ")
    
    if confirmation == 'OUI':
        count = pointages_today.count()
        pointages_today.delete()
        print(f"✅ {count} pointage(s) supprimé(s)")
        print("🎉 Les développeurs peuvent maintenant pointer à nouveau !")
    else:
        print("❌ Suppression annulée")
else:
    print("✅ Aucun pointage aujourd'hui à supprimer")

print("\n💡 Après suppression:")
print("1. Rafraîchir le dashboard admin")
print("2. Les développeurs peuvent pointer normalement")
print("3. Les statistiques seront remises à zéro")
