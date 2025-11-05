# Formation PostgreSQL Pratique - Projet IT Management

## 🎯 **Objectif**
Apprendre PostgreSQL de manière pratique en utilisant votre projet de gestion IT comme cas d'étude.

## 📚 **Plan de Formation**

### **Module 1 : Comprendre la Structure de la Base**
### **Module 2 : Requêtes de Base (SELECT, INSERT, UPDATE, DELETE)**
### **Module 3 : Jointures et Relations**
### **Module 4 : Fonctions Avancées et Statistiques**
### **Module 5 : Optimisation et Performance**

---

## 🔧 **Module 1 : Structure de la Base de Données**

### **1.1 Connexion à PostgreSQL**

```bash
# Méthode 1 : Via psql (si installé)
psql -h localhost -U postgres -d it_project_management

# Méthode 2 : Via Django shell
python manage.py dbshell
```

### **1.2 Explorer la Structure**

```sql
-- Lister toutes les tables
\dt

-- Voir la structure d'une table
\d authentication_user
\d projects_project
\d tasks_task

-- Voir toutes les bases de données
\l

-- Voir les utilisateurs PostgreSQL
\du
```

### **1.3 Comprendre les Tables de Votre Projet**

```sql
-- Table des utilisateurs
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'authentication_user';

-- Table des projets
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'projects_project';

-- Table des tâches
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'tasks_task';
```

---

## 📊 **Module 2 : Requêtes de Base**

### **2.1 SELECT - Lire les Données**

```sql
-- Voir tous les utilisateurs
SELECT id, username, email, role, first_name, last_name 
FROM authentication_user;

-- Voir seulement les admins
SELECT username, email, first_name, last_name 
FROM authentication_user 
WHERE role = 'admin';

-- Compter les utilisateurs par rôle
SELECT role, COUNT(*) as nombre 
FROM authentication_user 
GROUP BY role;

-- Voir les projets avec leurs statuts
SELECT name, status, priority, start_date, end_date, budget 
FROM projects_project 
ORDER BY start_date DESC;

-- Voir les tâches en cours
SELECT title, status, priority, estimated_hours, due_date 
FROM tasks_task 
WHERE status = 'EN_COURS';
```

### **2.2 INSERT - Ajouter des Données**

```sql
-- Ajouter un nouveau client (exemple)
INSERT INTO authentication_user (
    username, email, first_name, last_name, role, 
    is_active, date_joined, password
) VALUES (
    'nouveau_client', 'client@test.com', 'Jean', 'Dupont', 'client',
    true, NOW(), 'pbkdf2_sha256$...'  -- Mot de passe hashé
);

-- Ajouter un projet
INSERT INTO projects_project (
    name, description, status, priority, 
    start_date, end_date, budget, progress,
    client_id, created_at, updated_at
) VALUES (
    'Projet Formation PostgreSQL', 
    'Projet pour apprendre PostgreSQL',
    'PLANIFIE', 'MOYENNE',
    '2025-10-27', '2025-12-31', 25000, 0,
    1, NOW(), NOW()
);
```

### **2.3 UPDATE - Modifier des Données**

```sql
-- Mettre à jour le statut d'un projet
UPDATE projects_project 
SET status = 'EN_COURS', progress = 25, updated_at = NOW()
WHERE name = 'Projet Formation PostgreSQL';

-- Mettre à jour les heures réelles d'une tâche
UPDATE tasks_task 
SET actual_hours = 5, updated_at = NOW()
WHERE title LIKE '%Formation%';

-- Augmenter le budget de tous les projets de 10%
UPDATE projects_project 
SET budget = budget * 1.10, updated_at = NOW()
WHERE status != 'TERMINEE';
```

### **2.4 DELETE - Supprimer des Données**

```sql
-- Supprimer les tâches terminées depuis plus de 6 mois
DELETE FROM tasks_task 
WHERE status = 'TERMINEE' 
AND completed_at < NOW() - INTERVAL '6 months';

-- Supprimer un projet spécifique (attention aux contraintes!)
DELETE FROM projects_project 
WHERE name = 'Projet Test' 
AND status = 'ANNULE';
```

---

## 🔗 **Module 3 : Jointures et Relations**

### **3.1 INNER JOIN - Données Liées**

```sql
-- Projets avec leurs clients
SELECT 
    p.name as projet_nom,
    p.status as projet_statut,
    u.first_name || ' ' || u.last_name as client_nom,
    u.email as client_email
FROM projects_project p
INNER JOIN authentication_user u ON p.client_id = u.id
WHERE u.role = 'client';

-- Tâches avec leurs projets et développeurs assignés
SELECT 
    t.title as tache_titre,
    t.status as tache_statut,
    p.name as projet_nom,
    dev.first_name || ' ' || dev.last_name as developpeur
FROM tasks_task t
INNER JOIN projects_project p ON t.project_id = p.id
LEFT JOIN authentication_user dev ON t.assigned_to_id = dev.id;
```

