import React, { useState, useEffect } from 'react';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';
import projectService from '../../services/projectService';
import authService from '../../services/authService';

const ProjectsPage = () => {
  const [projects, setProjects] = useState([]);
  const [clients, setClients] = useState([]);
  const [projectManagers, setProjectManagers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    client: '',
    project_manager: '',
    status: 'planning',
    priority: 'medium',
    start_date: '',
    end_date: '',
    budget: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [projectsData, usersData] = await Promise.all([
        projectService.getProjects(),
        authService.getUsers()
      ]);

      // Gérer le format des projets
      let projectsList = [];
      if (Array.isArray(projectsData)) {
        projectsList = projectsData;
      } else if (projectsData && Array.isArray(projectsData.results)) {
        projectsList = projectsData.results;
      }
      setProjects(projectsList);

      // Gérer le format des utilisateurs (même logique que UsersPage)
      let usersList = [];
      if (Array.isArray(usersData)) {
        usersList = usersData;
      } else if (usersData && Array.isArray(usersData.results)) {
        // Format paginé Django REST Framework
        usersList = usersData.results;
      } else if (usersData && typeof usersData === 'object') {
        // Autre format d'objet
        usersList = Object.values(usersData);
      }

      console.log('Utilisateurs récupérés pour projets:', usersList); // Debug
      setClients(usersList.filter(user => user.role === 'client'));
      // Les chefs de projet peuvent être des admins ou des développeurs
      setProjectManagers(usersList.filter(user => user.role === 'developer' || user.role === 'admin'));
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
      toast.error('Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Préparer les données avec les bons noms de champs pour le backend
      const dataToSend = {
        ...formData,
        client_id: formData.client,
        project_manager_id: formData.project_manager || null,
      };
      
      // Supprimer les anciens champs
      delete dataToSend.client;
      delete dataToSend.project_manager;
      
      console.log('🔍 Données à envoyer au backend:', dataToSend);
      
      if (editingProject) {
        await projectService.updateProject(editingProject.id, dataToSend);
        toast.success('Projet modifié avec succès !');
      } else {
        await projectService.createProject(dataToSend);
        toast.success('Projet créé avec succès !');
      }
      
      setShowModal(false);
      setEditingProject(null);
      resetForm();
      fetchData();
    } catch (error) {
      console.error('🔍 Erreur complète:', error);
      console.error('🔍 Erreur response:', error.response);
      console.error('🔍 Erreur data:', error.response?.data);
      console.error('🔍 Erreur status:', error.response?.status);
      console.error('🔍 Données envoyées:', formData);
      
      const errorMessage = error.response?.data?.error || 
                          error.response?.data?.message || 
                          error.message || 
                          'Erreur lors de la sauvegarde';
      
      toast.error(`Erreur: ${errorMessage}`);
    }
  };

  const handleEdit = (project) => {
    setEditingProject(project);
    setFormData({
      name: project.name,
      description: project.description,
      client: project.client.id,
      project_manager: project.project_manager?.id || '',
      status: project.status,
      priority: project.priority,
      start_date: project.start_date,
      end_date: project.end_date,
      budget: project.budget || '',
    });
    setShowModal(true);
  };

  const handleDelete = async (projectId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce projet ?')) {
      try {
        await projectService.deleteProject(projectId);
        toast.success('Projet supprimé avec succès !');
        fetchData();
      } catch (error) {
        console.error('Erreur:', error);
        toast.error('Erreur lors de la suppression');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      client: '',
      project_manager: '',
      status: 'planning',
      priority: 'medium',
      start_date: '',
      end_date: '',
      budget: '',
    });
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'planning':
        return 'bg-gray-100 text-gray-800';
      case 'in_progress':
        return 'bg-primary-100 text-primary-800';
      case 'testing':
        return 'bg-warning-100 text-warning-800';
      case 'completed':
        return 'bg-success-100 text-success-800';
      case 'on_hold':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-danger-100 text-danger-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'planning':
        return 'Planification';
      case 'in_progress':
        return 'En cours';
      case 'testing':
        return 'Tests';
      case 'completed':
        return 'Terminé';
      case 'on_hold':
        return 'En pause';
      case 'cancelled':
        return 'Annulé';
      default:
        return status;
    }
  };

  const getPriorityLabel = (priority) => {
    switch (priority) {
      case 'low':
        return 'Basse';
      case 'medium':
        return 'Moyenne';
      case 'high':
        return 'Haute';
      case 'urgent':
        return 'Urgente';
      default:
        return priority;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Gestion des Projets</h1>
          <p className="mt-2 text-sm text-gray-700">
            Gérez tous les projets de l'entreprise
          </p>
        </div>
        <button
          onClick={() => {
            resetForm();
            setEditingProject(null);
            setShowModal(true);
          }}
          className="btn-primary flex items-center"
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          Nouveau Projet
        </button>
      </div>

      {/* Liste des projets */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        {projects.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {projects.map((project) => (
              <li key={project.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center min-w-0 flex-1">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center justify-between">
                        <div className="text-sm font-medium text-gray-900 truncate">
                          {project.name}
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeClass(project.status)}`}>
                            {getStatusLabel(project.status)}
                          </span>
                          <div className="flex items-center space-x-2">
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-primary-600 h-2 rounded-full"
                                style={{ width: `${project.progress}%` }}
                              ></div>
                            </div>
                            <span className="text-sm text-gray-500">
                              {project.progress}%
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="mt-2 flex items-center text-sm text-gray-500">
                        <div className="flex-shrink-0">
                          Client: {project.client.first_name} {project.client.last_name}
                        </div>
                        {project.project_manager && (
                          <div className="ml-4">
                            Chef: {project.project_manager.first_name} {project.project_manager.last_name}
                          </div>
                        )}
                        <div className="ml-4">
                          {new Date(project.start_date).toLocaleDateString('fr-FR')} - {new Date(project.end_date).toLocaleDateString('fr-FR')}
                        </div>
                        {project.budget && (
                          <div className="ml-4">
                            Budget: {parseFloat(project.budget).toLocaleString('fr-FR')} Ar
                          </div>
                        )}
                      </div>
                      <div className="mt-2 text-sm text-gray-600">
                        {project.description}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <button
                      onClick={() => handleEdit(project)}
                      className="text-primary-600 hover:text-primary-500"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(project.id)}
                      className="text-danger-600 hover:text-danger-500"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center py-12">
            <h3 className="mt-2 text-sm font-medium text-gray-900">Aucun projet</h3>
            <p className="mt-1 text-sm text-gray-500">
              Commencez par créer un nouveau projet.
            </p>
          </div>
        )}
      </div>

      {/* Modal de création/édition */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingProject ? 'Modifier le Projet' : 'Nouveau Projet'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Nom</label>
                  <input
                    type="text"
                    required
                    className="input-field"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Description</label>
                  <textarea
                    required
                    rows={3}
                    className="input-field"
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Client</label>
                  <select
                    required
                    className="input-field"
                    value={formData.client}
                    onChange={(e) => setFormData({...formData, client: e.target.value})}
                  >
                    <option value="">Sélectionner un client</option>
                    {clients.map(client => (
                      <option key={client.id} value={client.id}>
                        {client.first_name} {client.last_name}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Chef de projet</label>
                  <select
                    className="input-field"
                    value={formData.project_manager}
                    onChange={(e) => setFormData({...formData, project_manager: e.target.value})}
                  >
                    <option value="">Sélectionner un chef de projet</option>
                    {projectManagers.map(manager => (
                      <option key={manager.id} value={manager.id}>
                        {manager.first_name} {manager.last_name} ({manager.role === 'admin' ? 'Admin' : 'Développeur'})
                      </option>
                    ))}
                  </select>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Statut</label>
                    <select
                      className="input-field"
                      value={formData.status}
                      onChange={(e) => setFormData({...formData, status: e.target.value})}
                    >
                      <option value="planning">Planification</option>
                      <option value="in_progress">En cours</option>
                      <option value="testing">Tests</option>
                      <option value="completed">Terminé</option>
                      <option value="on_hold">En pause</option>
                      <option value="cancelled">Annulé</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Priorité</label>
                    <select
                      className="input-field"
                      value={formData.priority}
                      onChange={(e) => setFormData({...formData, priority: e.target.value})}
                    >
                      <option value="low">Basse</option>
                      <option value="medium">Moyenne</option>
                      <option value="high">Haute</option>
                      <option value="urgent">Urgente</option>
                    </select>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Date de début</label>
                    <input
                      type="date"
                      required
                      className="input-field"
                      value={formData.start_date}
                      onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Date de fin</label>
                    <input
                      type="date"
                      required
                      className="input-field"
                      value={formData.end_date}
                      onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Budget (Ar)</label>
                  <input
                    type="number"
                    step="0.01"
                    className="input-field"
                    value={formData.budget}
                    onChange={(e) => setFormData({...formData, budget: e.target.value})}
                  />
                </div>
                
                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="btn-secondary"
                  >
                    Annuler
                  </button>
                  <button type="submit" className="btn-primary">
                    {editingProject ? 'Modifier' : 'Créer'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProjectsPage;
