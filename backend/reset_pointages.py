#!/usr/bin/env python
"""
Script pour remettre à zéro les pointages
"""
import os
import sys
import django
from datetime import date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage

print("\n" + "="*80)
print("  REMISE À ZÉRO DES POINTAGES")
print("="*80)

def afficher_statistiques():
    """Afficher les statistiques actuelles"""
    today = date.today()
    
    # Pointages d'aujourd'hui
    today_pointages = Pointage.objects.filter(date=today)
    
    # Tous les pointages
    all_pointages = Pointage.objects.all()
    
    print(f"📅 Date d'aujourd'hui: {today}")
    print(f"📊 Pointages d'aujourd'hui: {today_pointages.count()}")
    print(f"📊 Total pointages: {all_pointages.count()}")
    
    if today_pointages.exists():
        print(f"\n📋 POINTAGES D'AUJOURD'HUI:")
        for p in today_pointages:
            print(f"   • {p.employee.first_name} {p.employee.last_name}")
            print(f"     Arrivée: {p.arrival_time or 'Non pointé'}")
            print(f"     Départ: {p.departure_time or 'Non pointé'}")
            print(f"     Statut: {p.arrival_status or 'Aucun'}")
            print("-" * 40)
    
    return today_pointages.count(), all_pointages.count()

def supprimer_pointages_aujourd_hui():
    """Supprimer tous les pointages d'aujourd'hui"""
    today = date.today()
    pointages_today = Pointage.objects.filter(date=today)
    
    if not pointages_today.exists():
        print("✅ Aucun pointage aujourd'hui à supprimer")
        return
    
    count = pointages_today.count()
    print(f"\n⚠️  SUPPRESSION DE {count} POINTAGE(S) D'AUJOURD'HUI")
    
    confirmation = input("Êtes-vous sûr ? (oui/non): ").lower()
    if confirmation in ['oui', 'o', 'yes', 'y']:
        pointages_today.delete()
        print(f"✅ {count} pointage(s) d'aujourd'hui supprimé(s)")
        print("🎉 Les développeurs peuvent maintenant pointer à nouveau !")
    else:
        print("❌ Suppression annulée")

def supprimer_tous_pointages():
    """Supprimer TOUS les pointages"""
    all_pointages = Pointage.objects.all()
    
    if not all_pointages.exists():
        print("✅ Aucun pointage à supprimer")
        return
    
    count = all_pointages.count()
    print(f"\n⚠️  SUPPRESSION DE TOUS LES {count} POINTAGE(S)")
    print("🚨 ATTENTION: Cette action supprimera TOUT l'historique !")
    
    confirmation = input("Êtes-vous VRAIMENT sûr ? (SUPPRIMER/non): ")
    if confirmation == "SUPPRIMER":
        all_pointages.delete()
        print(f"✅ TOUS les {count} pointage(s) supprimés")
        print("🎉 Base de données remise à zéro !")
    else:
        print("❌ Suppression annulée")

def menu_principal():
    """Menu principal"""
    while True:
        print("\n" + "="*80)
        print("  MENU REMISE À ZÉRO")
        print("="*80)
        
        # Afficher les statistiques
        today_count, total_count = afficher_statistiques()
        
        print("\n📋 OPTIONS:")
        print("1. 🗑️  Supprimer les pointages d'AUJOURD'HUI seulement")
        print("2. 🚨 Supprimer TOUS les pointages (historique complet)")
        print("3. 📊 Rafraîchir les statistiques")
        print("4. ❌ Quitter")
        print("-" * 80)
        
        choix = input("Votre choix (1-4): ").strip()
        
        if choix == '1':
            supprimer_pointages_aujourd_hui()
        elif choix == '2':
            supprimer_tous_pointages()
        elif choix == '3':
            continue  # Rafraîchir en rebouclant
        elif choix == '4':
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide")
        
        if choix in ['1', '2']:
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == '__main__':
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