### **3.2 LEFT JOIN - Inclure les Données Manquantes**

```sql
-- Tous les projets, même sans tâches
SELECT 
    p.name as projet,
    COUNT(t.id) as nombre_taches,
    COALESCE(AVG(t.progress), 0) as progression_moyenne
FROM projects_project p
LEFT JOIN tasks_task t ON p.id = t.project_id
GROUP BY p.id, p.name
ORDER BY nombre_taches DESC;

-- Tous les développeurs, même sans tâches assignées
SELECT 
    u.first_name || ' ' || u.last_name as developpeur,
    COUNT(t.id) as taches_assignees,
    SUM(t.estimated_hours) as heures_estimees_total
FROM authentication_user u
LEFT JOIN tasks_task t ON u.id = t.assigned_to_id
WHERE u.role = 'developer'
GROUP BY u.id, u.first_name, u.last_name;
```

### **3.3 Requêtes Complexes avec Sous-requêtes**

```sql
-- Projets avec le plus de tâches
SELECT 
    p.name,
    p.status,
    (SELECT COUNT(*) FROM tasks_task t WHERE t.project_id = p.id) as nb_taches
FROM projects_project p
WHERE (SELECT COUNT(*) FROM tasks_task t WHERE t.project_id = p.id) > 5;

-- Développeurs les plus occupés
SELECT 
    u.first_name || ' ' || u.last_name as developpeur,
    (SELECT COUNT(*) FROM tasks_task t WHERE t.assigned_to_id = u.id AND t.status != 'TERMINEE') as taches_actives,
    (SELECT SUM(estimated_hours) FROM tasks_task t WHERE t.assigned_to_id = u.id AND t.status != 'TERMINEE') as heures_restantes
FROM authentication_user u
WHERE u.role = 'developer'
ORDER BY taches_actives DESC;
```

---

## 📈 **Module 4 : Fonctions Avancées et Statistiques**

### **4.1 Fonctions d'Agrégation**

```sql
-- Statistiques générales du système
SELECT 
    COUNT(*) as total_projets,
    COUNT(CASE WHEN status = 'EN_COURS' THEN 1 END) as projets_actifs,
    COUNT(CASE WHEN status = 'TERMINEE' THEN 1 END) as projets_termines,
    AVG(budget) as budget_moyen,
    SUM(budget) as budget_total
FROM projects_project;

-- Statistiques par mois
SELECT 
    DATE_TRUNC('month', created_at) as mois,
    COUNT(*) as nouveaux_projets,
    AVG(budget) as budget_moyen_mensuel
FROM projects_project
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY mois DESC;
```

### **4.2 Fonctions de Date**

```sql
-- Projets en retard
SELECT 
    name,
    end_date,
    CURRENT_DATE - end_date as jours_retard,
    status
FROM projects_project
WHERE end_date < CURRENT_DATE AND status != 'TERMINEE';

-- Tâches par semaine
SELECT 
    DATE_TRUNC('week', created_at) as semaine,
    COUNT(*) as nouvelles_taches
FROM tasks_task
WHERE created_at >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY DATE_TRUNC('week', created_at)
ORDER BY semaine;
```

### **4.3 Fonctions de Chaîne**

```sql
-- Recherche dans les descriptions
SELECT 
    name,
    description,
    LENGTH(description) as longueur_description
FROM projects_project
WHERE LOWER(description) LIKE '%web%' OR LOWER(description) LIKE '%mobile%';

-- Formater les noms d'utilisateurs
SELECT 
    UPPER(SUBSTRING(first_name, 1, 1)) || LOWER(SUBSTRING(first_name, 2)) || ' ' ||
    UPPER(SUBSTRING(last_name, 1, 1)) || LOWER(SUBSTRING(last_name, 2)) as nom_formate,
    email
FROM authentication_user
WHERE role = 'client';
```

---

## ⚡ **Module 5 : Optimisation et Performance**

### **5.1 Index et Performance**

```sql
-- Voir les index existants
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename IN ('authentication_user', 'projects_project', 'tasks_task');

-- Créer des index pour améliorer les performances
CREATE INDEX idx_tasks_status ON tasks_task(status);
CREATE INDEX idx_projects_client ON projects_project(client_id);
CREATE INDEX idx_tasks_assigned_to ON tasks_task(assigned_to_id);

-- Analyser les performances d'une requête
EXPLAIN ANALYZE
SELECT p.name, COUNT(t.id) as nb_taches
FROM projects_project p
LEFT JOIN tasks_task t ON p.id = t.project_id
GROUP BY p.id, p.name;
```

