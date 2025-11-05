#!/usr/bin/env python
"""
Script pour exporter la base de données PostgreSQL
"""
import os
import subprocess
import datetime

def export_database():
    """Exporter la base de données PostgreSQL"""
    print("🗄️ EXPORTATION DE LA BASE DE DONNÉES POSTGRESQL")
    print("=" * 50)
    
    # Configuration de la base
    db_config = {
        'host': '127.0.0.1',
        'port': '5432',
        'database': 'it_project_management',
        'username': 'postgres',
        'password': 'postgres'
    }
    
    # Nom du fichier de sauvegarde avec timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"it_project_management_backup_{timestamp}.sql"
    backup_path = os.path.join(os.path.dirname(__file__), backup_filename)
    
    print(f"📁 Fichier de sauvegarde : {backup_filename}")
    print(f"📍 Chemin complet : {backup_path}")
    
    # Commande pg_dump
    pg_dump_cmd = [
        'pg_dump',
        '-h', db_config['host'],
        '-p', db_config['port'],
        '-U', db_config['username'],
        '-d', db_config['database'],
        '-f', backup_path,
        '--verbose',
        '--clean',
        '--if-exists',
        '--create'
    ]
    
    print(f"\n🔄 Exécution de la commande d'exportation...")
    print(f"Commande : {' '.join(pg_dump_cmd)}")
    
    # Définir la variable d'environnement pour le mot de passe
    env = os.environ.copy()
    env['PGPASSWORD'] = db_config['password']
    
    try:
        # Exécuter pg_dump
        result = subprocess.run(
            pg_dump_cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ Exportation réussie !")
        print(f"📊 Taille du fichier : {os.path.getsize(backup_path)} bytes")
        
        # Créer aussi un fichier de structure seulement
        structure_filename = f"it_project_management_structure_{timestamp}.sql"
        structure_path = os.path.join(os.path.dirname(__file__), structure_filename)
        
        pg_dump_structure_cmd = [
            'pg_dump',
            '-h', db_config['host'],
            '-p', db_config['port'],
            '-U', db_config['username'],
            '-d', db_config['database'],
            '-f', structure_path,
            '--schema-only',
            '--clean',
            '--if-exists',
            '--create'
        ]
        
        print(f"\n🏗️ Création du fichier de structure...")
        subprocess.run(pg_dump_structure_cmd, env=env, check=True)
        print(f"✅ Structure exportée : {structure_filename}")
        
        # Informations pour GitHub
        print(f"\n📋 FICHIERS CRÉÉS POUR GITHUB :")
        print(f"1. 📄 {backup_filename} - Base complète avec données")
        print(f"2. 🏗️ {structure_filename} - Structure seulement")
        
        print(f"\n🚀 POUR GITHUB :")
        print(f"1. Ajoutez ces fichiers à votre projet")
        print(f"2. Créez un dossier 'database/' dans votre repo")
        print(f"3. Placez les fichiers .sql dans ce dossier")
        print(f"4. Ajoutez un README.md avec les instructions d'importation")
        
        return backup_path, structure_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exportation : {e}")
        print(f"Sortie d'erreur : {e.stderr}")
        return None, None
    except FileNotFoundError:
        print("❌ pg_dump non trouvé !")
        print("💡 Solutions :")
        print("1. Vérifiez que PostgreSQL est installé")
        print("2. Ajoutez PostgreSQL au PATH système")
        print("3. Ou utilisez le chemin complet vers pg_dump.exe")
        print("   Exemple : C:\\Program Files\\PostgreSQL\\16\\bin\\pg_dump.exe")
        return None, None

def create_import_instructions():
    """Créer un fichier d'instructions d'importation"""
    instructions = """# 🗄️ Instructions d'Importation de la Base de Données

## 📋 Prérequis
- PostgreSQL installé
- Utilisateur `postgres` avec mot de passe `postgres`
- Base de données `it_project_management` (sera créée automatiquement)

## 🚀 Importation Complète (avec données)

```bash
# Windows
psql -U postgres -h localhost -f it_project_management_backup_[timestamp].sql

# Ou avec chemin complet
"C:\\Program Files\\PostgreSQL\\16\\bin\\psql.exe" -U postgres -h localhost -f it_project_management_backup_[timestamp].sql
```

## 🏗️ Importation Structure Seulement

```bash
# Windows
psql -U postgres -h localhost -f it_project_management_structure_[timestamp].sql
```

## ⚙️ Configuration Django

Assurez-vous que `settings.py` contient :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'it_project_management',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

## 🔄 Après Importation

```bash
# Appliquer les migrations Django
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver
```

## 📊 Données de Test

La base contient :
- Utilisateurs de test (admin, clients, développeurs)
- Projets d'exemple
- Tâches assignées
- Données de pointage

**Connexions de test :**
- Admin : `admin@example.com` / `admin123`
- Client : `client@example.com` / `client123`
- Développeur : `dev@example.com` / `dev123`
"""
    
    instructions_path = os.path.join(os.path.dirname(__file__), "DATABASE_IMPORT_INSTRUCTIONS.md")
    with open(instructions_path, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"📋 Instructions créées : DATABASE_IMPORT_INSTRUCTIONS.md")
    return instructions_path

if __name__ == '__main__':
    backup_path, structure_path = export_database()
    
    if backup_path:
        instructions_path = create_import_instructions()
        print(f"\n🎉 EXPORTATION TERMINÉE !")
        print(f"\nFichiers créés :")
        print(f"- {os.path.basename(backup_path)}")
        print(f"- {os.path.basename(structure_path)}")
        print(f"- {os.path.basename(instructions_path)}")
    else:
        print(f"\n❌ Exportation échouée")
