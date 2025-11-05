import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { toast } from 'react-toastify';
import authService from '../../services/authService';

const ProfilePage = () => {
  const { user, updateUser } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  // Synchroniser formData avec user quand user change
  useEffect(() => {
    if (user) {
      setFormData(prev => ({
        ...prev,
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || ''
      }));
    }
  }, [user]);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // Validation des mots de passe
      if (formData.new_password && formData.new_password !== formData.confirm_password) {
        toast.error('Les mots de passe ne correspondent pas');
        return;
      }

      // Préparer les données à envoyer
      const updateData = {
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email
      };

      // Ajouter le mot de passe seulement s'il est fourni ET non vide
      if (formData.new_password && formData.new_password.trim() !== '') {
        updateData.current_password = formData.current_password;
        updateData.new_password = formData.new_password;
      }

      // Mettre à jour le profil
      const updatedUser = await authService.updateProfile(updateData);
      
      // Mettre à jour le contexte utilisateur
      if (updateUser) {
        updateUser(updatedUser);
      }
      
      // Mettre à jour le formulaire avec les nouvelles données
      setFormData({
        first_name: updatedUser.first_name || '',
        last_name: updatedUser.last_name || '',
        email: updatedUser.email || '',
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
      
      toast.success('Profil mis à jour avec succès !');
      setIsEditing(false);
      
    } catch (error) {
      console.error('Erreur lors de la mise à jour:', error);
      console.error('Détails de l\'erreur:', error.response?.data);
      
      // Afficher les erreurs spécifiques si disponibles
      if (error.response?.data) {
        const errorData = error.response.data;
        if (typeof errorData === 'object') {
          // Afficher chaque erreur de champ
          Object.keys(errorData).forEach(key => {
            const message = Array.isArray(errorData[key]) ? errorData[key][0] : errorData[key];
            toast.error(`${key}: ${message}`);
          });
        } else {
          toast.error(errorData.toString());
        }
      } else {
        toast.error('Erreur lors de la mise à jour du profil');
      }
    }
  };

  const handleCancel = () => {
    setFormData({
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      email: user?.email || '',
      current_password: '',
      new_password: '',
      confirm_password: ''
    });
    setIsEditing(false);
  };

  return (
    <div className="max-w-2xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-semibold text-gray-900">Mon Profil</h1>
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className="btn-primary"
              >
                Modifier
              </button>
            )}
          </div>

          {!isEditing ? (
            // Mode affichage
            <div className="space-y-6">
              <div className="flex items-center space-x-4">
                <div className="h-20 w-20 rounded-full bg-primary-600 flex items-center justify-center">
                  <span className="text-white text-2xl font-medium">
                    {user?.first_name?.[0]}{user?.last_name?.[0]}
                  </span>
                </div>
                <div>
                  <h2 className="text-xl font-medium text-gray-900">
                    {user?.first_name} {user?.last_name}
                  </h2>
                  <p className="text-sm text-gray-500">{getRoleLabel(user?.role)}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Prénom</label>
                  <p className="mt-1 text-sm text-gray-900">{user?.first_name}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Nom</label>
                  <p className="mt-1 text-sm text-gray-900">{user?.last_name}</p>
                </div>
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <p className="mt-1 text-sm text-gray-900">{user?.email}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Rôle</label>
                  <p className="mt-1 text-sm text-gray-900">{getRoleLabel(user?.role)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Statut</label>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    user?.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {user?.is_active ? 'Actif' : 'Inactif'}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            // Mode édition
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
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
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    type="email"
                    required
                    className="input-field"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                  />
                </div>
              </div>

              <div className="border-t border-gray-200 pt-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Changer le mot de passe</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Mot de passe actuel</label>
                    <input
                      type="password"
                      className="input-field"
                      value={formData.current_password}
                      onChange={(e) => setFormData({...formData, current_password: e.target.value})}
                      placeholder="Laissez vide si vous ne voulez pas changer"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Nouveau mot de passe</label>
                    <input
                      type="password"
                      className="input-field"
                      value={formData.new_password}
                      onChange={(e) => setFormData({...formData, new_password: e.target.value})}
                      placeholder="Laissez vide si vous ne voulez pas changer"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Confirmer le nouveau mot de passe</label>
                    <input
                      type="password"
                      className="input-field"
                      value={formData.confirm_password}
                      onChange={(e) => setFormData({...formData, confirm_password: e.target.value})}
                      placeholder="Confirmez le nouveau mot de passe"
                    />
                  </div>
                </div>
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={handleCancel}
                  className="btn-secondary"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="btn-primary"
                >
                  Enregistrer
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
