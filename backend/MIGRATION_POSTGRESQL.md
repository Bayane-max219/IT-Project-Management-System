# Migration vers PostgreSQL

Ce guide vous aide à migrer votre système de gestion de projet IT de SQLite vers PostgreSQL.

## État actuel

✅ **Terminé:**
- PostgreSQL adapter installé (`psycopg2-binary==2.9.7`)
- Configuration Django mise à jour (`settings.py`)
- Fichier `.env` configuré avec les paramètres PostgreSQL
- Scripts de migration créés

## Prérequis

Avant de continuer, assurez-vous que PostgreSQL est installé et en cours d'exécution sur votre système.

### Installation PostgreSQL (si nécessaire)

1. Téléchargez PostgreSQL depuis: https://www.postgresql.org/download/windows/
2. Installez avec les paramètres par défaut
3. Utilisateur par défaut: `postgres`
4. Mot de passe par défaut: `postgres` (ou celui que vous avez défini)

## Configuration actuelle

Le système est configuré pour utiliser PostgreSQL avec ces paramètres:

```
Base de données: it_project_management
Utilisateur: postgres
Mot de passe: postgres
Hôte: 127.0.0.1
Port: 5432
```

## Étapes de migration

### 1. Créer la base de données PostgreSQL

Exécutez le script de configuration:

```bash
python setup_postgresql.py
```

### 2. Exécuter les migrations Django

```bash
python manage.py migrate
```

### 3. Créer un superutilisateur (si nécessaire)

```bash
python manage.py createsuperuser
```

### 4. Ou utiliser le script de recréation des comptes de démonstration

```bash
python recreate_admin_and_demo.py
```

## Scripts disponibles

- `setup_postgresql.py` - Configure la base de données PostgreSQL
- `migrate_postgresql.bat` - Script batch pour Windows
- `test_postgresql_connection.py` - Teste la connexion PostgreSQL
- `recreate_admin_and_demo.py` - Recrée les comptes de démonstration

## Vérification

Pour vérifier que la migration a réussi:

1. Démarrez le serveur:
   ```bash
   python manage.py runserver
   ```

2. Accédez à l'interface admin:
   ```
   http://localhost:8000/admin
   ```

3. Connectez-vous avec:
   - Email: admin@itproject.com
   - Mot de passe: admin123

## Données de test

Pour créer des données de démonstration:

```bash
python create_demo_data.py
```

## Résolution des problèmes

### Erreur de connexion PostgreSQL

Si vous obtenez une erreur de connexion:

1. Vérifiez que PostgreSQL est en cours d'exécution
2. Vérifiez les paramètres dans `.env`
3. Testez la connexion avec: `python test_postgresql_connection.py`

### Erreurs de migration

Si les migrations échouent:

1. Supprimez les fichiers de migration (sauf `__init__.py`)
2. Recréez les migrations: `python manage.py makemigrations`
3. Appliquez les migrations: `python manage.py migrate`

## Avantages de PostgreSQL

- **Performance**: Meilleure performance pour les requêtes complexes
- **Concurrence**: Support natif des accès concurrents
- **Fonctionnalités**: Types de données avancés, index, contraintes
- **Scalabilité**: Adapté pour la production et la croissance
- **Fiabilité**: ACID compliant, sauvegarde et récupération

## Prochaines étapes

Une fois la migration terminée:

1. Testez toutes les fonctionnalités de l'application
2. Vérifiez les performances
3. Configurez les sauvegardes automatiques
4. Optimisez les requêtes si nécessaire

---

**Note**: Cette migration remplace complètement SQLite par PostgreSQL. Assurez-vous d'avoir une sauvegarde de vos données importantes avant de procéder.
