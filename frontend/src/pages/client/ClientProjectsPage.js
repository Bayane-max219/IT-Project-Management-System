import React, { useState, useEffect } from 'react';
import { FolderIcon, ChartBarIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';
import projectService from '../../services/projectService';

const ClientProjectsPage = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedProject, setSelectedProject] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const projectsData = await projectService.getProjects();
      // S'assurer que projectsData est un tableau
      setProjects(Array.isArray(projectsData) ? projectsData : []);
    } catch (error) {
      console.error('Erreur lors du chargement des projets:', error);
      toast.error('Erreur lors du chargement des projets');
      setProjects([]); // Définir un tableau vide en cas d'erreur
    } finally {
      setLoading(false);
    }
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

  const getPriorityBadgeClass = (priority) => {
    switch (priority) {
      case 'low':
        return 'bg-gray-100 text-gray-800';
      case 'medium':
        return 'bg-warning-100 text-warning-800';
      case 'high':
        return 'bg-danger-100 text-danger-800';
      case 'urgent':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
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

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR');
  };

  const formatCurrency = (amount) => {
    if (!amount && amount !== 0) return 'Non défini';
    return `${parseFloat(amount).toLocaleString('fr-FR')} Ar`;
  };

  const handleProjectClick = (project) => {
    setSelectedProject(project);
    setShowDetails(true);
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
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Mes Projets</h1>
        <p className="mt-2 text-sm text-gray-700">
          Suivez l'avancement de tous vos projets en cours et terminés
        </p>
      </div>

      {/* Statistiques rapides */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <FolderIcon className="h-6 w-6 text-primary-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Projets Actifs</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {Array.isArray(projects) ? projects.filter(p => ['planning', 'in_progress', 'testing'].includes(p.status)).length : 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-6 w-6 text-success-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Projets Terminés</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {Array.isArray(projects) ? projects.filter(p => p.status === 'completed').length : 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CalendarIcon className="h-6 w-6 text-warning-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">En Retard</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {Array.isArray(projects) ? projects.filter(p => p.is_overdue).length : 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Liste des projets */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        {Array.isArray(projects) && projects.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {projects.map((project) => (
              <li key={project.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50 cursor-pointer" onClick={() => handleProjectClick(project)}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center min-w-0 flex-1">
                    <div className="flex-shrink-0">
                      <FolderIcon className="h-6 w-6 text-gray-400" />
                    </div>
                    <div className="ml-4 min-w-0 flex-1">
                      <div className="flex items-center justify-between">
                        <div className="text-lg font-medium text-gray-900 truncate">
                          {project.name}
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeClass(project.status)}`}>
                            {getStatusLabel(project.status)}
                          </span>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityBadgeClass(project.priority)}`}>
                            {getPriorityLabel(project.priority)}
                          </span>
                        </div>
                      </div>
                      <div className="mt-2 text-sm text-gray-600">
                        {project.description}
                      </div>
                      <div className="mt-3 flex items-center justify-between">
                        <div className="flex items-center space-x-6 text-sm text-gray-500">
                          <div>
                            <span className="font-medium">Début:</span> {formatDate(project.start_date)}
                          </div>
                          <div>
                            <span className="font-medium">Fin prévue:</span> {formatDate(project.end_date)}
                          </div>
                          {project.budget && (
                            <div>
                              <span className="font-medium">Budget:</span> {formatCurrency(project.budget)}
                            </div>
                          )}
                          {project.is_overdue && (
                            <div className="text-danger-600 font-medium">
                              En retard de {Math.abs(project.days_remaining)} jours
                            </div>
                          )}
                        </div>
                        <div className="flex items-center space-x-3">
                          <div className="flex items-center space-x-2">
                            <div className="w-32 bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${project.progress}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium text-gray-900 min-w-0">
                              {project.progress}%
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center py-12">
            <FolderIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">Aucun projet</h3>
            <p className="mt-1 text-sm text-gray-500">
              Vous n'avez aucun projet pour le moment.
            </p>
          </div>
        )}
      </div>

      {/* Modal de détails du projet */}
      {showDetails && selectedProject && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-medium text-gray-900">{selectedProject.name}</h3>
                  <div className="flex items-center space-x-2 mt-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeClass(selectedProject.status)}`}>
                      {getStatusLabel(selectedProject.status)}
                    </span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityBadgeClass(selectedProject.priority)}`}>
                      {getPriorityLabel(selectedProject.priority)}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => setShowDetails(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <span className="sr-only">Fermer</span>
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Informations générales */}
                <div className="space-y-4">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900 mb-3">Informations Générales</h4>
                    <div className="space-y-3">
                      <div>
                        <span className="text-sm font-medium text-gray-500">Description:</span>
                        <p className="text-sm text-gray-900 mt-1">{selectedProject.description}</p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-500">Chef de projet:</span>
                        <p className="text-sm text-gray-900">
                          {selectedProject.project_manager 
                            ? `${selectedProject.project_manager.first_name} ${selectedProject.project_manager.last_name}`
                            : 'Non assigné'
                          }
                        </p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-500">Budget:</span>
                        <p className="text-sm text-gray-900">
                          {selectedProject.budget ? formatCurrency(selectedProject.budget) : 'Non défini'}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Équipe */}
                  {selectedProject.team_members && selectedProject.team_members.length > 0 && (
                    <div>
                      <h4 className="text-lg font-medium text-gray-900 mb-3">Équipe</h4>
                      <div className="space-y-2">
                        {selectedProject.team_members.map((member, index) => (
                          <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                            <span className="text-sm text-gray-900">
                              {member.developer.first_name} {member.developer.last_name}
                            </span>
                            <span className="text-xs text-gray-500">{member.role_in_project}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Progression et dates */}
                <div className="space-y-4">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900 mb-3">Progression</h4>
                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-500">Avancement</span>
                          <span className="font-medium">{selectedProject.progress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                          <div
                            className="bg-primary-600 h-3 rounded-full transition-all duration-300"
                            style={{ width: `${selectedProject.progress}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-lg font-medium text-gray-900 mb-3">Dates</h4>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-500">Date de début:</span>
                        <span className="text-sm text-gray-900">{formatDate(selectedProject.start_date)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-500">Date de fin prévue:</span>
                        <span className="text-sm text-gray-900">{formatDate(selectedProject.end_date)}</span>
                      </div>
                      {selectedProject.actual_end_date && (
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-500">Date de fin réelle:</span>
                          <span className="text-sm text-gray-900">{formatDate(selectedProject.actual_end_date)}</span>
                        </div>
                      )}
                      {selectedProject.is_overdue && (
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-500">Retard:</span>
                          <span className="text-sm text-danger-600 font-medium">
                            {Math.abs(selectedProject.days_remaining)} jours
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-end pt-6">
                <button
                  onClick={() => setShowDetails(false)}
                  className="btn-primary"
                >
                  Fermer
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClientProjectsPage;