### **5.2 Vues pour Simplifier les Requêtes**

```sql
-- Créer une vue pour les statistiques de projets
CREATE VIEW vue_stats_projets AS
SELECT 
    p.id,
    p.name,
    p.status,
    p.budget,
    u.first_name || ' ' || u.last_name as client_nom,
    COUNT(t.id) as nombre_taches,
    COUNT(CASE WHEN t.status = 'TERMINEE' THEN 1 END) as taches_terminees,
    ROUND(
        COUNT(CASE WHEN t.status = 'TERMINEE' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(t.id), 0), 2
    ) as pourcentage_completion
FROM projects_project p
LEFT JOIN authentication_user u ON p.client_id = u.id
LEFT JOIN tasks_task t ON p.id = t.project_id
GROUP BY p.id, p.name, p.status, p.budget, u.first_name, u.last_name;

-- Utiliser la vue
SELECT * FROM vue_stats_projets WHERE pourcentage_completion > 50;
```

### **5.3 Fonctions Personnalisées**

```sql
-- Fonction pour calculer les jours ouvrables
CREATE OR REPLACE FUNCTION jours_ouvrables(date_debut DATE, date_fin DATE)
RETURNS INTEGER AS $$
DECLARE
    jours INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO jours
    FROM generate_series(date_debut, date_fin, '1 day'::interval) AS d
    WHERE EXTRACT(DOW FROM d) BETWEEN 1 AND 5;
    
    RETURN jours;
END;
$$ LANGUAGE plpgsql;

-- Utiliser la fonction
SELECT 
    name,
    start_date,
    end_date,
    jours_ouvrables(start_date, end_date) as jours_travail
FROM projects_project
WHERE status = 'EN_COURS';
```

---

## 🎯 **Exercices Pratiques**

### **Exercice 1 : Tableau de Bord**
Créez une requête qui affiche :
- Nombre total de projets par statut
- Budget total par statut
- Nombre de tâches en retard
- Top 5 des développeurs les plus occupés

### **Exercice 2 : Rapport Mensuel**
Créez une requête pour un rapport mensuel avec :
- Nouveaux projets créés ce mois
- Projets terminés ce mois
- Heures travaillées par développeur
- Budget total des nouveaux contrats

### **Exercice 3 : Optimisation**
- Identifiez les requêtes lentes avec EXPLAIN
- Créez les index appropriés
- Mesurez l'amélioration des performances

---

## 🛠️ **Scripts Pratiques pour Votre Projet**

### **Script de Monitoring**
```sql
-- Surveillance quotidienne
SELECT 
    'Projets actifs' as metric, COUNT(*)::text as valeur
FROM projects_project WHERE status = 'EN_COURS'
UNION ALL
SELECT 
    'Tâches en retard', COUNT(*)::text
FROM tasks_task WHERE due_date < CURRENT_DATE AND status != 'TERMINEE'
UNION ALL
SELECT 
    'Utilisateurs actifs', COUNT(*)::text
FROM authentication_user WHERE is_active = true;
```

### **Script de Nettoyage**
```sql
-- Nettoyer les données anciennes (à utiliser avec précaution)
DELETE FROM tasks_task 
WHERE status = 'TERMINEE' 
AND completed_at < CURRENT_DATE - INTERVAL '1 year';

-- Archiver les projets terminés
UPDATE projects_project 
SET status = 'ARCHIVE' 
WHERE status = 'TERMINEE' 
AND updated_at < CURRENT_DATE - INTERVAL '6 months';
```

---

## 📝 **Commandes Utiles à Retenir**

```sql
-- Sauvegarder la base
pg_dump -h localhost -U postgres it_project_management > backup.sql

-- Restaurer la base
psql -h localhost -U postgres -d it_project_management < backup.sql

-- Voir la taille des tables
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) as taille
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;

-- Voir les connexions actives
SELECT pid, usename, application_name, state, query_start
FROM pg_stat_activity
WHERE state = 'active';
```

---

## 🎓 **Prochaines Étapes**

1. **Pratiquez** chaque module avec vos vraies données
2. **Créez** vos propres requêtes pour vos besoins spécifiques
3. **Optimisez** les performances selon votre usage
4. **Explorez** les fonctionnalités avancées (triggers, procédures stockées)
5. **Apprenez** la sauvegarde et la restauration

**PostgreSQL est maintenant votre outil de travail quotidien !** 🚀
