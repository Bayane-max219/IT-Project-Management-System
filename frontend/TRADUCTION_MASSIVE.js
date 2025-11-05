// Script pour traduire massivement les textes anglais vers français
const fs = require('fs');
const path = require('path');

// Dictionnaire de traductions
const translations = {
  // Mots courants
  'Dashboard': 'Tableau de bord',
  'Projects': 'Projets',
  'Tasks': 'Tâches', 
  'Users': 'Utilisateurs',
  'Create': 'Créer',
  'Update': 'Modifier',
  'Edit': 'Modifier',
  'Delete': 'Supprimer',
  'Save': 'Enregistrer',
  'Cancel': 'Annuler',
  'Submit': 'Valider',
  'Loading': 'Chargement',
  'Error': 'Erreur',
  'Success': 'Succès',
  'Login': 'Connexion',
  'Register': 'Inscription',
  'Email': 'Email',
  'Password': 'Mot de passe',
  'Name': 'Nom',
  'Description': 'Description',
  'Status': 'Statut',
  'Priority': 'Priorité',
  'Budget': 'Budget',
  'Client': 'Client',
  'Manager': 'Responsable',
  'Developer': 'Développeur',
  'Admin': 'Administrateur',
  'Active': 'Actif',
  'Inactive': 'Inactif',
  'Start Date': 'Date de début',
  'End Date': 'Date de fin',
  'Due Date': 'Date d\'échéance',
  'Progress': 'Progression',
  'Duration': 'Durée',
  'Total': 'Total',
  'Search': 'Rechercher',
  'Filter': 'Filtrer',
  'Export': 'Exporter',
  'Import': 'Importer',
  'View': 'Voir',
  'Details': 'Détails',
  'Close': 'Fermer',
  'Back': 'Retour',
  'Next': 'Suivant',
  'Previous': 'Précédent',
  
  // Messages
  'Loading...': 'Chargement...',
  'No data': 'Aucune donnée',
  'No projects': 'Aucun projet',
  'No tasks': 'Aucune tâche',
  'No users': 'Aucun utilisateur',
  'Are you sure?': 'Êtes-vous sûr ?',
  'Confirm delete': 'Confirmer la suppression',
  'Successfully created': 'Créé avec succès',
  'Successfully updated': 'Modifié avec succès',
  'Successfully deleted': 'Supprimé avec succès',
  'Error loading': 'Erreur lors du chargement',
  'Error saving': 'Erreur lors de la sauvegarde',
  'Error deleting': 'Erreur lors de la suppression',
  
  // Statuts
  'Planning': 'Planification',
  'In Progress': 'En cours',
  'Testing': 'Tests',
  'Completed': 'Terminé',
  'On Hold': 'En pause',
  'Cancelled': 'Annulé',
  'Todo': 'À faire',
  'Done': 'Terminé',
  'Review': 'En révision',
  
  // Priorités
  'Low': 'Basse',
  'Medium': 'Moyenne',
  'High': 'Haute',
  'Urgent': 'Urgente',
  
  // Titres de pages
  'Project Management': 'Gestion des Projets',
  'Task Management': 'Gestion des Tâches',
  'User Management': 'Gestion des Utilisateurs',
  'Time Tracking': 'Suivi du Temps',
  'Statistics': 'Statistiques',
  
  // Formulaires
  'Project Name': 'Nom du projet',
  'Project Description': 'Description du projet',
  'Task Name': 'Nom de la tâche',
  'Task Description': 'Description de la tâche',
  'First Name': 'Prénom',
  'Last Name': 'Nom',
  'Username': 'Nom d\'utilisateur',
  'Role': 'Rôle',
  'Select': 'Sélectionner',
  'Choose': 'Choisir',
  'Optional': 'Optionnel',
  'Required': 'Obligatoire',
  
  // Actions
  'Add New': 'Ajouter nouveau',
  'Create New': 'Créer nouveau',
  'Edit Project': 'Modifier le projet',
  'Delete Project': 'Supprimer le projet',
  'View Project': 'Voir le projet',
  'Assign Task': 'Assigner la tâche',
  'Mark Complete': 'Marquer comme terminé',
  'Start Timer': 'Démarrer le chrono',
  'Stop Timer': 'Arrêter le chrono',
  
  // Navigation
  'My Projects': 'Mes Projets',
  'My Tasks': 'Mes Tâches',
  'All Projects': 'Tous les Projets',
  'All Tasks': 'Toutes les Tâches',
  'All Users': 'Tous les Utilisateurs',
  'Profile': 'Profil',
  'Settings': 'Paramètres',
  'Logout': 'Déconnexion',
  
  // Temps et dates
  'Today': 'Aujourd\'hui',
  'Yesterday': 'Hier',
  'Tomorrow': 'Demain',
  'This Week': 'Cette semaine',
  'This Month': 'Ce mois',
  'Last Week': 'La semaine dernière',
  'Last Month': 'Le mois dernier',
  'Start Time': 'Heure de début',
  'End Time': 'Heure de fin',
  
  // Autres
  'Welcome': 'Bienvenue',
  'Hello': 'Bonjour',
  'Goodbye': 'Au revoir',
  'Thank you': 'Merci',
  'Please': 'S\'il vous plaît',
  'Yes': 'Oui',
  'No': 'Non',
  'OK': 'OK',
  'Help': 'Aide',
  'About': 'À propos',
  'Contact': 'Contact',
  'Support': 'Support',
  'Version': 'Version'
};

