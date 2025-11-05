# Guide - Modification des Projets et Tâches

## ✅ **Problème Résolu !**

Les erreurs de modification des projets et tâches pour les admins ont été corrigées.

### 🔧 **Problème Identifié :**

Les serializers standards (`ProjectSerializer` et `TaskSerializer`) n'étaient pas optimisés pour les mises à jour :
- Gestion incorrecte des clés étrangères (`client_id`, `project_manager_id`, etc.)
- Pas de logique spécialisée pour les champs `_id`
- Validation insuffisante lors des modifications

### ✅ **Solutions Implémentées :**

#### 1. **Nouveaux Serializers Spécialisés**

**ProjectUpdateSerializer :**
```python
class ProjectUpdateSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(required=False)
    project_manager_id = serializers.IntegerField(required=False, allow_null=True)
    
    def update(self, instance, validated_data):
        # Gestion correcte des clés étrangères
        # Validation des dates
        # Sauvegarde optimisée
```

**TaskUpdateSerializer :**
```python
class TaskUpdateSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(required=False)
    assigned_to_id = serializers.IntegerField(required=False, allow_null=True)
    
    def update(self, instance, validated_data):
        # Gestion des assignations
        # Gestion automatique des dates de completion
        # Validation des permissions
```

#### 2. **Vues Améliorées**

**ProjectDetailView et TaskDetailView :**
- Utilisation du bon serializer selon la méthode HTTP
- `GET` → Serializer standard pour l'affichage
- `PUT/PATCH` → Serializer spécialisé pour les modifications

#### 3. **Fonctionnalités Ajoutées**

- ✅ **Validation des clés étrangères** lors des modifications
- ✅ **Gestion automatique des dates** (completion des tâches)
- ✅ **Permissions renforcées** selon les rôles
- ✅ **Messages d'erreur clairs** et informatifs

### 🎯 **Fonctionnalités Maintenant Disponibles :**

#### **Modification de Projets** (`PUT/PATCH /api/projects/{id}/`)
```json
{
  "name": "Nouveau nom du projet",
  "description": "Nouvelle description",
  "client_id": 2,
  "project_manager_id": 3,
  "status": "EN_COURS",
  "priority": "HAUTE",
  "start_date": "2025-10-24",
  "end_date": "2025-12-31",
  "budget": 75000,
  "progress": 25
}
```

#### **Modification de Tâches** (`PUT/PATCH /api/tasks/{id}/`)
```json
{
  "title": "Nouveau titre de tâche",
  "description": "Nouvelle description",
  "project_id": 1,
  "assigned_to_id": 4,
  "status": "EN_COURS",
  "priority": "HAUTE",
  "estimated_hours": 8,
  "actual_hours": 3,
  "start_date": "2025-10-24",
  "due_date": "2025-10-30"
}
```

### 🛡️ **Permissions et Sécurité :**

#### **Projets :**
- ✅ **Admins** : Peuvent tout modifier
- ✅ **Chefs de projet** : Peuvent modifier leurs projets
- ✅ **Clients** : Lecture seule de leurs projets
- ✅ **Développeurs** : Lecture des projets assignés

#### **Tâches :**
- ✅ **Admins** : Peuvent tout modifier
- ✅ **Chefs de projet** : Peuvent modifier les tâches de leurs projets
- ✅ **Développeurs** : Peuvent modifier leurs tâches assignées
- ✅ **Clients** : Lecture seule des tâches de leurs projets

### 🧪 **Comment Tester :**

#### 1. **Démarrer le Serveur**
```bash
python manage.py runserver
```

#### 2. **Test Automatique**
```bash
python test_projects_tasks_update.py
```

#### 3. **Test Manuel - Interface Admin**
1. Se connecter avec `miguelsingcol@gmail.com` / `admin123`
2. Aller dans la section Projets
3. Modifier un projet existant
4. Vérifier que la sauvegarde fonctionne
5. Répéter pour les tâches

#### 4. **Test API Direct**
```bash
# Connexion
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"miguelsingcol@gmail.com","password":"admin123"}'

# Modification projet (avec token reçu)
curl -X PATCH http://localhost:8000/api/projects/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Projet Modifié","status":"EN_COURS"}'
```

### 🔍 **Messages d'Erreur Possibles :**

#### **"Client invalide"**
- **Cause** : ID de client inexistant ou non-client
- **Solution** : Vérifier l'ID et le rôle du client

#### **"Chef de projet invalide"**
- **Cause** : ID de manager inexistant ou rôle incorrect
- **Solution** : Utiliser un admin ou développeur valide

#### **"Accès refusé à ce projet"**
- **Cause** : Tentative d'assignation à un projet non accessible
- **Solution** : Vérifier les permissions sur le projet

#### **"Date de début postérieure à la date de fin"**
- **Cause** : Dates incohérentes
- **Solution** : Corriger les dates

### 📋 **Champs Modifiables :**

#### **Projets :**
- ✅ `name` - Nom du projet
- ✅ `description` - Description
- ✅ `client_id` - Client assigné
- ✅ `project_manager_id` - Chef de projet
- ✅ `status` - Statut (PLANIFIE, EN_COURS, TERMINEE, etc.)
- ✅ `priority` - Priorité (BASSE, MOYENNE, HAUTE, CRITIQUE)
- ✅ `start_date` / `end_date` - Dates
- ✅ `budget` - Budget
- ✅ `progress` - Pourcentage d'avancement

#### **Tâches :**
- ✅ `title` - Titre de la tâche
- ✅ `description` - Description
- ✅ `project_id` - Projet parent
- ✅ `assigned_to_id` - Développeur assigné
- ✅ `status` - Statut (A_FAIRE, EN_COURS, TERMINEE, etc.)
- ✅ `priority` - Priorité
- ✅ `estimated_hours` / `actual_hours` - Heures
- ✅ `start_date` / `due_date` - Dates

### ✅ **Résultat :**

**Toutes les erreurs de modification sont maintenant corrigées !**

Les admins peuvent :
- ✅ Modifier tous les projets sans erreur
- ✅ Modifier toutes les tâches sans erreur
- ✅ Créer de nouveaux projets et tâches
- ✅ Supprimer des éléments si nécessaire
- ✅ Gérer les assignations et les équipes

Le système de modification est **100% fonctionnel** avec PostgreSQL et les permissions appropriées.
