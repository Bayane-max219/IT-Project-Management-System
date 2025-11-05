import React, { useState, useEffect } from 'react';
import { 
  ClockIcon, 
  UserIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon 
} from '@heroicons/react/24/outline';
import pointageService from '../../services/pointageService';

const PointageStatsPageNew = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      console.log('🔍 NOUVELLE PAGE: Chargement des données...');
      
      // Utiliser seulement getPointageStats() comme le Dashboard Admin
      const statsData = await pointageService.getPointageStats();

      console.log('🔍 NOUVELLE PAGE: Données reçues:', statsData);
      console.log('🔍 NOUVELLE PAGE: Type de statsData:', typeof statsData);
      console.log('🔍 NOUVELLE PAGE: Keys de statsData:', Object.keys(statsData || {}));
      console.log('🔍 NOUVELLE PAGE: total_employees:', statsData?.total_employees);
      console.log('🔍 NOUVELLE PAGE: present_today:', statsData?.present_today);
      console.log('🔍 NOUVELLE PAGE: late_today:', statsData?.late_today);
      
      setStats(statsData);
    } catch (error) {
      console.error('Erreur lors du chargement des statistiques:', error);
    } finally {
      setLoading(false);
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
      <div>
        <h1 className="text-2xl font-semibold text-gray-900" style={{backgroundColor: 'green', color: 'white', padding: '10px'}}>
          ✅ NOUVELLE PAGE STATISTIQUES POINTAGE - CORRIGÉE ✅
        </h1>
        <p className="mt-2 text-sm text-gray-700">
          Vue d'ensemble des pointages et de la présence des employés
        </p>
        <div className="bg-green-100 p-4 mt-4 rounded">
          <h3 className="font-bold text-green-800">DONNÉES REÇUES DE L'API:</h3>
          <p className="text-green-700">Total employés: {stats?.total_employees}</p>
          <p className="text-green-700">Présents aujourd'hui: {stats?.present_today}</p>
          <p className="text-green-700">En retard: {stats?.late_today}</p>
          <p className="text-green-700">Taux présence: {stats?.attendance_rate}%</p>
          <p className="text-green-700">Employés en retard: {stats?.late_employees?.length || 0}</p>
        </div>
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
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Employés</dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats?.total_employees || 0}
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
                <CheckCircleIcon className="h-6 w-6 text-green-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Présents Aujourd'hui</dt>
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
                <ExclamationTriangleIcon className="h-6 w-6 text-yellow-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">En Retard</dt>
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
                <ClockIcon className="h-6 w-6 text-blue-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Taux Présence</dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats?.attendance_rate || 0}%
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Employés en retard */}
      {stats?.late_employees && stats.late_employees.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Employés en Retard Aujourd'hui
            </h3>
            <div className="space-y-3">
              {stats.late_employees.map((employee, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{employee.full_name}</p>
                    <p className="text-sm text-red-600">{employee.late_reason || 'Aucune raison fournie'}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-red-600">+{employee.late_minutes} min</p>
                    <p className="text-xs text-gray-500">Arrivée: {employee.arrival_time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PointageStatsPageNew;
