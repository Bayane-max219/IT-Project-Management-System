// Utilitaires de formatage de devise pour Madagascar (Ariary)

/**
 * Formate un montant en Ariary Malagasy (MGA)
 * @param {number} amount - Le montant à formater
 * @returns {string} - Le montant formaté en Ariary
 */
export const formatCurrency = (amount) => {
  if (!amount && amount !== 0) return 'Non défini';
  
  return new Intl.NumberFormat('fr-MG', {
    style: 'currency',
    currency: 'MGA',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

/**
 * Formate un montant en Ariary avec le symbole "Ar"
 * @param {number} amount - Le montant à formater
 * @returns {string} - Le montant formaté avec "Ar"
 */
export const formatCurrencySimple = (amount) => {
  if (!amount && amount !== 0) return 'Non défini';
  
  return `${parseFloat(amount).toLocaleString('fr-FR')} Ar`;
};

/**
 * Formate un montant en Ariary pour les formulaires
 * @param {number} amount - Le montant à formater
 * @returns {string} - Le montant formaté pour affichage
 */
export const formatBudgetDisplay = (amount) => {
  if (!amount && amount !== 0) return '0';
  
  return parseFloat(amount).toLocaleString('fr-FR');
};
