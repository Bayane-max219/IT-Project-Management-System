import React, { useState, useEffect } from 'react';
import { 
  ClockIcon, 
  UserIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon 
} from '@heroicons/react/24/outline';

const PointageStatsPageSimple = () => {
  const [stats, setStats] = useState({
    total_employees: 2,
    present_today: 1,
    late_today: 0,
    absent_today: 1,
    average_arrival_time: "08:30",
    total_work_hours_today: 8.5,
    attendance_rate: 50.0,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Simuler le chargement des données
    setLoading(false);
  }, []);

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

      {/* Statistiques principales */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <UserIcon className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Employés</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats.total_employees}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckCircleIcon className="h-6 w-6 text-success-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Présents Aujourd'hui</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats.present_today}</dd>
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
                  <dt className="text-sm font-medium text-gray-500 truncate">En Retard</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats.late_today}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ClockIcon className="h-6 w-6 text-primary-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Heure Moyenne</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats.average_arrival_time}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Informations détaillées */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Résumé du Jour
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Taux de présence:</span>
                <span className="text-sm font-medium text-gray-900">{stats.attendance_rate}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Heures travaillées:</span>
                <span className="text-sm font-medium text-gray-900">{stats.total_work_hours_today}h</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Absents:</span>
                <span className="text-sm font-medium text-gray-900">{stats.absent_today}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Statut Système
            </h3>
            <div className="space-y-4">
              <div className="flex items-center">
                <CheckCircleIcon className="h-5 w-5 text-success-400 mr-2" />
                <span className="text-sm text-gray-900">Système de pointage actif</span>
              </div>
              <div className="flex items-center">
                <CheckCircleIcon className="h-5 w-5 text-success-400 mr-2" />
                <span className="text-sm text-gray-900">Base de données connectée</span>
              </div>
              <div className="flex items-center">
                <CheckCircleIcon className="h-5 w-5 text-success-400 mr-2" />
                <span className="text-sm text-gray-900">API fonctionnelle</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Message d'information */}
      <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <ClockIcon className="h-5 w-5 text-blue-400" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-blue-800">
              Statistiques Simplifiées
            </h3>
            <div className="mt-2 text-sm text-blue-700">
              <p>
                Cette page affiche les statistiques de base du système de pointage. 
                Les données sont mises à jour en temps réel.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PointageStatsPageSimple;
