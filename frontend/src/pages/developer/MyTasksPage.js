import React, { useState, useEffect } from 'react';
import { CheckIcon, CalendarIcon, ClockIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';
import taskService from '../../services/taskService';

const MyTasksPage = () => {
  const [tasks, setTasks] = useState([]);
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');

  useEffect(() => {
    fetchTasks();
  }, []);

  useEffect(() => {
    filterTasks();
  }, [tasks, statusFilter, priorityFilter]);

  const fetchTasks = async () => {
    try {
      const tasksData = await taskService.getMyTasks();
      console.log('Mes tâches reçues:', tasksData); // Debug
      
      // Gérer le format des tâches (même logique que les autres pages)
      let tasksList = [];
      if (Array.isArray(tasksData)) {
        tasksList = tasksData;
      } else if (tasksData && Array.isArray(tasksData.results)) {
        tasksList = tasksData.results;
      } else if (tasksData && typeof tasksData === 'object') {
        tasksList = Object.values(tasksData);
      }
      
      console.log('Liste finale des tâches:', tasksList); // Debug
      setTasks(tasksList);
    } catch (error) {
      console.error('Erreur lors du chargement des tâches:', error);
      toast.error('Erreur lors du chargement des tâches');
    } finally {
      setLoading(false);
    }
  };

  const filterTasks = () => {
    let filtered = tasks;

    if (statusFilter !== 'all') {
      filtered = filtered.filter(task => task.status === statusFilter);
    }

    if (priorityFilter !== 'all') {
      filtered = filtered.filter(task => task.priority === priorityFilter);
    }

    setFilteredTasks(filtered);
  };

  const updateTaskStatus = async (taskId, newStatus) => {
    try {
      await taskService.updateTaskStatus(taskId, newStatus);
      toast.success('Statut mis à jour !');
      fetchTasks();
    } catch (error) {
      console.error('Erreur:', error);
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
      case 'completed':
        return 'Terminé';
      case 'blocked':
        return 'Bloqué';
      case 'testing':
        return 'En test';
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

  const todoTasks = tasks.filter(t => t.status === 'todo').length;
  const inProgressTasks = tasks.filter(t => t.status === 'in_progress').length;
  const completedTasks = tasks.filter(t => t.status === 'completed').length;
  const overdueTasks = tasks.filter(t => t.is_overdue).length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Mes Tâches</h1>
        <p className="mt-2 text-sm text-gray-700">
          Gérez vos tâches assignées et suivez votre progression
        </p>
      </div>

      {/* Statistiques rapides */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckIcon className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">À faire</dt>
                  <dd className="text-lg font-medium text-gray-900">{todoTasks}</dd>
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
                  <dt className="text-sm font-medium text-gray-500 truncate">En cours</dt>
                  <dd className="text-lg font-medium text-gray-900">{inProgressTasks}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckIcon className="h-6 w-6 text-success-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Terminées</dt>
                  <dd className="text-lg font-medium text-gray-900">{completedTasks}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CalendarIcon className="h-6 w-6 text-danger-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">En retard</dt>
                  <dd className="text-lg font-medium text-gray-900">{overdueTasks}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Filtres */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex flex-wrap gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Statut</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="input-field w-auto"
            >
              <option value="all">Tous les statuts</option>
              <option value="todo">À faire</option>
              <option value="in_progress">En cours</option>
              <option value="testing">En test</option>
              <option value="completed">Terminé</option>
              <option value="blocked">Bloqué</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Priorité</label>
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="input-field w-auto"
            >
              <option value="all">Toutes les priorités</option>
              <option value="low">Basse</option>
              <option value="medium">Moyenne</option>
              <option value="high">Haute</option>
              <option value="urgent">Urgente</option>
            </select>
          </div>
        </div>
      </div>

      {/* Liste des tâches */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        {filteredTasks.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {filteredTasks.map((task) => (
              <li key={task.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center min-w-0 flex-1">
                    <div className="flex-shrink-0">
                      <CheckIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <div className="ml-4 min-w-0 flex-1">
                      <div className="flex items-center justify-between">
                        <div className="text-sm font-medium text-gray-900 truncate">
                          {task.title}
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`status-badge ${getStatusBadgeClass(task.status)}`}>
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
                        {task.is_overdue && (
                          <div className="ml-4 text-danger-600 font-medium">
                            En retard
                          </div>
                        )}
                      </div>
                      <div className="mt-2 text-sm text-gray-600">
                        {task.description}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    {task.status !== 'completed' && (
                      <select
                        value={task.status}
                        onChange={(e) => updateTaskStatus(task.id, e.target.value)}
                        className="text-sm border border-gray-300 rounded px-2 py-1"
                      >
                        <option value="todo">À faire</option>
                        <option value="in_progress">En cours</option>
                        <option value="testing">En test</option>
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
              {statusFilter !== 'all' || priorityFilter !== 'all' 
                ? 'Aucune tâche ne correspond aux filtres sélectionnés.'
                : 'Vous n\'avez aucune tâche assignée pour le moment.'
              }
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MyTasksPage;
