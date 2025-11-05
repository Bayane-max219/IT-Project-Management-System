import api from './api';

const taskService = {
  async getTasks() {
    const response = await api.get('/tasks/');
    return response.data;
  },

  async getTask(taskId) {
    const response = await api.get(`/tasks/${taskId}/`);
    return response.data;
  },

  async getMyTasks() {
    const response = await api.get('/tasks/my-tasks/');
    return response.data;
  },

  async createTask(taskData) {
    const response = await api.post('/tasks/', taskData);
    return response.data;
  },

  async updateTask(taskId, taskData) {
    const response = await api.put(`/tasks/${taskId}/`, taskData);
    return response.data;
  },

  async updateTaskStatus(taskId, status) {
    const response = await api.post(`/tasks/${taskId}/status/`, { status });
    return response.data;
  },

  async deleteTask(taskId) {
    const response = await api.delete(`/tasks/${taskId}/`);
    return response.data;
  },

  async getTaskComments(taskId) {
    const response = await api.get(`/tasks/${taskId}/comments/`);
    return response.data;
  },

  async addTaskComment(taskId, content) {
    const response = await api.post(`/tasks/${taskId}/comments/`, { content });
    return response.data;
  },

  async getTaskStats() {
    const response = await api.get('/tasks/stats/');
    return response.data;
  },
};

export default taskService;
