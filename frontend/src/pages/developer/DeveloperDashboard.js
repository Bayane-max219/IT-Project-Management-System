import React, { useState, useEffect } from 'react';
import { 
  CheckIcon, 
  ClockIcon, 
  PlayIcon, 
  PauseIcon,
  StopIcon 
} from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';
import taskService from '../../services/taskService';
import pointageService from '../../services/pointageService';

const DeveloperDashboard = () => {
  const [myTasks, setMyTasks] = useState([]);
  const [todayPointage, setTodayPointage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pointageLoading, setPointageLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [tasks, pointage] = await Promise.all([
        taskService.getMyTasks(),
        pointageService.getTodayPointage().catch(() => null) // Ne pas échouer si pas de pointage
      ]);

      setMyTasks(Array.isArray(tasks) ? tasks.slice(0, 5) : []); // Limiter à 5 tâches pour le dashboard
      setTodayPointage(pointage);
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
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
      
      // SOLUTION RADICALE: Forcer la synchronisation
      console.log('🔄 RECHARGEMENT FORCÉ après pointage...');
      
      // Méthode 1: Rechargement immédiat
      setTimeout(async () => {
        console.log('🔄 Tentative 1: Rechargement immédiat');
        try {
          const newPointage = await pointageService.getTodayPointage();
          console.log('✅ Données reçues (tentative 1):', newPointage);
          setTodayPointage(newPointage);
        } catch (error) {
          console.error('❌ Échec tentative 1:', error);
        }
      }, 500);
      
      // Méthode 2: Rechargement avec délai
      setTimeout(async () => {
        console.log('🔄 Tentative 2: Rechargement avec délai');
        try {
          const newPointage = await pointageService.getTodayPointage();
          console.log('✅ Données reçues (tentative 2):', newPointage);
          setTodayPointage(newPointage);
          
          // Forcer un re-render
          setLoading(true);
          setTimeout(() => setLoading(false), 100);
          
        } catch (error) {
          console.error('❌ Échec tentative 2:', error);
        }
      }, 1500);
      
      // Méthode 3: Rechargement complet en dernier recours
      setTimeout(() => {
        console.log('🔄 Tentative 3: Rechargement complet');
        fetchData();
      }, 3000);
    } catch (error) {
      console.error('Erreur pointage:', error);
      
      const errorData = error.response?.data;
      
      // Si justification requise
      if (errorData?.requires_justification) {
        const reason = prompt(errorData.message || 'Veuillez fournir une raison');
        if (reason) {
          // Réessayer avec la raison
          try {
            let result;
            const dataWithReason = { reason: reason };
            
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
                const newPointage = await pointageService.getTodayPointage();
                console.log('✅ Nouvelles données reçues:', newPointage);
                setTodayPointage(newPointage);
                
                // Recharger aussi les tâches
                const tasks = await taskService.getMyTasks();
                setMyTasks(Array.isArray(tasks) ? tasks.slice(0, 5) : []);
                
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
        }
      } else {
        toast.error(errorData?.error || errorData?.message || 'Erreur lors du pointage');
      }
    } finally {
      setPointageLoading(false);
    }
  };

  const updateTaskStatus = async (taskId, newStatus) => {
    try {
      await taskService.updateTaskStatus(taskId, newStatus);
      toast.success('Statut de la tâche mis à jour !');
      fetchData(); // Recharger les données
    } catch (error) {
      console.error('Erreur mise à jour tâche:', error);
      toast.error('Erreur lors de la mise à jour');
    }
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
      default:
        return 'status-badge status-todo';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'todo':
        return 'À faire';
      case 'in_progress':
        return 'En cours';
      case 'completed':
        return 'Terminé';
      case 'blocked':
        return 'Bloqué';
      default:
        return status;
    }
  };

  const formatTime = (timeString) => {
    if (!timeString) return '--:--';
    return timeString.substring(0, 5); // HH:MM
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
        <h1 className="text-2xl font-semibold text-gray-900">Tableau de bord Développeur</h1>
        <p className="mt-2 text-sm text-gray-700">
          Gérez vos tâches et votre pointage quotidien
        </p>
      </div>

      {/* Section Pointage */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Pointage du jour
          </h3>
          
          {todayPointage ? (
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="text-center">
                <div className="text-sm text-gray-500">Arrivée</div>
                <div className="text-lg font-semibold text-gray-900">
                  {formatTime(todayPointage.arrival_time)}
                </div>
                {todayPointage.is_late && (
                  <div className="text-xs text-danger-600">
                    Retard: {todayPointage.late_minutes} min
                  </div>
                )}
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-500">Départ</div>
                <div className="text-lg font-semibold text-gray-900">
                  {formatTime(todayPointage.departure_time)}
                </div>
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-500">Début Pause</div>
                <div className="text-lg font-semibold text-gray-900">
                  {formatTime(todayPointage.break_start)}
                </div>
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-500">Fin Pause</div>
                <div className="text-lg font-semibold text-gray-900">
                  {formatTime(todayPointage.break_end)}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500 mb-6">
              Aucun pointage aujourd'hui
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
        </div>
      </div>

      {/* Mes tâches récentes */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
          <div>
            <h3 className="text-lg leading-6 font-medium text-gray-900">Mes Tâches Récentes</h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Vos 5 tâches les plus récentes
            </p>
          </div>
          <a
            href="/developer/tasks"
            className="text-primary-600 hover:text-primary-500 text-sm font-medium"
          >
            Voir toutes →
          </a>
        </div>
        
        {myTasks.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {myTasks.map((task) => (
              <li key={task.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <CheckIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <div className="ml-4 min-w-0 flex-1">
                      <div className="text-sm font-medium text-gray-900 truncate">
                        {task.title}
                      </div>
                      <div className="text-sm text-gray-500">
                        {task.project.name}
                      </div>
                      {task.due_date && (
                        <div className="text-xs text-gray-400">
                          Échéance: {new Date(task.due_date).toLocaleDateString('fr-FR')}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={getStatusBadgeClass(task.status)}>
                      {getStatusLabel(task.status)}
                    </span>
                    {task.status !== 'completed' && (
                      <select
                        value={task.status}
                        onChange={(e) => updateTaskStatus(task.id, e.target.value)}
                        className="text-xs border border-gray-300 rounded px-2 py-1"
                      >
                        <option value="todo">À faire</option>
                        <option value="in_progress">En cours</option>
                        <option value="completed">Terminé</option>
                        <option value="blocked">Bloqué</option>
                      </select>
                    )}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center py-12">
            <CheckIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">Aucune tâche</h3>
            <p className="mt-1 text-sm text-gray-500">
              Vous n'avez aucune tâche assignée pour le moment.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default DeveloperDashboard;
