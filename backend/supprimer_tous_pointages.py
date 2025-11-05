#!/usr/bin/env python
"""
Supprimer TOUS les pointages
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage

print("🗑️ SUPPRESSION DE TOUS LES POINTAGES")
print("="*50)

# Compter les pointages
total_pointages = Pointage.objects.all().count()
print(f"📊 Total pointages à supprimer: {total_pointages}")

if total_pointages == 0:
    print("✅ Aucun pointage à supprimer")
else:
    # Supprimer tous les pointages
    Pointage.objects.all().delete()
    print(f"✅ {total_pointages} pointage(s) supprimé(s)")

print("\n🎉 SUPPRESSION TERMINÉE !")
print("Vous pouvez maintenant:")
print("1. Rafraîchir le dashboard admin")
print("2. Commencer de nouveaux pointages")
print("3. Tester la synchronisation")
