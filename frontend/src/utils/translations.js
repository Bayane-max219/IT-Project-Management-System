// Traductions français pour l'application IT Project Manager

export const translations = {
  // Navigation et menus
  dashboard: "Tableau de bord",
  projects: "Projets", 
  tasks: "Tâches",
  users: "Utilisateurs",
  pointage: "Pointage",
  statistics: "Statistiques",
  profile: "Profil",
  logout: "Déconnexion",
  
  // Actions générales
  create: "Créer",
  edit: "Modifier",
  delete: "Supprimer",
  save: "Enregistrer",
  cancel: "Annuler",
  submit: "Valider",
  close: "Fermer",
  add: "Ajouter",
  update: "Mettre à jour",
  view: "Voir",
  details: "Détails",
  back: "Retour",
  next: "Suivant",
  previous: "Précédent",
  search: "Rechercher",
  filter: "Filtrer",
  export: "Exporter",
  import: "Importer",
  
  // États et statuts
  loading: "Chargement...",
  success: "Succès",
  error: "Erreur",
  warning: "Attention",
  info: "Information",
  
  // Authentification
  login: "Connexion",
  register: "Inscription",
  email: "Email",
  password: "Mot de passe",
  confirmPassword: "Confirmer le mot de passe",
  forgotPassword: "Mot de passe oublié",
  rememberMe: "Se souvenir de moi",
  
  // Utilisateurs
  firstName: "Prénom",
  lastName: "Nom",
  username: "Nom d'utilisateur",
  role: "Rôle",
  admin: "Administrateur",
  client: "Client",
  developer: "Développeur",
  active: "Actif",
  inactive: "Inactif",
  
  // Projets
  projectName: "Nom du projet",
  projectDescription: "Description du projet",
  projectManager: "Chef de projet",
  projectClient: "Client",
  projectStatus: "Statut du projet",
  projectPriority: "Priorité",
  projectBudget: "Budget",
  projectStartDate: "Date de début",
  projectEndDate: "Date de fin",
  projectProgress: "Progression",
  
  // Statuts de projet
  planning: "Planification",
  inProgress: "En cours",
  testing: "Tests",
  completed: "Terminé",
  onHold: "En pause",
  cancelled: "Annulé",
  
  // Priorités
  low: "Basse",
  medium: "Moyenne", 
  high: "Haute",
  urgent: "Urgente",
  
  // Tâches
  taskName: "Nom de la tâche",
  taskDescription: "Description de la tâche",
  taskProject: "Projet",
  taskAssignee: "Assigné à",
  taskStatus: "Statut de la tâche",
  taskPriority: "Priorité de la tâche",
  taskDueDate: "Date d'échéance",
  taskEstimatedHours: "Heures estimées",
  taskActualHours: "Heures réelles",
  
  // Statuts de tâche
  todo: "À faire",
  inProgressTask: "En cours",
  review: "En révision",
  done: "Terminé",
  
  // Pointage
  startTime: "Heure de début",
  endTime: "Heure de fin",
  duration: "Durée",
  description: "Description",
  date: "Date",
  
  // Messages
  noData: "Aucune donnée disponible",
  noProjects: "Aucun projet",
  noTasks: "Aucune tâche",
  noUsers: "Aucun utilisateur",
  
  // Messages de succès
  projectCreated: "Projet créé avec succès !",
  projectUpdated: "Projet modifié avec succès !",
  projectDeleted: "Projet supprimé avec succès !",
  taskCreated: "Tâche créée avec succès !",
  taskUpdated: "Tâche modifiée avec succès !",
  taskDeleted: "Tâche supprimée avec succès !",
  userCreated: "Utilisateur créé avec succès !",
  userUpdated: "Utilisateur modifié avec succès !",
  userDeleted: "Utilisateur supprimé avec succès !",
  
  // Messages d'erreur
  errorLoading: "Erreur lors du chargement",
  errorSaving: "Erreur lors de la sauvegarde",
  errorDeleting: "Erreur lors de la suppression",
  errorLogin: "Erreur de connexion",
  errorNetwork: "Erreur de réseau",
  errorPermission: "Permissions insuffisantes",
  
  // Formulaires
  required: "Champ obligatoire",
  invalidEmail: "Email invalide",
  passwordTooShort: "Mot de passe trop court",
  passwordMismatch: "Les mots de passe ne correspondent pas",
  
  // Confirmations
  confirmDelete: "Êtes-vous sûr de vouloir supprimer cet élément ?",
  confirmLogout: "Êtes-vous sûr de vouloir vous déconnecter ?",
  
  // Pagination
  page: "Page",
  of: "sur",
  itemsPerPage: "Éléments par page",
  
  // Dates
  today: "Aujourd'hui",
  yesterday: "Hier",
  tomorrow: "Demain",
  thisWeek: "Cette semaine",
  thisMonth: "Ce mois",
  
  // Statistiques
  total: "Total",
  average: "Moyenne",
  minimum: "Minimum",
  maximum: "Maximum",
  
  // Titres de pages
  adminDashboard: "Tableau de bord Administrateur",
  clientDashboard: "Tableau de bord Client",
  developerDashboard: "Tableau de bord Développeur",
  projectManagement: "Gestion des Projets",
  taskManagement: "Gestion des Tâches",
  userManagement: "Gestion des Utilisateurs",
  timeTracking: "Suivi du Temps",
  
  // Autres
  welcome: "Bienvenue",
  version: "Version",
  help: "Aide",
  settings: "Paramètres",
  about: "À propos",
  contact: "Contact",
  support: "Support"
};

// Fonction utilitaire pour récupérer une traduction
export const t = (key, defaultValue = key) => {
  return translations[key] || defaultValue;
};

// Fonction pour formater les messages avec paramètres
export const tf = (key, params = {}) => {
  let message = translations[key] || key;
  
  Object.keys(params).forEach(param => {
    message = message.replace(`{${param}}`, params[param]);
  });
  
  return message;
};
