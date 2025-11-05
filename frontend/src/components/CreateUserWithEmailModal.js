import React, { useState } from 'react';
import { XMarkIcon, EnvelopeIcon, KeyIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';
import authService from '../services/authService';

const CreateUserWithEmailModal = ({ isOpen, onClose, onUserCreated }) => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    role: 'developer',
    username: ''
  });
  const [loading, setLoading] = useState(false);
  const [createdUser, setCreatedUser] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Générer le username automatiquement
      const username = `${formData.first_name.toLowerCase()}_${formData.last_name.toLowerCase()}`;
      const dataToSend = { ...formData, username };

      const response = await authService.createUserWithEmail(dataToSend);
      
      setCreatedUser(response);
      toast.success(`Utilisateur créé ! Email envoyé à ${formData.email}`);
      
      if (onUserCreated) {
        onUserCreated(response);
      }
    } catch (error) {
      console.error('Erreur:', error);
      toast.error('Erreur lors de la création de l\'utilisateur');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      role: 'developer',
      username: ''
    });
    setCreatedUser(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium text-gray-900">
            {createdUser ? 'Utilisateur Créé' : 'Créer un Utilisateur'}
          </h3>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {createdUser ? (
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-md p-4">
              <div className="flex">
                <EnvelopeIcon className="h-5 w-5 text-green-400 mr-2" />
                <div>
                  <h4 className="text-sm font-medium text-green-800">
                    Compte créé avec succès !
                  </h4>
                  <p className="text-sm text-green-700 mt-1">
                    Un email avec les identifiants a été envoyé à {createdUser.email}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
              <div className="flex">
                <KeyIcon className="h-5 w-5 text-blue-400 mr-2" />
                <div>
                  <h4 className="text-sm font-medium text-blue-800">
                    Identifiants temporaires
                  </h4>
                  <p className="text-sm text-blue-700 mt-1">
                    <strong>Email :</strong> {createdUser.email}<br />
                    <strong>Mot de passe :</strong> {createdUser.temporary_password}
                  </p>
                  <p className="text-xs text-blue-600 mt-2">
                    L'utilisateur devra changer son mot de passe lors de sa première connexion.
                  </p>
                </div>
              </div>
            </div>

            <button
              onClick={handleClose}
              className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700"
            >
              Fermer
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Prénom</label>
                <input
                  type="text"
                  required
                  value={formData.first_name}
                  onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Nom</label>
                <input
                  type="text"
                  required
                  value={formData.last_name}
                  onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Téléphone</label>
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({...formData, phone: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Rôle</label>
              <select
                value={formData.role}
                onChange={(e) => setFormData({...formData, role: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
              >
                <option value="developer">Développeur</option>
                <option value="client">Client</option>
                <option value="admin">Administrateur</option>
              </select>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
              <p className="text-sm text-yellow-800">
                <EnvelopeIcon className="h-4 w-4 inline mr-1" />
                Un email sera automatiquement envoyé avec les identifiants de connexion.
              </p>
            </div>

            <div className="flex space-x-3">
              <button
                type="button"
                onClick={handleClose}
                className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400"
              >
                Annuler
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 disabled:opacity-50"
              >
                {loading ? 'Création...' : 'Créer & Envoyer'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default CreateUserWithEmailModal;
