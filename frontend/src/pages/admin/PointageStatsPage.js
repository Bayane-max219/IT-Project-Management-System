import React, { useState, useEffect } from 'react';
import { 
  ClockIcon, 
  UserIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon 
} from '@heroicons/react/24/outline';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import pointageService from '../../services/pointageService';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const PointageStatsPage = () => {
  const [stats, setStats] = useState(null);
  const [pointages, setPointages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      console.log('🔍 POINTAGE STATS PAGE: Chargement des données...');
      
      // UTILISER LA MÊME LOGIQUE QUE LE DASHBOARD ADMIN
      const pointageStats = await pointageService.getPointageStats();

      console.log('🔍 POINTAGE STATS PAGE: Données reçues:', pointageStats);
      
      setStats(pointageStats);
      setPointages(pointageStats?.late_employees || []);
    } catch (error) {
      console.error('Erreur lors du chargement des statistiques:', error);
      setPointages([]);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (timeString) => {
    if (!timeString) return '--:--';
    return timeString.substring(0, 5);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR');
  };

  // Données pour le graphique des heures travaillées par jour
  const getWorkHoursChartData = () => {
    const last7Days = [];
    const today = new Date();
    
    for (let i = 6; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      last7Days.push(date.toISOString().split('T')[0]);
    }

    const workHoursByDay = last7Days.map(date => {
      const dayPointages = Array.isArray(pointages) ? pointages.filter(p => p.date === date) : [];
      return dayPointages.reduce((total, p) => total + (p.total_work_hours || 0), 0);
    });

    return {
      labels: last7Days.map(date => new Date(date).toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric' })),
      datasets: [
        {
          label: 'Heures travaillées',
          data: workHoursByDay,
          backgroundColor: '#3B82F6',
          borderColor: '#2563EB',
          borderWidth: 1,
        },
      ],
    };
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
        <h1 className="text-2xl font-semibold text-gray-900">Statistiques de Pointage</h1>
        <p className="mt-2 text-sm text-gray-700">
          Vue d'ensemble des pointages et de la présence des employés
        </p>
      </div>

      {/* Statistiques du jour */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <UserIcon className="h-6 w-6 text-primary-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Employés Présents</dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-gray-900">
                      {stats?.present_today || 0}
                    </div>
                    <div className="ml-2 text-sm text-gray-500">
                      / {stats?.total_employees || 0}
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
                <ExclamationTriangleIcon className="h-6 w-6 text-warning-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Retards Aujourd'hui</dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats?.late_today || 0}
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
                <ClockIcon className="h-6 w-6 text-success-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Heures Travaillées</dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats?.total_work_hours_today || 0}h
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
                <CheckCircleIcon className="h-6 w-6 text-primary-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Taux de Présence</dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats?.attendance_rate || 0}%
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Graphique des heures travaillées */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="p-5">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Heures Travaillées - 7 Derniers Jours
          </h3>
          <div style={{ height: '300px' }}>
            {Array.isArray(pointages) ? (
              <Bar 
                data={getWorkHoursChartData()} 
                options={{ 
                maintainAspectRatio: false,
                scales: {
                  y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: 'Heures'
                    }
                  }
                },
                plugins: {
                  legend: {
                    display: false
                  }
                }
              }} 
            />
            ) : (
              <div className="flex items-center justify-center h-full">
                <p className="text-gray-500">Chargement du graphique...</p>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Employés en retard aujourd'hui */}
        {stats?.late_employees_today && stats.late_employees_today.length > 0 && (
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Employés en Retard Aujourd'hui
              </h3>
              <p className="mt-1 max-w-2xl text-sm text-gray-500">
                Liste des employés arrivés en retard
              </p>
            </div>
            <ul className="divide-y divide-gray-200">
              {(stats?.late_employees || []).map((employee, index) => (
                <li key={index} className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <ExclamationTriangleIcon className="h-5 w-5 text-warning-400" />
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">
                          {employee.full_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {employee.late_reason || 'Aucune raison fournie'}
                        </div>
                      </div>
                    </div>
                    <div className="text-sm text-warning-600 font-medium">
                      +{employee.late_minutes} min
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Informations générales */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Informations Générales
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Heure d'arrivée moyenne:</span>
                <span className="text-sm font-medium text-gray-900">
                  {stats?.average_arrival_time || 'N/A'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Total employés:</span>
                <span className="text-sm font-medium text-gray-900">
                  {stats?.total_employees || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Absents aujourd'hui:</span>
                <span className="text-sm font-medium text-gray-900">
                  {stats?.absent_today || 0}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Historique des pointages récents */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Pointages Récents
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Les 20 derniers pointages enregistrés
          </p>
        </div>
        
        {Array.isArray(pointages) && pointages.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {pointages.slice(0, 20).map((pointage) => (
              <li key={pointage.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <ClockIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">
                        {pointage.employee?.first_name || 'N/A'} {pointage.employee?.last_name || ''}
                      </div>
                      <div className="text-sm text-gray-500">
                        {formatDate(pointage.date)} - 
                        Arrivée: {formatTime(pointage.arrival_time)} - 
                        Départ: {formatTime(pointage.departure_time)}
                      </div>
                      {pointage.late_reason && (
                        <div className="text-xs text-warning-600 mt-1">
                          Retard ({pointage.late_minutes} min): {pointage.late_reason}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">
                        {pointage.total_work_hours ? `${pointage.total_work_hours.toFixed(2)}h` : 'N/A'}
                      </div>
                      <div className="text-xs text-gray-500">Temps travaillé</div>
                    </div>
                    {pointage.is_late && (
                      <div className="flex-shrink-0">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-warning-100 text-warning-800">
                          En retard
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center py-12">
            <ClockIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">Aucun pointage</h3>
            <p className="mt-1 text-sm text-gray-500">
              Les pointages apparaîtront ici une fois enregistrés.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PointageStatsPage;
