#!/usr/bin/env python
"""
Script pour nettoyer le pointage bloqué de Rabe
"""
import os
import sys
import django
from datetime import date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.pointage.models import Pointage

User = get_user_model()

print("\n" + "="*80)
print("  NETTOYAGE POINTAGE - RABE RASOAMANANAS")
print("="*80)

try:
    rabe = User.objects.get(email='rabe@company.com')
    print(f"✅ Utilisateur: {rabe.first_name} {rabe.last_name}")
except User.DoesNotExist:
    print("❌ Rabe non trouvé")
    sys.exit(1)

today = date.today()
print(f"📅 Date: {today}")

# Supprimer les pointages d'aujourd'hui
pointages_today = Pointage.objects.filter(employee=rabe, date=today)

if pointages_today.exists():
    count = pointages_today.count()
    
    print(f"\n⚠️  {count} pointage(s) trouvé(s) pour aujourd'hui:")
    for p in pointages_today:
        print(f"   - ID {p.id}: Arrivée={p.arrival_time}, Départ={p.departure_time}")
    
    # Supprimer
    deleted_count = pointages_today.delete()[0]
    print(f"\n✅ {deleted_count} pointage(s) supprimé(s)")
    
    print("\n🎉 NETTOYAGE TERMINÉ !")
    print("Rabe peut maintenant pointer son arrivée normalement.")
    
else:
    print("\n✅ Aucun pointage à nettoyer")
    print("Le problème vient d'ailleurs.")

print("\n💡 Actions à faire:")
print("1. Rafraîchir la page web (Ctrl+Shift+R)")
print("2. Essayer de pointer l'arrivée")
print("3. Vérifier les logs du serveur si ça ne marche pas")
