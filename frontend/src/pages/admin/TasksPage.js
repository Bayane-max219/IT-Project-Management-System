import React, { useState, useEffect } from 'react';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';
import taskService from '../../services/taskService';
import projectService from '../../services/projectService';
import authService from '../../services/authService';

const TasksPage = () => {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [developers, setDevelopers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    project: '',
    assigned_to: '',
    status: 'todo',
    priority: 'medium',
    estimated_hours: '',
    start_date: '',
    due_date: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [tasksData, projectsData, usersData] = await Promise.all([
        taskService.getTasks(),
        projectService.getProjects(),
        authService.getUsers()
      ]);

      // Gérer le format des tâches
      let tasksList = [];
      if (Array.isArray(tasksData)) {
        tasksList = tasksData;
      } else if (tasksData && Array.isArray(tasksData.results)) {
        tasksList = tasksData.results;
      }
      setTasks(tasksList);

      // Gérer le format des projets
      let projectsList = [];
      if (Array.isArray(projectsData)) {
        projectsList = projectsData;
      } else if (projectsData && Array.isArray(projectsData.results)) {
        projectsList = projectsData.results;
      }
      setProjects(projectsList);

      // Gérer le format des utilisateurs
      let usersList = [];
      if (Array.isArray(usersData)) {
        usersList = usersData;
      } else if (usersData && Array.isArray(usersData.results)) {
        usersList = usersData.results;
      } else if (usersData && typeof usersData === 'object') {
        usersList = Object.values(usersData);
      }

      console.log('Données pour tâches - Projets:', projectsList, 'Développeurs:', usersList.filter(u => u.role === 'developer')); // Debug
      setDevelopers(usersList.filter(user => user.role === 'developer'));
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
      if (editingTask) {
        await taskService.updateTask(editingTask.id, formData);
        toast.success('Tâche modifiée avec succès !');
      } else {
        await taskService.createTask(formData);
        toast.success('Tâche créée avec succès !');
      }
      
      setShowModal(false);
      setEditingTask(null);
      resetForm();
      fetchData();
    } catch (error) {
      console.error('🔍 TÂCHE: Erreur complète:', error);
      console.error('🔍 TÂCHE: Erreur response:', error.response);
      console.error('🔍 TÂCHE: Erreur data:', error.response?.data);
      console.error('🔍 TÂCHE: Status:', error.response?.status);
      console.error('🔍 TÂCHE: Données envoyées:', formData);
      
      // Log détaillé de l'erreur data
      if (error.response?.data) {
        console.error('🔍 TÂCHE: Détails erreur:');
        Object.keys(error.response.data).forEach(key => {
          console.error(`   ${key}:`, error.response.data[key]);
        });
      }
      
      // Afficher l'erreur spécifique
      let errorMessage = error.response?.data?.message || 
                        error.response?.data?.error || 
                        error.message || 
                        'Erreur lors de la sauvegarde';
      
      // Messages plus clairs pour les erreurs courantes
      if (error.response?.data) {
        const errorData = error.response.data;
        const errors = [];
        
        Object.keys(errorData).forEach(field => {
          const fieldErrors = errorData[field];
          if (Array.isArray(fieldErrors)) {
            fieldErrors.forEach(err => {
              if (field === 'project' && err.includes('required')) {
                errors.push('Le projet est obligatoire');
              } else if (field === 'title' && err.includes('required')) {
                errors.push('Le titre est obligatoire');
              } else if (field === 'assigned_to' && err.includes('invalid')) {
                errors.push('Développeur sélectionné invalide');
              } else {
                errors.push(`${field}: ${err}`);
              }
            });
          }
        });
        
        if (errors.length > 0) {
          errorMessage = errors.join(', ');
        }
      }
      
      toast.error(errorMessage);
    }
  };

  const handleEdit = (task) => {
    setEditingTask(task);
    setFormData({
      title: task.title,
      description: task.description,
      project: task.project.id,
      assigned_to: task.assigned_to?.id || '',
      status: task.status,
      priority: task.priority,
      estimated_hours: task.estimated_hours || '',
      start_date: task.start_date || '',
      due_date: task.due_date || '',
    });
    setShowModal(true);
  };

  const handleDelete = async (taskId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) {
      try {
        await taskService.deleteTask(taskId);
        toast.success('Tâche supprimée avec succès !');
        fetchData();
      } catch (error) {
        console.error('Erreur:', error);
        toast.error('Erreur lors de la suppression');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      project: '',
      assigned_to: '',
      status: 'todo',
      priority: 'medium',
      estimated_hours: '',
      start_date: '',
      due_date: '',
    });
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'todo':
        return 'status-badge status-todo';
      case 'in_progress':
        return 'status-badge status-in-progress';
      case 'completed':
        return 'status-badge status-completed';
      case 'blocked':
        return 'status-badge status-blocked';
      case 'testing':
        return 'status-badge bg-warning-100 text-warning-800';
      default:
        return 'status-badge status-todo';
    }
  };

  const getPriorityBadgeClass = (priority) => {
    switch (priority) {
      case 'low':
        return 'priority-low';
      case 'medium':
        return 'priority-medium';
      case 'high':
        return 'priority-high';
      case 'urgent':
        return 'priority-urgent';
      default:
        return 'priority-medium';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'todo':
        return 'À faire';
      case 'in_progress':
        return 'En cours';
      case 'testing':
        return 'En test';
      case 'completed':
        return 'Terminé';
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
          <h1 className="text-2xl font-semibold text-gray-900">Gestion des Tâches</h1>
          <p className="mt-2 text-sm text-gray-700">
            Gérez toutes les tâches de l'entreprise
          </p>
        </div>
        <button
          onClick={() => {
            resetForm();
            setEditingTask(null);
            setShowModal(true);
          }}
          className="btn-primary flex items-center"
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          Nouvelle Tâche
        </button>
      </div>

      {/* Liste des tâches */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        {tasks.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {tasks.map((task) => (
              <li key={task.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center min-w-0 flex-1">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center justify-between">
                        <div className="text-sm font-medium text-gray-900 truncate">
                          {task.title}
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={getStatusBadgeClass(task.status)}>
                            {getStatusLabel(task.status)}
                          </span>
                          <span className={`status-badge ${getPriorityBadgeClass(task.priority)}`}>
                            {getPriorityLabel(task.priority)}
                          </span>
                        </div>
                      </div>
                      <div className="mt-2 flex items-center text-sm text-gray-500">
                        <div className="flex-shrink-0">
                          Projet: {task.project.name}
                        </div>
                        {task.assigned_to && (
                          <div className="ml-4">
                            Assigné à: {task.assigned_to.first_name} {task.assigned_to.last_name}
                          </div>
                        )}
                        {task.due_date && (
                          <div className="ml-4">
                            Échéance: {new Date(task.due_date).toLocaleDateString('fr-FR')}
                          </div>
                        )}
                        {task.estimated_hours && (
                          <div className="ml-4">
                            Estimé: {task.estimated_hours}h
                          </div>
                        )}
                      </div>
                      <div className="mt-2 text-sm text-gray-600">
                        {task.description}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <button
                      onClick={() => handleEdit(task)}
                      className="text-primary-600 hover:text-primary-500"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(task.id)}
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
            <h3 className="mt-2 text-sm font-medium text-gray-900">Aucune tâche</h3>
            <p className="mt-1 text-sm text-gray-500">
              Commencez par créer une nouvelle tâche.
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
                {editingTask ? 'Modifier la Tâche' : 'Nouvelle Tâche'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Titre</label>
                  <input
                    type="text"
                    required
                    className="input-field"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
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
                  <label className="block text-sm font-medium text-gray-700">Projet</label>
                  <select
                    required
                    className="input-field"
                    value={formData.project}
                    onChange={(e) => setFormData({...formData, project: e.target.value})}
                  >
                    <option value="">Sélectionner un projet</option>
                    {projects.map(project => (
                      <option key={project.id} value={project.id}>
                        {project.name}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Assigné à</label>
                  <select
                    className="input-field"
                    value={formData.assigned_to}
                    onChange={(e) => setFormData({...formData, assigned_to: e.target.value})}
                  >
                    <option value="">Sélectionner un développeur</option>
                    {developers.map(dev => (
                      <option key={dev.id} value={dev.id}>
                        {dev.first_name} {dev.last_name}
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
                      <option value="todo">À faire</option>
                      <option value="in_progress">En cours</option>
                      <option value="testing">En test</option>
                      <option value="completed">Terminé</option>
                      <option value="blocked">Bloqué</option>
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
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Heures estimées</label>
                  <input
                    type="number"
                    step="0.5"
                    className="input-field"
                    value={formData.estimated_hours}
                    onChange={(e) => setFormData({...formData, estimated_hours: e.target.value})}
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Date de début</label>
                    <input
                      type="date"
                      className="input-field"
                      value={formData.start_date}
                      onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Date limite</label>
                    <input
                      type="date"
                      className="input-field"
                      value={formData.due_date}
                      onChange={(e) => setFormData({...formData, due_date: e.target.value})}
                    />
                  </div>
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
                    {editingTask ? 'Modifier' : 'Créer'}
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

export default TasksPage;
