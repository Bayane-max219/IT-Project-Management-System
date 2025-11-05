import React, { useState, useEffect } from 'react';
import { 
  ClockIcon, 
  CalendarIcon, 
  PlayIcon, 
  PauseIcon, 
  StopIcon 
} from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';
import pointageService from '../../services/pointageService';

const PointagePage = () => {
  const [pointages, setPointages] = useState([]);
  const [todayPointage, setTodayPointage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pointageLoading, setPointageLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [pointagesData, todayData] = await Promise.all([
        pointageService.getMyPointages(),
        pointageService.getTodayPointage().catch(() => null)
      ]);

      setPointages(pointagesData);
      setTodayPointage(todayData);
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
      toast.error('Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  const handlePointageAction = async (action) => {
    setPointageLoading(true);
    try {
      let result;
      switch (action) {
        case 'clock-in':
          result = await pointageService.clockIn();
          toast.success('Arrivée enregistrée !');
          break;
        case 'break-start':
          result = await pointageService.breakStart();
          toast.success('Début de pause enregistré !');
          break;
        case 'break-end':
          result = await pointageService.breakEnd();
          toast.success('Fin de pause enregistrée !');
          break;
        case 'clock-out':
          result = await pointageService.clockOut();
          toast.success('Départ enregistré !');
          break;
        default:
          break;
      }
      setTodayPointage(result);
      
      // Recharger les données avec un délai pour s'assurer de la synchronisation
      console.log('🔄 Rechargement des données après pointage...');
      setTimeout(async () => {
        try {
          console.log('🔄 Récupération des nouvelles données...');
          const [pointagesData, todayData] = await Promise.all([
            pointageService.getMyPointages(),
            pointageService.getTodayPointage().catch(() => null)
          ]);
          
          console.log('✅ Nouvelles données reçues:', { pointagesData, todayData });
          setPointages(pointagesData);
          setTodayPointage(todayData);
          
          console.log('✅ Interface mise à jour');
        } catch (error) {
          console.error('❌ Erreur lors du rechargement:', error);
          // Fallback: recharger toutes les données
          fetchData();
        }
      }, 1000); // Augmenter le délai à 1 seconde
    } catch (error) {
      console.error('Erreur pointage:', error);
      console.error('Détails erreur:', error.response?.data);
      
      const errorData = error.response?.data;
      
      // Si justification requise
      if (errorData?.requires_justification) {
        console.log('🔍 FRONTEND: Justification requise');
        console.log('🔍 Message:', errorData.message);
        
        const reason = prompt(errorData.message || 'Veuillez fournir une raison');
        console.log('🔍 Raison saisie:', reason);
        
        if (reason) {
          // Réessayer avec la raison
          console.log('🔍 Envoi de la justification:', reason);
          try {
            let result;
            const dataWithReason = { reason: reason };
            console.log('🔍 Données à envoyer:', dataWithReason);
            
            switch (action) {
              case 'clock-in':
                result = await pointageService.clockIn(dataWithReason);
                break;
              case 'break-start':
                result = await pointageService.breakStart(dataWithReason);
                break;
              case 'break-end':
                result = await pointageService.breakEnd(dataWithReason);
                break;
              case 'clock-out':
                result = await pointageService.clockOut(dataWithReason);
                break;
              default:
                break;
            }
            setTodayPointage(result);
            toast.success('Pointage enregistré avec justification !');
            
            // Recharger les données avec un délai
            console.log('🔄 Rechargement après justification...');
            setTimeout(async () => {
              try {
                console.log('🔄 Récupération des nouvelles données après justification...');
                const [pointagesData, todayData] = await Promise.all([
                  pointageService.getMyPointages(),
                  pointageService.getTodayPointage().catch(() => null)
                ]);
                
                console.log('✅ Nouvelles données reçues:', { pointagesData, todayData });
                setPointages(pointagesData);
                setTodayPointage(todayData);
                
                console.log('✅ Interface mise à jour après justification');
              } catch (error) {
                console.error('❌ Erreur lors du rechargement après justification:', error);
                fetchData();
              }
            }, 1000);
          } catch (retryError) {
            console.error('Erreur lors du retry:', retryError);
            toast.error(retryError.response?.data?.error || 'Erreur lors du pointage');
          }
        } else {
          console.log('❌ FRONTEND: Justification annulée par l\'utilisateur');
          toast.error('Justification requise pour pointer en retard');
        }
      } else {
        toast.error(errorData?.error || errorData?.message || 'Erreur lors du pointage');
      }
    } finally {
      setPointageLoading(false);
    }
  };

  const formatTime = (timeString) => {
    if (!timeString) return '--:--';
    return timeString.substring(0, 5); // HH:MM
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
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
        <h1 className="text-2xl font-semibold text-gray-900">Pointage</h1>
        <p className="mt-2 text-sm text-gray-700">
          Gérez votre pointage quotidien et consultez votre historique
        </p>
      </div>

      {/* Section Pointage du jour */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Pointage du jour - {formatDate(new Date())}
          </h3>
          
          {todayPointage ? (
            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <ClockIcon className="mx-auto h-8 w-8 text-success-400 mb-2" />
                <div className="text-sm text-gray-500">Arrivée</div>
                <div className="text-2xl font-semibold text-gray-900">
                  {formatTime(todayPointage.arrival_time)}
                </div>
                {todayPointage.is_late && (
                  <div className="text-sm text-danger-600 mt-1">
                    Retard: {todayPointage.late_minutes} min
                  </div>
                )}
              </div>

              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <StopIcon className="mx-auto h-8 w-8 text-danger-400 mb-2" />
                <div className="text-sm text-gray-500">Départ</div>
                <div className="text-2xl font-semibold text-gray-900">
                  {formatTime(todayPointage.departure_time)}
                </div>
              </div>

              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <PauseIcon className="mx-auto h-8 w-8 text-warning-400 mb-2" />
                <div className="text-sm text-gray-500">Début Pause</div>
                <div className="text-2xl font-semibold text-gray-900">
                  {formatTime(todayPointage.break_start)}
                </div>
              </div>

              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <PlayIcon className="mx-auto h-8 w-8 text-primary-400 mb-2" />
                <div className="text-sm text-gray-500">Fin Pause</div>
                <div className="text-2xl font-semibold text-gray-900">
                  {formatTime(todayPointage.break_end)}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500 mb-6 py-8">
              <ClockIcon className="mx-auto h-12 w-12 text-gray-300 mb-4" />
              <p>Aucun pointage aujourd'hui</p>
              <p className="text-sm">Commencez par pointer votre arrivée</p>
            </div>
          )}

          {/* Boutons de pointage */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <button
              onClick={() => handlePointageAction('clock-in')}
              disabled={pointageLoading || (todayPointage?.arrival_time)}
              className="btn-success flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <PlayIcon className="h-4 w-4 mr-2" />
              Arrivée
            </button>
            
            <button
              onClick={() => handlePointageAction('break-start')}
              disabled={pointageLoading || !todayPointage?.arrival_time || todayPointage?.break_start}
              className="btn-warning flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <PauseIcon className="h-4 w-4 mr-2" />
              Pause
            </button>
            
            <button
              onClick={() => handlePointageAction('break-end')}
              disabled={pointageLoading || !todayPointage?.break_start || todayPointage?.break_end}
              className="btn-primary flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <PlayIcon className="h-4 w-4 mr-2" />
              Retour
            </button>
            
            <button
              onClick={() => handlePointageAction('clock-out')}
              disabled={pointageLoading || !todayPointage?.arrival_time || todayPointage?.departure_time}
              className="btn-danger flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <StopIcon className="h-4 w-4 mr-2" />
              Départ
            </button>
          </div>

          {/* Informations sur le pointage actuel */}
          {todayPointage && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-medium text-blue-900">Temps de travail aujourd'hui</h4>
                  <p className="text-2xl font-semibold text-blue-600">
                    {todayPointage.total_work_hours ? `${todayPointage.total_work_hours.toFixed(2)}h` : 'En cours...'}
                  </p>
                </div>
                {todayPointage.break_duration_minutes > 0 && (
                  <div className="text-right">
                    <h4 className="text-sm font-medium text-blue-900">Durée de pause</h4>
                    <p className="text-lg font-semibold text-blue-600">
                      {todayPointage.break_duration_minutes} min
                    </p>
                  </div>
                )}
              </div>
              
              {todayPointage.late_reason && (
                <div className="mt-3">
                  <h4 className="text-sm font-medium text-blue-900">Raison du retard</h4>
                  <p className="text-sm text-blue-700">{todayPointage.late_reason}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Historique des pointages */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Historique des Pointages</h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Vos 30 derniers pointages
          </p>
        </div>
        
        {pointages.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {pointages.slice(0, 30).map((pointage) => (
              <li key={pointage.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <CalendarIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">
                        {formatDate(pointage.date)}
                      </div>
                      <div className="text-sm text-gray-500 flex items-center space-x-4">
                        <span>Arrivée: {formatTime(pointage.arrival_time)}</span>
                        <span>Départ: {formatTime(pointage.departure_time)}</span>
                        {pointage.break_start && (
                          <span>Pause: {formatTime(pointage.break_start)} - {formatTime(pointage.break_end)}</span>
                        )}
                      </div>
                      {pointage.late_reason && (
                        <div className="text-xs text-danger-600 mt-1">
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
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-danger-100 text-danger-800">
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
            <h3 className="mt-2 text-sm font-medium text-gray-900">Aucun historique</h3>
            <p className="mt-1 text-sm text-gray-500">
              Votre historique de pointages apparaîtra ici.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PointagePage;
