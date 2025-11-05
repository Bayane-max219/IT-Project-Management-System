# 👥 Gestion des Utilisateurs PostgreSQL

## 📋 Scripts Disponibles

J'ai créé 2 scripts pour vous aider :

### **1. `voir_utilisateurs.py`** - Voir tous les utilisateurs
### **2. `reset_password.py`** - Réinitialiser un mot de passe

---

## 🔍 Voir Tous les Utilisateurs

### **Commande**

```bash
cd "c:\Users\Miguel\Desktop\Applikcation Octobre\Gestion de Projet IT\backend"

python voir_utilisateurs.py
```

### **Résultat**

Vous verrez quelque chose comme :

```
================================================================================
  LISTE DES UTILISATEURS
================================================================================

Total : 5 utilisateur(s)

────────────────────────────────────────────────────────────────────────────────
👑 ADMINISTRATEURS
────────────────────────────────────────────────────────────────────────────────

  ID: 1
  Email: admin@example.com
  Username: admin
  Nom: Admin User
  Actif: ✅ Oui
  Dernière connexion: 2025-10-31 09:30:00

────────────────────────────────────────────────────────────────────────────────
💻 DÉVELOPPEURS
────────────────────────────────────────────────────────────────────────────────

  ID: 2
  Email: rakoto@example.com
  Username: rakoto
  Nom: Rakoto Developer
  Actif: ✅ Oui
  Dernière connexion: 2025-10-30 14:20:00

  ID: 3
  Email: rabe@example.com
  Username: rabe
  Nom: Rabe Developer
  Actif: ✅ Oui
  Dernière connexion: Jamais

────────────────────────────────────────────────────────────────────────────────
👤 CLIENTS
────────────────────────────────────────────────────────────────────────────────

  ID: 4
  Email: marie@example.com
  Username: marie
  Nom: Marie Client
  Actif: ✅ Oui
  Dernière connexion: 2025-10-29 10:15:00

================================================================================

⚠️  NOTE: Les mots de passe sont hashés et ne peuvent pas être affichés.
   Pour réinitialiser un mot de passe, utilisez le script 'reset_password.py'
```

---

## 🔑 Réinitialiser un Mot de Passe

### **Commande**

```bash
cd "c:\Users\Miguel\Desktop\Applikcation Octobre\Gestion de Projet IT\backend"

python reset_password.py
```

### **Étapes Interactives**

```
================================================================================
  RÉINITIALISATION DE MOT DE PASSE
================================================================================

Utilisateurs disponibles :

1. 👑 admin@example.com - Admin User (admin)
2. 💻 rakoto@example.com - Rakoto Developer (developer)
3. 💻 rabe@example.com - Rabe Developer (developer)
4. 👤 marie@example.com - Marie Client (client)

────────────────────────────────────────────────────────────────────────────────

Numéro de l'utilisateur (ou 'q' pour quitter) : 2

✅ Utilisateur sélectionné : rakoto@example.com
   Nom : Rakoto Developer
   Rôle : developer

────────────────────────────────────────────────────────────────────────────────

Nouveau mot de passe (minimum 6 caractères) : Test123

⚠️  Confirmer le changement de mot de passe pour rakoto@example.com ? (oui/non) : oui

================================================================================
✅ MOT DE PASSE RÉINITIALISÉ AVEC SUCCÈS !
================================================================================

Email : rakoto@example.com
Nouveau mot de passe : Test123

⚠️  IMPORTANT : Notez bien ce mot de passe !
```

---

## 📊 Méthode Alternative : Django Admin

### **Étape 1 : Créer un superutilisateur (si nécessaire)**

```bash
cd backend
python manage.py createsuperuser
```

### **Étape 2 : Accéder à l'admin**

```
URL : http://127.0.0.1:8000/admin
```

### **Étape 3 : Se connecter et gérer les utilisateurs**

1. Connectez-vous avec le superutilisateur
2. Cliquez sur "Users"
3. Vous pouvez voir, modifier, ou supprimer des utilisateurs
4. Pour changer un mot de passe : Cliquez sur un utilisateur → "Change password"

---

## 🗄️ Méthode PostgreSQL Direct (Avancé)

### **Ouvrir pgAdmin ou psql**

```bash
psql -U postgres -d it_project_management
```

### **Voir tous les utilisateurs**

```sql
SELECT id, email, username, first_name, last_name, role, is_active 
FROM users 
ORDER BY role, email;
```

### **Résultat**

```
 id |        email         | username | first_name | last_name |   role    | is_active
----+----------------------+----------+------------+-----------+-----------+-----------
  1 | admin@example.com    | admin    | Admin      | User      | admin     | t
  2 | rakoto@example.com   | rakoto   | Rakoto     | Developer | developer | t
  3 | rabe@example.com     | rabe     | Rabe       | Developer | developer | t
  4 | marie@example.com    | marie    | Marie      | Client    | client    | t
```

---

## 💡 Conseils

### **Pour se connecter à l'application**

Utilisez :
- **Email** : L'email de l'utilisateur (ex: `rakoto@example.com`)
- **Mot de passe** : Le mot de passe que vous avez défini

### **Si vous oubliez le mot de passe**

1. Utilisez `reset_password.py` pour le réinitialiser
2. Ou créez un nouveau compte

### **Mots de passe par défaut (si vous avez utilisé les scripts de création)**

Généralement :
- Admin : `admin123`
- Développeurs : `dev123` ou `password123`
- Clients : `client123`

---

## 🚀 Utilisation Rapide

### **Scénario 1 : Voir tous les comptes**

```bash
cd backend
python voir_utilisateurs.py
```

### **Scénario 2 : Réinitialiser le mot de passe d'un développeur**

```bash
cd backend
python reset_password.py
# Choisir le numéro du développeur
# Entrer le nouveau mot de passe
# Confirmer
```

### **Scénario 3 : Se connecter avec le nouveau mot de passe**

```
1. Aller sur http://localhost:3000
2. Email : rakoto@example.com
3. Mot de passe : [le nouveau mot de passe]
4. Se connecter
```

---

## ✅ Checklist

- [ ] Exécuter `voir_utilisateurs.py` pour voir tous les comptes
- [ ] Noter les emails des développeurs
- [ ] Utiliser `reset_password.py` pour réinitialiser un mot de passe
- [ ] Tester la connexion avec le nouveau mot de passe
- [ ] Noter le mot de passe quelque part en sécurité

---

## 📝 Exemples de Comptes Typiques

### **Admin**
- Email : `admin@example.com`
- Username : `admin`
- Rôle : Administrateur

### **Développeur 1**
- Email : `rakoto@example.com`
- Username : `rakoto`
- Rôle : Développeur

### **Développeur 2**
- Email : `rabe@example.com`
- Username : `rabe`
- Rôle : Développeur

### **Client**
- Email : `marie@example.com`
- Username : `marie`
- Rôle : Client

---

**Date** : 31 Octobre 2025, 10h05
**Statut** : ✅ **SCRIPTS CRÉÉS**

**Utilisez `voir_utilisateurs.py` pour voir tous les comptes ! 🚀**
