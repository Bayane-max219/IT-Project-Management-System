#!/usr/bin/env python
"""
Debug des vraies justifications utilisateur
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from datetime import date

today = date.today()

print("🔍 DEBUG VRAIES JUSTIFICATIONS UTILISATEUR")
print("="*60)

# Supprimer tous les pointages de test
Pointage.objects.filter(date=today).delete()
print("🧹 Pointages de test supprimés")

print(f"\n💡 MAINTENANT:")
print("1. Allez sur l'interface développeur")
print("2. Pointez une arrivée en retard (après 8h15)")
print("3. Saisissez 'panne moto' comme justification")
print("4. Revenez ici et exécutez: python verifier_justification.py")

print(f"\n🎯 OBJECTIF:")
print("Vérifier si 'panne moto' est bien sauvegardé dans la DB")
