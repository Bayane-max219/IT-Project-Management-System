import api from './api';

const projectService = {
  async getProjects() {
    console.log('🔍 DEBUG API: Appel getProjects()');
    console.log('🔍 DEBUG API: URL de base:', api.defaults.baseURL);
    
    try {
      const response = await api.get('/projects/');
      console.log('🔍 DEBUG API: Réponse status:', response.status);
      console.log('🔍 DEBUG API: Réponse data:', response.data);
      console.log('🔍 DEBUG API: Type de data:', typeof response.data);
      
      // Extraire les résultats de la pagination
      const projects = response.data.results || response.data;
      console.log('🔍 DEBUG API: Projets extraits:', projects);
      console.log('🔍 DEBUG API: Longueur projets:', projects?.length);
      
      return projects;
    } catch (error) {
      console.error('🔍 DEBUG API: Erreur getProjects:', error);
      console.error('🔍 DEBUG API: Status:', error.response?.status);
      console.error('🔍 DEBUG API: Data:', error.response?.data);
      throw error;
    }
  },

  async getProject(projectId) {
    const response = await api.get(`/projects/${projectId}/`);
    return response.data;
  },

  async createProject(projectData) {
    const response = await api.post('/projects/', projectData);
    return response.data;
  },

  async updateProject(projectId, projectData) {
    const response = await api.put(`/projects/${projectId}/`, projectData);
    return response.data;
  },

  async deleteProject(projectId) {
    const response = await api.delete(`/projects/${projectId}/`);
    return response.data;
  },

  async addTeamMember(projectId, developerId, roleInProject = 'Développeur') {
    const response = await api.post(`/projects/${projectId}/team/add/`, {
      developer_id: developerId,
      role_in_project: roleInProject,
    });
    return response.data;
  },

  async removeTeamMember(projectId, memberId) {
    const response = await api.delete(`/projects/${projectId}/team/${memberId}/remove/`);
    return response.data;
  },

  async getProjectStats() {
    const response = await api.get('/projects/stats/');
    return response.data;
  },
};

export default projectService;
