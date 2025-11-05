import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs de réponse (DÉSACTIVÉ TEMPORAIREMENT)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // TEMPORAIRE : Ne pas rediriger automatiquement vers login
    console.log('Erreur API:', error.response?.status, error.config?.url);
    
    // Seulement logger l'erreur sans redirection automatique
    if (error.response?.status === 401) {
      console.warn('Erreur 401 détectée mais redirection désactivée');
    }

    return Promise.reject(error);
  }
);

export default api;
