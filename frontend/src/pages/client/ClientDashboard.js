import React, { useState, useEffect } from 'react';
import { 
  FolderIcon, 
  CheckIcon, 
  CalendarIcon,
  ChartBarIcon 
} from '@heroicons/react/24/outline';
import projectService from '../../services/projectService';
import taskService from '../../services/taskService';

const ClientDashboard = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      console.log('🔍 DEBUG MARIE DASHBOARD: Début fetchData');
      const projectsData = await projectService.getProjects();
      console.log('🔍 DEBUG MARIE DASHBOARD: Données reçues:', projectsData);
      console.log('🔍 DEBUG MARIE DASHBOARD: Type des données:', typeof projectsData);
      console.log('🔍 DEBUG MARIE DASHBOARD: Est un tableau?', Array.isArray(projectsData));
      console.log('🔍 DEBUG MARIE DASHBOARD: Longueur:', projectsData?.length);
      
      // S'assurer que projectsData est un tableau
      const finalProjects = Array.isArray(projectsData) ? projectsData : [];
      console.log('🔍 DEBUG MARIE DASHBOARD: Projets finaux:', finalProjects);
      setProjects(finalProjects);
    } catch (error) {
      console.error('🔍 DEBUG MARIE DASHBOARD: Erreur lors du chargement des projets:', error);
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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const activeProjects = Array.isArray(projects) ? projects.filter(p => ['planning', 'in_progress', 'testing'].includes(p.status)) : [];
  const completedProjects = Array.isArray(projects) ? projects.filter(p => p.status === 'completed') : [];
  const totalTasks = Array.isArray(projects) ? projects.reduce((sum, project) => sum + (project.tasks?.length || 0), 0) : 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Tableau de bord Client</h1>
        <p className="mt-2 text-sm text-gray-700">
          Suivez l'avancement de vos projets en temps réel
        </p>
      </div>

      {/* Statistiques rapides */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <FolderIcon className="h-6 w-6 text-primary-400" aria-hidden="true" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Projets Actifs</dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900">{activeProjects.length}</div>
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
                <CheckIcon className="h-6 w-6 text-success-400" aria-hidden="true" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Projets Terminés</dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900">{completedProjects.length}</div>
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
                <ChartBarIcon className="h-6 w-6 text-warning-400" aria-hidden="true" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Progression Moyenne</dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900">
                      {projects.length > 0 
                        ? Math.round(projects.reduce((sum, p) => sum + p.progress, 0) / projects.length)
                        : 0}%
                    </div>
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
                <CalendarIcon className="h-6 w-6 text-danger-400" aria-hidden="true" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Projets en Retard</dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900">
                      {Array.isArray(projects) ? projects.filter(p => p.is_overdue).length : 0}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Liste des projets */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
          <div>
            <h3 className="text-lg leading-6 font-medium text-gray-900">Mes Projets</h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Suivi de l'avancement de vos projets
            </p>
          </div>
          <a
            href="/client/projects"
            className="text-primary-600 hover:text-primary-500 text-sm font-medium"
          >
            Voir tous →
          </a>
        </div>
        
        {projects.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {projects.slice(0, 5).map((project) => (
              <li key={project.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center min-w-0 flex-1">
                    <div className="flex-shrink-0">
                      <FolderIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <div className="ml-4 min-w-0 flex-1">
                      <div className="text-sm font-medium text-gray-900 truncate">
                        {project.name}
                      </div>
                      <div className="text-sm text-gray-500 truncate">
                        {project.description}
                      </div>
                      <div className="flex items-center mt-2 space-x-4">
                        <div className="text-xs text-gray-400">
                          Début: {new Date(project.start_date).toLocaleDateString('fr-FR')}
                        </div>
                        <div className="text-xs text-gray-400">
                          Fin prévue: {new Date(project.end_date).toLocaleDateString('fr-FR')}
                        </div>
                        {project.is_overdue && (
                          <div className="text-xs text-danger-600 font-medium">
                            En retard
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    {/* Barre de progression */}
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full"
                          style={{ width: `${project.progress}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-500 min-w-0">
                        {project.progress}%
                      </span>
                    </div>
                    
                    {/* Badges */}
                    <div className="flex flex-col space-y-1">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeClass(project.status)}`}>
                        {getStatusLabel(project.status)}
                      </span>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityBadgeClass(project.priority)}`}>
                        {getPriorityLabel(project.priority)}
                      </span>
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
              Vous n'avez aucun projet en cours pour le moment.
            </p>
          </div>
        )}
      </div>

      {/* Projets récemment terminés */}
      {completedProjects.length > 0 && (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Projets Récemment Terminés</h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Vos projets terminés avec succès
            </p>
          </div>
          <ul className="divide-y divide-gray-200">
            {completedProjects.slice(0, 3).map((project) => (
              <li key={project.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <CheckIcon className="h-5 w-5 text-success-400" />
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">
                        {project.name}
                      </div>
                      <div className="text-sm text-gray-500">
                        Terminé le {project.actual_end_date 
                          ? new Date(project.actual_end_date).toLocaleDateString('fr-FR')
                          : new Date(project.end_date).toLocaleDateString('fr-FR')
                        }
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-success-100 text-success-800">
                      Terminé
                    </span>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ClientDashboard;
