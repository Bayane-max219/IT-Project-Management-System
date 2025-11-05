import React, { useState, useEffect } from 'react';
import { PlusIcon, PencilIcon, TrashIcon, UserIcon, EnvelopeIcon, KeyIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';
import authService from '../../services/authService';
import CreateUserWithEmailModal from '../../components/CreateUserWithEmailModal';

const UsersPage = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    role: 'developer',
    phone: '',
    password: '',
    password_confirm: '',
  });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const usersData = await authService.getUsers();
      console.log('Données utilisateurs reçues:', usersData); // Debug
      
      // Gérer les différents formats de réponse
      let usersList = [];
      if (Array.isArray(usersData)) {
        usersList = usersData;
      } else if (usersData && Array.isArray(usersData.results)) {
        // Format paginé Django REST Framework
        usersList = usersData.results;
      } else if (usersData && typeof usersData === 'object') {
        // Autre format d'objet
        usersList = Object.values(usersData);
      }
      
      console.log('Liste utilisateurs finale:', usersList); // Debug
      setUsers(usersList);
    } catch (error) {
      console.error('Erreur lors du chargement des utilisateurs:', error);
      toast.error('Erreur lors du chargement des utilisateurs');
      setUsers([]); // Définir un tableau vide en cas d'erreur
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingUser) {
        const updateData = { ...formData };
        delete updateData.password;
        delete updateData.password_confirm;
        await authService.updateUser(editingUser.id, updateData);
        toast.success('Utilisateur modifié avec succès !');
      } else {
        await authService.createUser(formData);
        toast.success('Utilisateur créé avec succès !');
      }
      setShowModal(false);
      setEditingUser(null);
      resetForm();
      await fetchUsers();
    } catch (error) {
      console.error('🔍 Erreur complète:', error);
      console.error('🔍 Erreur response:', error.response);
      console.error('🔍 Erreur data:', error.response?.data);
      console.error('🔍 Données envoyées:', formData);
      
      // Afficher l'erreur spécifique du backend
      let errorMessage = 'Erreur lors de la sauvegarde';
      
      if (error.response?.data) {
        const errorData = error.response.data;
        
        // Gérer les erreurs de validation Django
        if (typeof errorData === 'object') {
          const errors = [];
          
          // Erreurs spécifiques par champ
          Object.keys(errorData).forEach(field => {
            const fieldErrors = errorData[field];
            if (Array.isArray(fieldErrors)) {
              fieldErrors.forEach(err => {
                if (field === 'email' && err.includes('already exists')) {
                  errors.push('Cet email est déjà utilisé');
                } else if (field === 'username' && err.includes('already exists')) {
                  errors.push('Ce nom d\'utilisateur est déjà pris');
                } else {
                  errors.push(`${field}: ${err}`);
                }
              });
            }
          });
          
          if (errors.length > 0) {
            errorMessage = errors.join(', ');
          }
        } else if (errorData.message) {
          errorMessage = errorData.message;
        } else if (errorData.error) {
          errorMessage = errorData.error;
        }
      }
      
      toast.error(errorMessage);
    }
  };

  const handleEdit = (user) => {
    setEditingUser(user);
    setFormData({
      username: user.username,
      email: user.email,
      first_name: user.first_name,
      last_name: user.last_name,
      role: user.role,
      phone: user.phone || '',
      password: '',
      password_confirm: '',
    });
    setShowModal(true);
  };

  const handleDelete = async (userId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) {
      try {
        await authService.deleteUser(userId);
        toast.success('Utilisateur supprimé avec succès !');
        fetchUsers();
      } catch (error) {
        console.error('Erreur:', error);
        toast.error('Erreur lors de la suppression');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      role: 'developer',
      phone: '',
      password: '',
      password_confirm: '',
    });
  };

  const getRoleBadgeClass = (role) => {
    switch (role) {
      case 'admin':
        return 'bg-red-100 text-red-800';
      case 'developer':
        return 'bg-blue-100 text-blue-800';
      case 'client':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRoleLabel = (role) => {
    switch (role) {
      case 'admin':
        return 'Administrateur';
      case 'developer':
        return 'Développeur';
      case 'client':
        return 'Client';
      default:
        return role;
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
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Gestion des Utilisateurs</h1>
          <p className="mt-2 text-sm text-gray-700">
            Gérez tous les utilisateurs de l'entreprise
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowEmailModal(true)}
            className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 flex items-center"
          >
            <EnvelopeIcon className="h-4 w-4 mr-2" />
            Créer & Envoyer Email
          </button>
          <button
            onClick={() => setShowInviteModal(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center"
          >
            <KeyIcon className="h-4 w-4 mr-2" />
            Envoyer Invitation
          </button>
          <button
            onClick={() => {
              resetForm();
              setEditingUser(null);
              setShowModal(true);
            }}
            className="btn-primary flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Création Manuelle
          </button>
        </div>
      </div>

      {/* Statistiques rapides */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <UserIcon className="h-6 w-6 text-red-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Administrateurs</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {Array.isArray(users) ? users.filter(u => u.role === 'admin').length : 0}
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
                <UserIcon className="h-6 w-6 text-blue-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Développeurs</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {Array.isArray(users) ? users.filter(u => u.role === 'developer').length : 0}
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
                <UserIcon className="h-6 w-6 text-green-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Clients</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {Array.isArray(users) ? users.filter(u => u.role === 'client').length : 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Liste des utilisateurs */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        {Array.isArray(users) && users.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {users.map((user) => (
              <li key={user.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center min-w-0 flex-1">
                    <div className="flex-shrink-0">
                      <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                        <span className="text-sm font-medium text-gray-700">
                          {user.first_name?.[0]}{user.last_name?.[0]}
                        </span>
                      </div>
                    </div>
                    <div className="ml-4 min-w-0 flex-1">
                      <div className="flex items-center justify-between">
                        <div className="text-sm font-medium text-gray-900 truncate">
                          {user.first_name} {user.last_name}
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRoleBadgeClass(user.role)}`}>
                            {getRoleLabel(user.role)}
                          </span>
                          {!user.is_active && (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                              Inactif
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="mt-2 flex items-center text-sm text-gray-500">
                        <div className="flex-shrink-0">
                          Email: {user.email}
                        </div>
                        <div className="ml-4">
                          Username: {user.username}
                        </div>
                        {user.phone && (
                          <div className="ml-4">
                            Tél: {user.phone}
                          </div>
                        )}
                        <div className="ml-4">
                          Créé le: {new Date(user.created_at).toLocaleDateString('fr-FR')}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <button
                      onClick={() => handleEdit(user)}
                      className="text-primary-600 hover:text-primary-500"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(user.id)}
                      className="text-danger-600 hover:text-danger-500"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center py-12">
            <h3 className="mt-2 text-sm font-medium text-gray-900">Aucun utilisateur</h3>
            <p className="mt-1 text-sm text-gray-500">
              Commencez par créer un nouvel utilisateur.
            </p>
          </div>
        )}
      </div>

      {/* Modal de création/édition */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingUser ? 'Modifier l\'Utilisateur' : 'Nouvel Utilisateur'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Prénom</label>
                    <input
                      type="text"
                      required
                      className="input-field"
                      value={formData.first_name}
                      onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Nom</label>
                    <input
                      type="text"
                      required
                      className="input-field"
                      value={formData.last_name}
                      onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Username</label>
                  <input
                    type="text"
                    required
                    className="input-field"
                    value={formData.username}
                    onChange={(e) => setFormData({...formData, username: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    type="email"
                    required
                    className="input-field"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Téléphone</label>
                  <input
                    type="tel"
                    className="input-field"
                    value={formData.phone}
                    onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">Rôle</label>
                  <select
                    required
                    className="input-field"
                    value={formData.role}
                    onChange={(e) => setFormData({...formData, role: e.target.value})}
                  >
                    <option value="developer">Développeur</option>
                    <option value="client">Client</option>
                    <option value="admin">Administrateur</option>
                  </select>
                </div>
                
                {!editingUser && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Mot de passe</label>
                      <input
                        type="password"
                        required={!editingUser}
                        className="input-field"
                        value={formData.password}
                        onChange={(e) => setFormData({...formData, password: e.target.value})}
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Confirmer le mot de passe</label>
                      <input
                        type="password"
                        required={!editingUser}
                        className="input-field"
                        value={formData.password_confirm}
                        onChange={(e) => setFormData({...formData, password_confirm: e.target.value})}
                      />
                    </div>
                  </>
                )}
                
                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="btn-secondary"
                  >
                    Annuler
                  </button>
                  <button type="submit" className="btn-primary">
                    {editingUser ? 'Modifier' : 'Créer'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Modal pour créer un utilisateur avec email */}
      <CreateUserWithEmailModal
        isOpen={showEmailModal}
        onClose={() => setShowEmailModal(false)}
        onUserCreated={(user) => {
          fetchUsers();
          setShowEmailModal(false);
        }}
      />

      {/* Modal pour envoyer une invitation */}
      {showInviteModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">Envoyer une Invitation</h3>
              <button
                onClick={() => setShowInviteModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            </div>
            
            <InviteForm onClose={() => setShowInviteModal(false)} />
          </div>
        </div>
      )}
    </div>
  );
};

// Composant pour le formulaire d'invitation
const InviteForm = ({ onClose }) => {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('developer');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      console.log('🔍 INVITATION: Envoi en cours...');
      console.log('   Email:', email);
      console.log('   Rôle:', role);
      const response = await authService.sendRegistrationInvitation(email, role);
      console.log('🔍 INVITATION: Réponse reçue:', response);
      toast.success(`Invitation envoyée à ${email}`);
      onClose();
    } catch (error) {
      console.error('🔍 INVITATION: Erreur complète:', error);
      console.error('🔍 INVITATION: Erreur response:', error.response);
      console.error('🔍 INVITATION: Erreur data:', error.response?.data);
      console.error('🔍 INVITATION: Status:', error.response?.status);
      console.error('🔍 INVITATION: Status Text:', error.response?.statusText);
      
      // Log détaillé de l'erreur data
      if (error.response?.data) {
        console.error('🔍 INVITATION: Détails erreur:');
        Object.keys(error.response.data).forEach(key => {
          console.error(`   ${key}:`, error.response.data[key]);
        });
      }
      
      // Afficher l'erreur spécifique
      let errorMessage = error.response?.data?.error || 
                        error.response?.data?.message || 
                        error.message || 
                        'Erreur lors de l\'envoi de l\'invitation';
      
      // Message plus clair pour l'email existant
      if (errorMessage.includes('existe déjà')) {
        errorMessage = `❌ Cet email est déjà utilisé par un autre utilisateur. Veuillez utiliser un email différent.`;
      }
      
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">Email</label>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
          placeholder="email@exemple.com"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Rôle</label>
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
        >
          <option value="developer">Développeur</option>
          <option value="client">Client</option>
        </select>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
        <p className="text-sm text-blue-800">
          <KeyIcon className="h-4 w-4 inline mr-1" />
          Une clé d'inscription sera envoyée par email. Elle expire dans 7 jours.
        </p>
      </div>

      <div className="flex space-x-3">
        <button
          type="button"
          onClick={onClose}
          className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400"
        >
          Annuler
        </button>
        <button
          type="submit"
          disabled={loading}
          className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Envoi...' : 'Envoyer Invitation'}
        </button>
      </div>
    </form>
  );
};

export default UsersPage;
