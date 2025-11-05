# 🚀 Guide d'Exportation pour GitHub

## 📍 **Localisation de la Base PostgreSQL**

### **Où se trouve votre base de données :**

**Windows - Répertoire de données PostgreSQL :**
```
C:\Program Files\PostgreSQL\[version]\data\
```
ou
```
C:\Users\[username]\AppData\Local\PostgreSQL\[version]\data\
```

**Votre base spécifique :** `it_project_management`

## 🗄️ **Méthodes d'Exportation**

### **Méthode 1 : Script Python (Recommandé)**
```bash
cd backend
python export_database.py
```

### **Méthode 2 : Script Batch Windows**
```bash
cd backend
export_db.bat
```

### **Méthode 3 : Commande Manuelle**
```bash
# Exportation complète
pg_dump -h 127.0.0.1 -p 5432 -U postgres -d it_project_management -f backup.sql --clean --create

# Structure seulement
pg_dump -h 127.0.0.1 -p 5432 -U postgres -d it_project_management -f structure.sql --schema-only --clean --create
```

## 📁 **Structure Recommandée pour GitHub**

```
votre-projet/
├── backend/
│   ├── apps/
│   ├── core/
│   └── manage.py
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── database/
│   ├── it_project_management_backup.sql     # Base complète
│   ├── it_project_management_structure.sql  # Structure seulement
│   └── README.md                            # Instructions d'importation
├── docs/
│   └── installation.md
└── README.md
```

## 📋 **Fichiers à Inclure dans GitHub**

### **1. Base de Données :**
- ✅ `it_project_management_backup.sql` - Base complète avec données
- ✅ `it_project_management_structure.sql` - Structure seulement
- ✅ `DATABASE_IMPORT_INSTRUCTIONS.md` - Instructions d'importation

### **2. Configuration :**
- ✅ `requirements.txt` - Dépendances Python
- ✅ `package.json` - Dépendances Node.js
- ✅ `.env.example` - Variables d'environnement exemple

### **3. Documentation :**
- ✅ `README.md` - Guide principal
- ✅ `INSTALLATION.md` - Instructions d'installation
- ✅ `API_DOCUMENTATION.md` - Documentation API

## 🔧 **Commandes d'Exportation Détaillées**

### **Si pg_dump n'est pas dans le PATH :**
```bash
# Windows - Chemin complet
"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" -h 127.0.0.1 -p 5432 -U postgres -d it_project_management -f backup.sql --clean --create
```

### **Avec mot de passe :**
```bash
# Définir la variable d'environnement
set PGPASSWORD=postgres
pg_dump -h 127.0.0.1 -p 5432 -U postgres -d it_project_management -f backup.sql
```

## 📊 **Contenu de la Base Exportée**

Votre base contient :
- **Utilisateurs** : Admin, clients, développeurs
- **Projets** : Projets d'exemple avec budgets en Ariary
- **Tâches** : Tâches assignées aux développeurs
- **Pointage** : Données de suivi du temps
- **Permissions** : Rôles et autorisations

## 🎯 **Instructions pour les Utilisateurs GitHub**

Créez un `README.md` dans le dossier `database/` :

```markdown
# Base de Données IT Project Management

## Installation Rapide

1. Installez PostgreSQL
2. Créez la base : `createdb -U postgres it_project_management`
3. Importez : `psql -U postgres -d it_project_management -f it_project_management_backup.sql`
4. Configurez Django et démarrez : `python manage.py runserver`

## Comptes de Test

- **Admin** : admin@example.com / admin123
- **Client** : client@example.com / client123  
- **Développeur** : dev@example.com / dev123
```

## 🚀 **Étapes pour GitHub**

1. **Exportez la base** :
   ```bash
   cd backend
   python export_database.py
   ```

2. **Créez la structure** :
   ```
   mkdir database
   move *.sql database/
   ```

3. **Ajoutez au Git** :
   ```bash
   git add database/
   git add backend/
   git add frontend/
   git commit -m "Ajout base de données PostgreSQL et projet complet"
   git push origin main
   ```

## 💡 **Conseils**

- **Fichier .gitignore** : N'incluez pas les mots de passe réels
- **Variables d'environnement** : Utilisez `.env` pour la configuration
- **Documentation** : Ajoutez des instructions claires d'installation
- **Tests** : Incluez des données de test pour faciliter les démonstrations

**Votre projet sera prêt pour GitHub avec une base PostgreSQL complète !** 🎉
