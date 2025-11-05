#!/usr/bin/env python
"""
Script de nettoyage pour préparer le projet pour GitHub
Supprime tous les fichiers de test et debug
"""

import os
import glob

def clean_project():
    """Nettoyer le projet des fichiers de développement"""
    
    # Fichiers à supprimer (patterns)
    files_to_remove = [
        'test_*.py',
        'debug_*.py',
        'check_*.py',
        'fix_*.py',
        'create_*.py',
        'reset_*.py',
        'corriger_*.py',
        'creer_*.py',
        'diagnostic_*.py',
        'export_*.py',
        'liste_*.py',
        'migrate_*.py',
        'nettoyer_*.py',
        'recreate_*.py',
        'setup_*.py',
        'supprimer_*.py',
        'verifier_*.py',
        'voir_*.py',
        'clean_*.py',
        'demo_*.py',
        '*.bat',
        '*.md',
        'initial_data.json'
    ]
    
    # Fichiers à garder
    keep_files = [
        'manage.py',
        'requirements.txt',
        '.env.example'
    ]
    
    print("🧹 NETTOYAGE DU PROJET POUR GITHUB")
    print("="*50)
    
    removed_count = 0
    
    for pattern in files_to_remove:
        files = glob.glob(pattern)
        for file in files:
            if file not in keep_files and os.path.exists(file):
                try:
                    os.remove(file)
                    print(f"🗑️  Supprimé: {file}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Erreur suppression {file}: {e}")
    
    print(f"\n✅ Nettoyage terminé: {removed_count} fichiers supprimés")
    print("\n📋 FICHIERS CONSERVÉS:")
    
    # Lister les fichiers restants
    remaining_files = []
    for file in os.listdir('.'):
        if os.path.isfile(file) and not file.startswith('.'):
            remaining_files.append(file)
    
    for file in sorted(remaining_files):
        print(f"   ✅ {file}")
    
    print(f"\n🎯 PROJET PRÊT POUR GITHUB!")

if __name__ == '__main__':
    clean_project()
