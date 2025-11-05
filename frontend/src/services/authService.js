import api from './api';

const authService = {
  async login(email, password) {
    const response = await api.post('/auth/login/', { email, password });
    return response.data;
  },

  async logout(refreshToken) {
    const response = await api.post('/auth/logout/', { refresh: refreshToken });
    return response.data;
  },

  async getProfile() {
    const response = await api.get('/auth/profile/');
    return response.data;
  },

  async updateProfile(profileData) {
    const response = await api.put('/auth/profile/update/', profileData);
    return response.data;
  },

  async changePassword(oldPassword, newPassword, newPasswordConfirm) {
    const response = await api.post('/auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm,
    });
    return response.data;
  },

  async getUsers() {
    const response = await api.get('/auth/users/');
    return response.data;
  },

  async createUserWithEmail(userData) {
    const response = await api.post('/auth/create-user-with-email/', userData);
    return response.data;
  },

  async sendRegistrationInvitation(email, role) {
    const response = await api.post('/auth/send-invitation/', { email, role });
    return response.data;
  },

  async registerWithKey(userData) {
    const response = await api.post('/auth/register-with-key/', userData);
    return response.data;
  },

  async createUser(userData) {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  },

  async updateUser(userId, userData) {
    const response = await api.put(`/auth/users/${userId}/`, userData);
    return response.data;
  },

  async deleteUser(userId) {
    const response = await api.delete(`/auth/users/${userId}/`);
    return response.data;
  },
};

export default authService;