function translateFile(filePath) {
  console.log(`\n🔄 Traduction de ${filePath}...`);
  
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Compter les traductions appliquées
    let translationCount = 0;
    
    // Appliquer les traductions
    Object.entries(translations).forEach(([english, french]) => {
      // Patterns pour différents contextes
      const patterns = [
        // Texte entre guillemets simples
        new RegExp(`'${english}'`, 'g'),
        // Texte entre guillemets doubles
        new RegExp(`"${english}"`, 'g'),
        // Texte dans les templates literals
        new RegExp(`\`${english}\``, 'g'),
        // Texte dans les JSX (entre >< )
        new RegExp(`>${english}<`, 'g'),
        // Placeholder dans les inputs
        new RegExp(`placeholder="${english}"`, 'g'),
        new RegExp(`placeholder='${english}'`, 'g'),
        // Titres et labels
        new RegExp(`title="${english}"`, 'g'),
        new RegExp(`title='${english}'`, 'g'),
        new RegExp(`label="${english}"`, 'g'),
        new RegExp(`label='${english}'`, 'g'),
      ];
      
      patterns.forEach(pattern => {
        if (pattern.test(content)) {
          const replacement = pattern.source
            .replace(english, french)
            .replace(/\\\\/g, '\\'); // Fix escaped characters
          
          content = content.replace(pattern, replacement.slice(1, -1)); // Remove /g flags
          modified = true;
          translationCount++;
        }
      });
    });
    
    if (modified) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ ${translationCount} traductions appliquées`);
    } else {
      console.log(`ℹ️ Aucune traduction nécessaire`);
    }
    
    return translationCount;
    
  } catch (error) {
    console.error(`❌ Erreur lors de la traduction de ${filePath}:`, error.message);
    return 0;
  }
}

function translateDirectory(dirPath) {
  console.log(`\n📁 Traduction du répertoire ${dirPath}...`);
  
  let totalTranslations = 0;
  let filesProcessed = 0;
  
  function processDirectory(currentPath) {
    const items = fs.readdirSync(currentPath);
    
    items.forEach(item => {
      const itemPath = path.join(currentPath, item);
      const stat = fs.statSync(itemPath);
      
      if (stat.isDirectory()) {
        // Ignorer node_modules et autres dossiers système
        if (!['node_modules', '.git', 'build', 'dist'].includes(item)) {
          processDirectory(itemPath);
        }
      } else if (stat.isFile() && (item.endsWith('.js') || item.endsWith('.jsx'))) {
        const translations = translateFile(itemPath);
        totalTranslations += translations;
        filesProcessed++;
      }
    });
  }
  
  processDirectory(dirPath);
  
  console.log(`\n📊 RÉSUMÉ:`);
  console.log(`- Fichiers traités: ${filesProcessed}`);
  console.log(`- Total traductions: ${totalTranslations}`);
  
  return { filesProcessed, totalTranslations };
}

// Fonction principale
function main() {
  console.log('🌍 TRADUCTION MASSIVE ANGLAIS → FRANÇAIS');
  console.log('=====================================');
  
  const srcPath = path.join(__dirname, 'src');
  
  if (!fs.existsSync(srcPath)) {
    console.error('❌ Dossier src/ non trouvé');
    return;
  }
  
  const result = translateDirectory(srcPath);
  
  console.log('\n🎉 TRADUCTION TERMINÉE!');
  console.log(`📈 ${result.totalTranslations} traductions appliquées sur ${result.filesProcessed} fichiers`);
  console.log('\n💡 Conseils:');
  console.log('1. Vérifiez les fichiers modifiés');
  console.log('2. Testez l\'application');
  console.log('3. Ajustez manuellement si nécessaire');
}

// Exécuter si appelé directement
if (require.main === module) {
  main();
}

module.exports = { translateFile, translateDirectory, translations };
