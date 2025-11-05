# 🚀 Démarrage Rapide - IT Project Management System

## ⚡ Installation Express (5 minutes)

### 1. Prérequis
Assurez-vous d'avoir installé :
- **Python 3.8+** 
- **Node.js 16+**
- **PostgreSQL 12+**

### 2. Configuration Base de Données
```sql
-- Connectez-vous à PostgreSQL
psql -U postgres

-- Créez la base de données
CREATE DATABASE it_project_management;
```

### 3. Installation Automatique
**Double-cliquez sur** `setup_project.bat` et suivez les instructions.

### 4. Démarrage
1. **Backend** : Double-cliquez sur `start_backend.bat`
2. **Frontend** : Double-cliquez sur `start_frontend.bat`
3. **Ouvrez** : http://localhost:3000

## 👤 Comptes de Test

| Rôle | Email | Mot de passe | Accès |
|------|-------|--------------|-------|
| **Admin** | admin@company.com | admin123 | Gestion complète |
| **Développeur** | rakoto@company.com | dev123 | Tâches + Pointage |
| **Client** | client@example.com | client123 | Suivi projets |

## 🎯 Fonctionnalités Clés

### 👨‍💼 Administrateur
- ✅ **Dashboard global** avec statistiques temps réel
- ✅ **Gestion projets** : Création, modification, assignation équipes
- ✅ **Gestion tâches** : CRUD complet, assignation développeurs
- ✅ **Gestion utilisateurs** : Création comptes, rôles, permissions
- ✅ **Statistiques pointage** : Présence, retards, heures travaillées
- ✅ **Graphiques interactifs** : Progression projets, performance équipe

### 👨‍💻 Développeur
- ✅ **Dashboard personnel** avec tâches assignées
- ✅ **Pointage temps réel** : Arrivée, pause, départ
- ✅ **Gestion tâches** : Modification statuts, commentaires
- ✅ **Historique pointage** : Consultation, temps travaillé
- ✅ **Interface intuitive** : Actions rapides, notifications

### 👤 Client
- ✅ **Dashboard projets** : Vue d'ensemble, progression
- ✅ **Suivi détaillé** : Statut, échéances, équipe assignée
- ✅ **Lecture seule** : Consultation sans modification
- ✅ **Informations temps réel** : Mise à jour automatique

## 📊 Captures d'Écran Principales

### Dashboard Admin
- **Statistiques globales** : Projets actifs, tâches, présence
- **Graphiques** : Répartition par statut, performance équipe
- **Alertes** : Projets en retard, employés absents

### Interface Développeur
- **Pointage rapide** : Boutons arrivée/pause/départ
- **Mes tâches** : Liste filtrée, changement statut
- **Historique** : Temps travaillé, statistiques personnelles

### Suivi Client
- **Mes projets** : Progression visuelle, détails équipe
- **Calendrier** : Échéances, jalons importants
- **Rapports** : Avancement, temps passé

## 🔧 Résolution Problèmes Courants

### ❌ Erreur Base de Données
```bash
# Vérifiez que PostgreSQL fonctionne
pg_ctl status

# Recréez la base si nécessaire
dropdb it_project_management
createdb it_project_management
```

### ❌ Port Déjà Utilisé
```bash
# Backend (changez le port)
python manage.py runserver 8001

# Frontend (acceptez le port proposé)
npm start
```

### ❌ Dépendances Manquantes
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## 📱 Utilisation Mobile

L'application est **entièrement responsive** :
- **Navigation tactile** optimisée
- **Formulaires adaptatifs** 
- **Tableaux scrollables**
- **Interface touch-friendly**

## 🎨 Personnalisation

### Thème et Couleurs
Modifiez `frontend/tailwind.config.js` :
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#votre-couleur',
        600: '#votre-couleur-foncee',
      }
    }
  }
}
```

### Logo et Branding
Remplacez les fichiers dans `frontend/public/` :
- `favicon.ico`
- `logo192.png`
- `logo512.png`

## 📈 Données de Démonstration

Le système inclut des **données de test réalistes** :
- **2 projets** en cours avec tâches assignées
- **5 utilisateurs** avec rôles différents
- **Pointages** des derniers jours
- **Statistiques** pré-calculées

## 🔐 Sécurité

### Authentification
- **JWT Tokens** sécurisés (24h access, 7j refresh)
- **Rotation automatique** des tokens
- **Permissions** basées sur les rôles

### Protection Données
- **Validation** côté serveur
- **CORS** configuré
- **CSRF** protection activée
- **Chiffrement** mots de passe

## 🚀 Mise en Production

### Checklist Déploiement
- [ ] Changer `SECRET_KEY` Django
- [ ] Définir `DEBUG=False`
- [ ] Configurer base de données production
- [ ] Activer HTTPS
- [ ] Configurer serveur web (Nginx/Apache)
- [ ] Mettre en place monitoring

### Recommandations
- **Serveur** : Ubuntu 20.04+ ou CentOS 8+
- **Base données** : PostgreSQL 13+
- **Serveur web** : Nginx + Gunicorn
- **SSL** : Let's Encrypt
- **Monitoring** : Sentry pour les erreurs

## 📞 Support

### En cas de problème :
1. **Vérifiez** les prérequis installés
2. **Consultez** les logs dans les terminaux
3. **Relancez** les scripts d'installation
4. **Vérifiez** la configuration PostgreSQL

### Logs Utiles
```bash
# Backend Django
tail -f backend/logs/django.log

# Frontend React
# Consultez la console navigateur (F12)
```

## 🎉 Félicitations !

Votre système de gestion IT est opérationnel ! 

**Prochaines étapes :**
1. **Explorez** les différents rôles utilisateur
2. **Créez** vos premiers projets et tâches
3. **Testez** le système de pointage
4. **Consultez** les statistiques générées
5. **Personnalisez** selon vos besoins

---

**Temps d'installation total : ~5 minutes**  
**Prêt à l'emploi : Immédiatement**  
**Support : Documentation complète incluse**
