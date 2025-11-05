# Documentation Technique - IT Project Management System

## 🏗️ Architecture du Système

### Vue d'ensemble
L'application est construite selon une architecture **client-serveur séparée** :
- **Backend** : API REST avec Django REST Framework
- **Frontend** : Application React SPA (Single Page Application)
- **Base de données** : PostgreSQL
- **Authentification** : JWT (JSON Web Tokens)

### Stack Technologique

#### Backend
- **Django 4.2.7** - Framework web Python
- **Django REST Framework 3.14.0** - API REST
- **PostgreSQL** - Base de données relationnelle
- **JWT Authentication** - Authentification sécurisée
- **CORS Headers** - Communication cross-origin

#### Frontend
- **React 18.2.0** - Bibliothèque UI
- **React Router 6.16.0** - Routing côté client
- **TailwindCSS 3.3.5** - Framework CSS utilitaire
- **Axios 1.5.0** - Client HTTP
- **Chart.js 4.4.0** - Graphiques et visualisations
- **Headless UI** - Composants accessibles

## 📊 Modèle de Données

### Entités Principales

#### User (Utilisateur)
```python
- id: AutoField (PK)
- username: CharField(unique)
- email: EmailField(unique)
- first_name: CharField
- last_name: CharField
- role: CharField(choices=['admin', 'developer', 'client'])
- phone: CharField(optional)
- profile_picture: ImageField(optional)
- is_active: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### Project (Projet)
```python
- id: AutoField (PK)
- name: CharField
- description: TextField
- client: ForeignKey(User, role='client')
- project_manager: ForeignKey(User, role=['admin', 'developer'])
- status: CharField(choices=['planning', 'in_progress', 'testing', 'completed', 'on_hold', 'cancelled'])
- priority: CharField(choices=['low', 'medium', 'high', 'urgent'])
- start_date: DateField
- end_date: DateField
- actual_end_date: DateField(optional)
- budget: DecimalField(optional)
- progress: IntegerField(default=0)
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### Task (Tâche)
```python
- id: AutoField (PK)
- title: CharField
- description: TextField
- project: ForeignKey(Project)
- assigned_to: ForeignKey(User, role='developer')
- created_by: ForeignKey(User)
- status: CharField(choices=['todo', 'in_progress', 'testing', 'completed', 'blocked'])
- priority: CharField(choices=['low', 'medium', 'high', 'urgent'])
- estimated_hours: DecimalField(optional)
- actual_hours: DecimalField(optional)
- start_date: DateField(optional)
- due_date: DateField(optional)
- completed_at: DateTimeField(optional)
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### Pointage
```python
- id: AutoField (PK)
- employee: ForeignKey(User, role='developer')
- date: DateField
- arrival_time: TimeField(optional)
- break_start: TimeField(optional)
- break_end: TimeField(optional)
- departure_time: TimeField(optional)
- late_reason: TextField(optional)
- notes: TextField(optional)
- is_late: BooleanField
- late_minutes: IntegerField
- created_at: DateTimeField
- updated_at: DateTimeField
```

### Relations
- **User ↔ Project** : Many-to-Many (via ProjectTeam)
- **Project → Task** : One-to-Many
- **User → Task** : One-to-Many (assigned_to)
- **User → Pointage** : One-to-Many

## 🔐 Système d'Authentification

### JWT Implementation
- **Access Token** : Durée de vie 24h
- **Refresh Token** : Durée de vie 7 jours
- **Rotation automatique** des tokens
- **Blacklist** des tokens après rotation

### Rôles et Permissions

#### Admin
- Accès complet à toutes les fonctionnalités
- CRUD sur tous les modèles
- Accès aux statistiques globales
- Gestion des utilisateurs

#### Developer (Développeur)
- Accès à ses tâches assignées
- Modification du statut des tâches
- Système de pointage personnel
- Vue des projets où il est assigné

#### Client
- Vue en lecture seule de ses projets
- Suivi de l'avancement
- Pas d'accès aux fonctionnalités de gestion

## 🌐 API REST Endpoints

### Authentication
```
POST /api/auth/login/           # Connexion
POST /api/auth/logout/          # Déconnexion
POST /api/auth/register/        # Inscription
GET  /api/auth/profile/         # Profil utilisateur
PUT  /api/auth/profile/update/  # Mise à jour profil
POST /api/auth/change-password/ # Changement mot de passe
GET  /api/auth/users/           # Liste utilisateurs (admin)
```

### Projects
```
GET    /api/projects/                    # Liste projets
POST   /api/projects/                    # Créer projet
GET    /api/projects/{id}/               # Détail projet
PUT    /api/projects/{id}/               # Modifier projet
DELETE /api/projects/{id}/               # Supprimer projet
POST   /api/projects/{id}/team/add/      # Ajouter membre équipe
DELETE /api/projects/{id}/team/{mid}/remove/ # Retirer membre
GET    /api/projects/stats/              # Statistiques projets
```

### Tasks
```
GET    /api/tasks/                # Liste tâches
POST   /api/tasks/                # Créer tâche
GET    /api/tasks/{id}/           # Détail tâche
PUT    /api/tasks/{id}/           # Modifier tâche
DELETE /api/tasks/{id}/           # Supprimer tâche
GET    /api/tasks/my-tasks/       # Mes tâches (dev)
POST   /api/tasks/{id}/status/    # Changer statut
GET    /api/tasks/{id}/comments/  # Commentaires tâche
POST   /api/tasks/{id}/comments/  # Ajouter commentaire
GET    /api/tasks/stats/          # Statistiques tâches
```

### Pointage
```
GET  /api/pointage/                    # Liste pointages
POST /api/pointage/                    # Créer pointage
GET  /api/pointage/my-pointages/       # Mes pointages
GET  /api/pointage/today/              # Pointage du jour
POST /api/pointage/clock-in/           # Pointer arrivée
POST /api/pointage/clock-out/          # Pointer départ
POST /api/pointage/break-start/        # Début pause
POST /api/pointage/break-end/          # Fin pause
GET  /api/pointage/stats/              # Statistiques pointage
GET  /api/pointage/absences/           # Demandes d'absence
POST /api/pointage/absences/           # Créer demande absence
POST /api/pointage/absences/{id}/approve/ # Approuver absence
```

## 🎨 Architecture Frontend

### Structure des Composants
```
src/
├── components/          # Composants réutilisables
│   ├── Layout.js       # Layout principal
│   ├── Header.js       # En-tête
│   ├── Sidebar.js      # Menu latéral
│   └── ProtectedRoute.js # Route protégée
├── contexts/           # Contextes React
│   └── AuthContext.js  # Contexte authentification
├── pages/              # Pages principales
│   ├── auth/           # Pages authentification
│   ├── admin/          # Pages administrateur
│   ├── developer/      # Pages développeur
│   └── client/         # Pages client
├── services/           # Services API
│   ├── api.js          # Configuration Axios
│   ├── authService.js  # Service authentification
│   ├── projectService.js # Service projets
│   ├── taskService.js  # Service tâches
│   └── pointageService.js # Service pointage
└── utils/              # Utilitaires
```

### Routing
- **Route publique** : `/login`
- **Routes admin** : `/admin/*`
- **Routes développeur** : `/developer/*`
- **Routes client** : `/client/*`
- **Redirection automatique** selon le rôle

### État Global
- **AuthContext** : Gestion de l'authentification
- **Local State** : État des composants individuels
- **API Calls** : Gestion via services dédiés

## 🔧 Configuration et Déploiement

### Variables d'Environnement Backend
```env
SECRET_KEY=django-secret-key
DEBUG=True/False
DB_NAME=it_project_management
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

### Configuration CORS
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Sécurité
- **CSRF Protection** activée
- **JWT Tokens** sécurisés
- **Validation des données** côté serveur
- **Permissions** basées sur les rôles
- **HTTPS** recommandé en production

## 📈 Fonctionnalités Principales

### Dashboard Personnalisés
- **Admin** : Vue globale, statistiques, graphiques
- **Développeur** : Tâches personnelles, pointage
- **Client** : Suivi projets, progression

### Système de Pointage
- **Pointage temps réel** : Arrivée, pause, départ
- **Gestion des retards** : Raisons obligatoires
- **Calcul automatique** : Heures travaillées
- **Historique complet** : Tous les pointages

### Gestion de Projets
- **CRUD complet** : Création, modification, suppression
- **Assignation d'équipes** : Développeurs par projet
- **Suivi progression** : Calcul automatique basé sur les tâches
- **Gestion des échéances** : Alertes retards

### Statistiques et Rapports
- **Graphiques temps réel** : Chart.js
- **Métriques de performance** : Taux de présence, productivité
- **Rapports détaillés** : Par projet, développeur, période

## 🚀 Performance et Optimisation

### Backend
- **Pagination** : 20 éléments par page
- **Select Related** : Optimisation des requêtes
- **Indexation** : Champs fréquemment utilisés
- **Cache** : Recommandé pour la production

### Frontend
- **Code Splitting** : Chargement à la demande
- **Optimisation images** : Compression automatique
- **Bundle Optimization** : Webpack optimisé
- **Responsive Design** : Mobile-first

## 🧪 Tests et Qualité

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
npm test
```

### Linting et Formatting
- **Backend** : flake8, black
- **Frontend** : ESLint, Prettier

## 📱 Responsive Design

L'application est entièrement responsive avec :
- **Breakpoints TailwindCSS** : sm, md, lg, xl
- **Navigation mobile** : Menu hamburger
- **Tableaux adaptatifs** : Scroll horizontal sur mobile
- **Formulaires optimisés** : Touch-friendly

## 🔮 Évolutions Futures

### Fonctionnalités Prévues
- **Notifications push** : Temps réel
- **Export PDF** : Rapports et statistiques
- **API mobile** : Application mobile native
- **Intégrations** : Slack, Teams, Email
- **Gestion des congés** : Système complet
- **Timetracking avancé** : Par tâche

### Améliorations Techniques
- **WebSockets** : Notifications temps réel
- **Redis Cache** : Performance améliorée
- **Docker** : Containerisation
- **CI/CD** : Déploiement automatisé
- **Tests automatisés** : Couverture complète

---

Cette documentation technique fournit une vue d'ensemble complète du système IT Project Management. Pour plus de détails sur l'installation et l'utilisation, consultez les fichiers `README.md` et `INSTALLATION.md`.
