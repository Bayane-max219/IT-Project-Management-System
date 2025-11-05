# 🚀 IT Project Management System - Version Professionnelle

## 📋 Vue d'ensemble

Système de gestion de projets IT professionnel avec :
- ✅ **Gestion des comptes professionnelle** (plus de comptes de test)
- ✅ **Envoi automatique d'emails** pour les nouveaux comptes
- ✅ **Système d'invitations** avec clés d'inscription
- ✅ **Pointage avec heures normales** (8h-17h)
- ✅ **Interface de connexion épurée**

## 🎯 Fonctionnalités Principales

### **👤 Gestion des Utilisateurs**
- **Admin crée les comptes** → Envoi email automatique
- **Invitations par clé** → Utilisateurs créent leur propre compte
- **Plus de comptes de test** dans l'interface

### **⏰ Système de Pointage**
- **Heures normales** : 8h00 - 17h00
- **Pause déjeuner** : 12h00 - 13h00 (déduite automatiquement)
- **Tolérance** : 15 minutes
- **Calcul automatique** des heures travaillées

### **📧 Système d'Email**
- **Développement** : Emails affichés dans la console
- **Production** : Configuration SMTP prête

## 🚀 Installation et Lancement

### **1. Prérequis**
```bash
# Python 3.8+
# Node.js 16+
# npm ou yarn
```

### **2. Backend (Django)**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### **3. Frontend (React)**
```bash
cd frontend
npm install
npm start
```

## 🔧 Configuration Initiale

### **Nettoyer et configurer le système :**
```bash
cd backend
python setup_professional_system.py
```

### **Créer des données de démonstration :**
```bash
cd backend
python demo_professional_workflow.py
```

## 👥 Workflow Professionnel

### **1. Création d'un Développeur**
1. Admin va sur **Utilisateurs**
2. Clique **"Créer & Envoyer Email"**
3. Remplit le formulaire
4. Email automatique envoyé avec identifiants

### **2. Invitation d'un Client**
1. Admin va sur **Utilisateurs**
2. Clique **"Envoyer Invitation"**
3. Saisit email et rôle
4. Clé d'inscription envoyée par email
5. Client crée son compte via le lien

### **3. Connexion**
- **Interface épurée** sans comptes de test
- **Message professionnel** affiché
- **Identifiants fournis par l'admin**

## 📊 Rôles et Permissions

### **🔴 Administrateur**
- Gestion complète des utilisateurs
- Création et envoi d'invitations
- Gestion des projets et tâches
- Statistiques de pointage

### **🟡 Développeur**
- Visualisation des tâches assignées
- Système de pointage
- Mise à jour du statut des tâches

### **🟢 Client**
- Visualisation de ses projets
- Suivi de l'avancement

## ⚙️ Configuration Email (Production)

### **1. Gmail SMTP**
```python
# Dans settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe-app'
```

### **2. Autres Providers**
- **Outlook** : smtp-mail.outlook.com:587
- **Yahoo** : smtp.mail.yahoo.com:587
- **SendGrid** : smtp.sendgrid.net:587

## 🔒 Sécurité

### **Mots de passe**
- **Génération automatique** sécurisée
- **Validation Django** intégrée
- **Changement obligatoire** à la première connexion

### **Clés d'inscription**
- **Expiration** : 7 jours
- **Usage unique**
- **Sécurisées** avec token_urlsafe

## 📱 URLs Importantes

- **Application** : http://localhost:3000
- **API Backend** : http://localhost:8000
- **Admin Django** : http://localhost:8000/admin
- **Inscription** : http://localhost:3000/register?key=XXXXX

## 🛠️ Scripts Utiles

### **Nettoyage du système**
```bash
python setup_professional_system.py
```

### **Démonstration**
```bash
python demo_professional_workflow.py
```

### **Vérification des tâches**
```bash
python check_task_assignments.py
```

## 📈 Statistiques

Le système track automatiquement :
- **Utilisateurs** par rôle
- **Projets** actifs
- **Tâches** assignées
- **Heures travaillées**
- **Retards** et présences

## 🎉 Système Prêt pour la Production !

✅ **Plus de comptes de test**  
✅ **Workflow professionnel**  
✅ **Emails automatiques**  
✅ **Pointage intelligent**  
✅ **Interface épurée**  

---

**Développé pour une gestion professionnelle des projets IT** 🚀
