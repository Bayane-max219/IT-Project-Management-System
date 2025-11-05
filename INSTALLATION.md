# Guide d'Installation - IT Project Management System

## 📋 Prérequis

Avant d'installer le projet, assurez-vous d'avoir les éléments suivants installés sur votre système :

### Logiciels requis
- **Python 3.8+** : [Télécharger Python](https://python.org/downloads/)
- **Node.js 16+** : [Télécharger Node.js](https://nodejs.org/)
- **PostgreSQL 12+** : [Télécharger PostgreSQL](https://postgresql.org/download/)
- **Git** (optionnel) : [Télécharger Git](https://git-scm.com/)

### Vérification des installations
Ouvrez un terminal/invite de commande et vérifiez :

```bash
python --version    # Doit afficher Python 3.8+
node --version      # Doit afficher v16+
npm --version       # Doit afficher 8+
psql --version      # Doit afficher PostgreSQL 12+
```

## 🗄️ Configuration de la Base de Données

### 1. Créer la base de données PostgreSQL

Connectez-vous à PostgreSQL et créez la base de données :

```sql
-- Connexion à PostgreSQL (en tant qu'utilisateur postgres)
psql -U postgres

-- Création de la base de données
CREATE DATABASE it_project_management;

-- Création d'un utilisateur (optionnel)
CREATE USER it_user WITH PASSWORD 'it_password';
GRANT ALL PRIVILEGES ON DATABASE it_project_management TO it_user;

-- Quitter psql
\q
```

### 2. Configuration des paramètres de connexion

Dans le dossier `backend/`, copiez le fichier `.env.example` vers `.env` et modifiez les paramètres :

```env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
DB_NAME=it_project_management
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## 🚀 Installation Automatique (Recommandée)

### Option 1 : Script d'installation automatique

1. **Double-cliquez** sur le fichier `setup_project.bat`
2. **Suivez les instructions** à l'écran
3. **Attendez** que l'installation se termine

Le script va automatiquement :
- Vérifier les prérequis
- Installer les dépendances Python et Node.js
- Configurer la base de données
- Charger les données de test
- Créer les comptes utilisateurs

## 🔧 Installation Manuelle

### 1. Installation du Backend (Django)

```bash
# Naviguer vers le dossier backend
cd backend

# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur macOS/Linux :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer et appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Charger les données initiales
python manage.py loaddata initial_data.json

# Créer un superutilisateur
python manage.py createsuperuser
```

### 2. Installation du Frontend (React)

```bash
# Naviguer vers le dossier frontend
cd frontend

# Installer les dépendances Node.js
npm install
```

## 🎯 Démarrage de l'Application

### Option 1 : Scripts de démarrage automatique

1. **Backend** : Double-cliquez sur `start_backend.bat`
2. **Frontend** : Double-cliquez sur `start_frontend.bat`

### Option 2 : Démarrage manuel

#### Terminal 1 - Backend Django
```bash
cd backend
python manage.py runserver
```
Le serveur Django sera accessible sur : http://localhost:8000

#### Terminal 2 - Frontend React
```bash
cd frontend
npm start
```
L'application React sera accessible sur : http://localhost:3000

## 👥 Comptes de Test

Une fois l'installation terminée, vous pouvez utiliser ces comptes de test :

### Administrateur
- **Email** : `admin@company.com`
- **Mot de passe** : `admin123`
- **Accès** : Gestion complète du système

### Développeur
- **Email** : `rakoto@company.com`
- **Mot de passe** : `dev123`
- **Accès** : Tâches assignées + pointage

### Client
- **Email** : `client@example.com`
- **Mot de passe** : `client123`
- **Accès** : Suivi des projets en lecture seule

## 🌐 Accès à l'Application

1. **Ouvrez votre navigateur**
2. **Allez sur** : http://localhost:3000
3. **Connectez-vous** avec l'un des comptes de test
4. **Explorez** les fonctionnalités selon votre rôle

## 📁 Structure du Projet

```
IT-Project-Management-System/
├── backend/                 # API Django REST Framework
│   ├── core/               # Configuration Django
│   ├── apps/               # Applications métier
│   │   ├── authentication/ # Gestion utilisateurs
│   │   ├── projects/       # Gestion projets
│   │   ├── tasks/          # Gestion tâches
│   │   └── pointage/       # Système pointage
│   └── requirements.txt    # Dépendances Python
├── frontend/               # Application React
│   ├── src/
│   │   ├── components/     # Composants réutilisables
│   │   ├── pages/          # Pages principales
│   │   ├── services/       # Services API
│   │   └── contexts/       # Contextes React
│   └── package.json        # Dépendances Node.js
├── setup_project.bat       # Script d'installation
├── start_backend.bat       # Script démarrage backend
├── start_frontend.bat      # Script démarrage frontend
└── README.md               # Documentation principale
```

## 🛠️ Dépannage

### Problèmes courants

#### Erreur de connexion à la base de données
- Vérifiez que PostgreSQL est démarré
- Vérifiez les paramètres dans le fichier `.env`
- Assurez-vous que la base de données existe

#### Port déjà utilisé
- Backend (8000) : Changez le port avec `python manage.py runserver 8001`
- Frontend (3000) : Le script proposera automatiquement un autre port

#### Erreur d'installation des dépendances
- Mettez à jour pip : `python -m pip install --upgrade pip`
- Utilisez un environnement virtuel Python
- Vérifiez votre connexion internet

#### Problèmes d'authentification
- Vérifiez que les données initiales sont chargées
- Réinitialisez la base de données si nécessaire

### Support

Si vous rencontrez des problèmes :

1. **Vérifiez** que tous les prérequis sont installés
2. **Consultez** les logs d'erreur dans les terminaux
3. **Réexécutez** le script d'installation
4. **Vérifiez** la configuration de la base de données

## 🎉 Félicitations !

Votre système de gestion de projets IT est maintenant opérationnel !

Vous pouvez maintenant :
- ✅ Gérer les projets et tâches
- ✅ Suivre le pointage des employés
- ✅ Consulter les statistiques en temps réel
- ✅ Collaborer efficacement en équipe
