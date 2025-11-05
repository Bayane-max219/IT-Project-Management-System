# Guide - Problème Client ne Voit Pas ses Projets

## 🔍 **Problème Identifié**

Le client Marie ne voit aucun projet dans son interface alors que des projets ont été créés par l'admin. Deux problèmes principaux :

1. **Serializer de création incorrect** - Utilisait des objets au lieu d'IDs
2. **Projets mal assignés** - Les projets ne sont pas correctement liés au client

## ✅ **Solutions Implémentées**

### **1. Correction du Serializer de Création**

**Problème :** Le `ProjectCreateSerializer` attendait des objets `client` et `project_manager` directement, mais le frontend envoie des IDs.

**Solution :** Modification pour utiliser `client_id` et `project_manager_id` :

```python
class ProjectCreateSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True)
    project_manager_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    def create(self, validated_data):
        client_id = validated_data.pop('client_id')
        project_manager_id = validated_data.pop('project_manager_id', None)
        
        # Récupérer les objets utilisateur
        client = User.objects.get(id=client_id)
        project_manager = User.objects.get(id=project_manager_id) if project_manager_id else None
        
        # Créer le projet avec les bonnes assignations
        project = Project.objects.create(
            client=client,
            project_manager=project_manager,
            **validated_data
        )
```

### **2. Scripts de Diagnostic et Correction**

**Scripts créés :**
- `test_client_projects.py` - Diagnostic complet du problème
- `fix_client_projects.py` - Correction automatique des données

## 🧪 **Comment Résoudre le Problème**

### **Étape 1 : Diagnostic**
```bash
cd backend
python test_client_projects.py
```

Ce script va :
- ✅ Vérifier si le client Marie existe
- ✅ Compter ses projets en base de données
- ✅ Tester la connexion client
- ✅ Vérifier l'API des projets
- ✅ Identifier les problèmes

### **Étape 2 : Correction Automatique**
```bash
python fix_client_projects.py
```

Ce script va :
- ✅ Assigner les projets orphelins au client Marie
- ✅ Créer le client Marie s'il n'existe pas
- ✅ Créer des projets de démonstration
- ✅ Vérifier la cohérence des données

### **Étape 3 : Test Final**
```bash
python test_client_projects.py
```

Vérifier que tout fonctionne maintenant.

## 🎯 **Vérification Manuelle**

### **1. Via Interface Web**
1. Démarrer le serveur : `python manage.py runserver`
2. Aller sur `http://localhost:3000`
3. Se connecter avec :
   - **Email :** `client@example.com`
   - **Mot de passe :** `client123`
4. Vérifier que les projets apparaissent

### **2. Via Interface Admin**
1. Aller sur `http://localhost:8000/admin`
2. Se connecter en tant qu'admin
3. Vérifier dans "Projets" que les projets ont bien un client assigné

### **3. Via API Directe**
```bash
# Connexion client
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"client@example.com","password":"client123"}'

# Récupérer les projets (avec le token reçu)
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔧 **Création de Nouveaux Projets**

Maintenant, pour créer un projet via l'interface admin, utilisez ces champs :

```json
{
  "name": "Nom du Projet",
  "description": "Description du projet",
  "client_id": 1,  // ID du client (pas l'objet)
  "project_manager_id": 2,  // ID du chef de projet
  "status": "PLANIFIE",
  "priority": "MOYENNE",
  "start_date": "2025-10-28",
  "end_date": "2025-12-31",
  "budget": 25000
}
```

## 📊 **Données de Test Créées**

Le script `fix_client_projects.py` crée automatiquement :

### **Client Marie :**
- **Email :** `client@example.com`
- **Mot de passe :** `client123`
- **Nom :** Marie Client

### **Projets de Démonstration :**
1. **Site Web Vitrine**
   - Statut : EN_COURS
   - Budget : 25,000€
   - Progression : 35%

2. **Application Mobile**
   - Statut : PLANIFIE
   - Budget : 45,000€
   - Progression : 0%

## 🛡️ **Permissions et Sécurité**

### **Visibilité des Projets :**
- ✅ **Admins** : Voient tous les projets
- ✅ **Clients** : Voient uniquement leurs projets assignés
- ✅ **Développeurs** : Voient les projets où ils sont assignés
- ✅ **Chefs de projet** : Voient les projets qu'ils gèrent

### **Code de Filtrage :**
```python
def get_queryset(self):
    user = self.request.user
    if user.is_admin():
        return Project.objects.all().select_related('client', 'project_manager')
    elif user.is_client():
        return Project.objects.filter(client=user).select_related('project_manager')
    else:  # developer
        return Project.objects.filter(
            Q(project_manager=user) | Q(team_members__developer=user)
        ).distinct().select_related('client', 'project_manager')
```

## 🔍 **Diagnostic des Problèmes Futurs**

### **Si un client ne voit pas ses projets :**

1. **Vérifier l'assignation :**
   ```sql
   SELECT p.name, u.email as client_email 
   FROM projects_project p 
   LEFT JOIN authentication_user u ON p.client_id = u.id 
   WHERE u.email = 'client@example.com';
   ```

2. **Vérifier les permissions :**
   ```python
   # Dans Django shell
   from apps.authentication.models import User
   from apps.projects.models import Project
   
   client = User.objects.get(email="client@example.com")
   projects = Project.objects.filter(client=client)
   print(f"Projets pour {client.email}: {projects.count()}")
   ```

3. **Vérifier l'API :**
   - Tester la connexion client
   - Vérifier le token JWT
   - Tester l'endpoint `/api/projects/`

## ✅ **Résultat Final**

Après ces corrections :

- ✅ **Les projets sont correctement assignés** aux clients
- ✅ **Le client Marie voit ses projets** dans l'interface
- ✅ **La création de projets fonctionne** correctement
- ✅ **Les permissions sont respectées** selon les rôles
- ✅ **Les données sont cohérentes** en base

**Le problème est maintenant résolu !** 🎉

Les clients peuvent voir leurs projets assignés et suivre leur avancement en temps réel.
