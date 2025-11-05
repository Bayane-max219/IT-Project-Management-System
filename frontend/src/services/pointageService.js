import api from './api';

const pointageService = {
  async getPointages() {
    const response = await api.get('/pointage/');
    return response.data;
  },

  async getMyPointages() {
    const response = await api.get('/pointage/my-pointages/');
    return response.data;
  },

  async getTodayPointage() {
    const response = await api.get('/pointage/today/');
    return response.data;
  },

  async clockIn(data = {}) {
    console.log('🔍 SERVICE: clockIn appelé avec:', data);
    console.log('🔍 SERVICE: Type de data:', typeof data);
    console.log('🔍 SERVICE: JSON.stringify(data):', JSON.stringify(data));
    
    const response = await api.post('/pointage/clock-in/', data);
    return response.data;
  },

  async clockOut(data = {}) {
    const response = await api.post('/pointage/clock-out/', data);
    return response.data;
  },

  async breakStart(data = {}) {
    const response = await api.post('/pointage/break-start/', data);
    return response.data;
  },

  async breakEnd(data = {}) {
    const response = await api.post('/pointage/break-end/', data);
    return response.data;
  },

  async createPointage(pointageData) {
    const response = await api.post('/pointage/', pointageData);
    return response.data;
  },

  async updatePointage(pointageId, pointageData) {
    const response = await api.put(`/pointage/${pointageId}/`, pointageData);
    return response.data;
  },

  async getPointageStats() {
    const response = await api.get('/pointage/stats/');
    return response.data;
  },

  async getAbsenceRequests() {
    const response = await api.get('/pointage/absences/');
    return response.data;
  },

  async createAbsenceRequest(absenceData) {
    const response = await api.post('/pointage/absences/', absenceData);
    return response.data;
  },

  async approveAbsence(absenceId, action, approvalNotes = '') {
    const response = await api.post(`/pointage/absences/${absenceId}/approve/`, {
      action,
      approval_notes: approvalNotes,
    });
    return response.data;
  },
};

export default pointageService;
