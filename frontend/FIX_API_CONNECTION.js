// Script pour corriger la connexion API
const fs = require('fs');
const path = require('path');

console.log('🔧 CORRECTION DE LA CONNEXION API');
console.log('================================');

// Chemin vers le fichier api.js
const apiFilePath = path.join(__dirname, 'src', 'services', 'api.js');

console.log('\n1. Lecture du fichier api.js...');

try {
    let content = fs.readFileSync(apiFilePath, 'utf8');
    console.log('✅ Fichier lu avec succès');
    
    // Afficher l'URL actuelle
    const currentUrlMatch = content.match(/API_BASE_URL = .* \|\| '([^']+)'/);
    if (currentUrlMatch) {
        console.log(`📍 URL actuelle: ${currentUrlMatch[1]}`);
    }
    
    console.log('\n2. Correction de l\'URL...');
    
    // Remplacer localhost par 127.0.0.1
    const newContent = content.replace(
        /const API_BASE_URL = process\.env\.REACT_APP_API_URL \|\| 'http:\/\/localhost:8000\/api';/,
        "const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';"
    );
    
    // Vérifier si le changement a été fait
    if (newContent !== content) {
        fs.writeFileSync(apiFilePath, newContent, 'utf8');
        console.log('✅ URL corrigée: http://localhost:8000 → http://127.0.0.1:8000');
        console.log('✅ Fichier api.js mis à jour');
    } else {
        console.log('ℹ️ URL déjà correcte ou pattern non trouvé');
    }
    
    console.log('\n3. Vérification finale...');
    const updatedContent = fs.readFileSync(apiFilePath, 'utf8');
    const updatedUrlMatch = updatedContent.match(/API_BASE_URL = .* \|\| '([^']+)'/);
    if (updatedUrlMatch) {
        console.log(`✅ Nouvelle URL: ${updatedUrlMatch[1]}`);
    }
    
    console.log('\n🎉 CORRECTION TERMINÉE!');
    console.log('\nÉtapes suivantes:');
    console.log('1. Redémarrez le serveur frontend: npm start');
    console.log('2. Videz le cache du navigateur: Ctrl+Shift+R');
    console.log('3. Testez la connexion Marie');
    
} catch (error) {
    console.error('❌ Erreur:', error.message);
    console.log('\n🔧 CORRECTION MANUELLE:');
    console.log('1. Ouvrez: frontend/src/services/api.js');
    console.log('2. Changez la ligne 3:');
    console.log('   AVANT: const API_BASE_URL = process.env.REACT_APP_API_URL || \'http://localhost:8000/api\';');
    console.log('   APRÈS: const API_BASE_URL = process.env.REACT_APP_API_URL || \'http://127.0.0.1:8000/api\';');
    console.log('3. Sauvegardez et redémarrez le frontend');
}
