import React, { useState, useEffect } from 'react';
import { 
  FolderIcon, 
  CheckIcon, 
  UsersIcon, 
  ClockIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
import projectService from '../../services/projectService';
import taskService from '../../services/taskService';
import pointageService from '../../services/pointageService';
import authService from '../../services/authService';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    projects: null,
    tasks: null,
    pointage: null,
    users: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [projectStats, taskStats, pointageStats, users] = await Promise.all([
          projectService.getProjectStats(),
          taskService.getTaskStats(),
          pointageService.getPointageStats(),
          authService.getUsers()
        ]);

        
        setStats({
          projects: projectStats,
          tasks: taskStats,
          pointage: pointageStats,
          users: users
        });
      } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const statsCards = [
    {
      name: 'Projets Actifs',
      value: stats.projects?.active_projects || 0,
      total: stats.projects?.total_projects || 0,
      icon: FolderIcon,
      color: 'bg-primary-500',
    },
    {
      name: 'Tâches En Cours',
      value: stats.tasks?.in_progress_tasks || 0,
      total: stats.tasks?.total_tasks || 0,
      icon: CheckIcon,
      color: 'bg-success-500',
    },
    {
      name: 'Employés Présents',
      value: stats.pointage?.present_today || 0,
      total: stats.pointage?.total_employees || 0,
      icon: UsersIcon,
      color: 'bg-warning-500',
    },
    {
      name: 'Retards Aujourd\'hui',
      value: stats.pointage?.late_today || 0,
      total: stats.pointage?.total_employees || 0,
      icon: ExclamationTriangleIcon,
      color: 'bg-danger-500',
    },
  ];

  // Traduction des statuts en français
  const statusTranslations = {
    'planning': 'Planification',
    'in_progress': 'En cours',
    'completed': 'Terminé',
    'on_hold': 'En pause',
    'cancelled': 'Annulé'
  };

  // Données pour le graphique des projets par statut
  const projectStatusData = {
    labels: Object.keys(stats.projects?.projects_by_status || {}).map(status => 
      statusTranslations[status] || status
    ),
    datasets: [
      {
        data: Object.values(stats.projects?.projects_by_status || {}),
        backgroundColor: [
          '#3B82F6', // blue
          '#10B981', // green
          '#F59E0B', // yellow
          '#EF4444', // red
          '#8B5CF6', // purple
        ],
      },
    ],
  };

  // Données pour le graphique des tâches par développeur
  const tasksByDeveloperData = {
    labels: Object.keys(stats.tasks?.tasks_by_developer || {}),
    datasets: [
      {
        label: 'Nombre de tâches',
        data: Object.values(stats.tasks?.tasks_by_developer || {}),
        backgroundColor: '#3B82F6',
      },
    ],
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Tableau de bord Administrateur</h1>
        <p className="mt-2 text-sm text-gray-700">
          Vue d'ensemble des projets, tâches et pointages
        </p>
      </div>

      {/* Cartes de statistiques */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statsCards.map((item) => (
          <div key={item.name} className="relative overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:px-6 sm:py-6">
            <div>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`${item.color} p-3 rounded-md`}>
                    <item.icon className="h-6 w-6 text-white" aria-hidden="true" />
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{item.name}</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{item.value}</div>
                      <div className="ml-2 text-sm text-gray-500">/ {item.total}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Graphiques */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        {/* Projets par statut */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Projets par Statut</h3>
            <div className="mt-5" style={{ height: '300px' }}>
              {stats.projects?.projects_by_status && Object.keys(stats.projects.projects_by_status).length > 0 ? (
                <Doughnut 
                  data={projectStatusData} 
                  options={{ 
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom'
                      }
                    }
                  }} 
                />
              ) : (
                <div className="flex items-center justify-center h-full text-gray-500">
                  Aucune donnée disponible
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tâches par développeur */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Tâches par Développeur</h3>
            <div className="mt-5" style={{ height: '300px' }}>
              {stats.tasks?.tasks_by_developer && Object.keys(stats.tasks.tasks_by_developer).length > 0 ? (
                <Bar 
                  data={tasksByDeveloperData} 
                  options={{ 
                    maintainAspectRatio: false,
                    scales: {
                      y: {
                        beginAtZero: true
                      }
                    }
                  }} 
                />
              ) : (
                <div className="flex items-center justify-center h-full text-gray-500">
                  Aucune donnée disponible
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Employés en retard aujourd'hui */}
      {stats.pointage?.late_employees && stats.pointage.late_employees.length > 0 && (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Employés en Retard Aujourd'hui</h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Liste des employés arrivés en retard aujourd'hui
            </p>
          </div>
          <ul className="divide-y divide-gray-200">
            {stats.pointage.late_employees.map((employee, index) => (
              <li key={index} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <ClockIcon className="h-5 w-5 text-danger-400" />
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">{employee.full_name}</div>
                      <div className="text-sm text-gray-500">
                        {(() => {
                          console.log(`🔍 Employee ${employee.full_name}:`, employee);
                          console.log(`🔍 late_reason:`, employee.late_reason, typeof employee.late_reason);
                          return employee.late_reason || 'Aucune raison fournie';
                        })()}
                      </div>
                    </div>
                  </div>
                  <div className="text-sm text-danger-600 font-medium">
                    +{employee.late_minutes} min
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Résumé rapide */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="p-5">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Résumé Rapide</h3>
          <div className="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div className="text-center">
              <div className="text-2xl font-semibold text-primary-600">
                {stats.projects?.overdue_projects || 0}
              </div>
              <div className="text-sm text-gray-500">Projets en Retard</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-semibold text-success-600">
                {stats.tasks?.completed_tasks || 0}
              </div>
              <div className="text-sm text-gray-500">Tâches Terminées</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-semibold text-warning-600">
                {stats.pointage?.attendance_rate || 0}%
              </div>
              <div className="text-sm text-gray-500">Taux de Présence</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
