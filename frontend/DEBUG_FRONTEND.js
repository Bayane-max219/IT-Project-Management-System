// Script de debug pour le frontend
const fs = require('fs');
const path = require('path');

console.log('🔍 DEBUG FRONTEND - MARIE CLIENT');
console.log('================================');

// 1. Ajouter du debug au ClientDashboard
const dashboardPath = path.join(__dirname, 'src', 'pages', 'client', 'ClientDashboard.js');

console.log('\n1. Ajout de debug au ClientDashboard...');

try {
    let content = fs.readFileSync(dashboardPath, 'utf8');
    
    // Vérifier si le debug est déjà ajouté
    if (content.includes('DEBUG MARIE')) {
        console.log('✅ Debug déjà présent dans ClientDashboard');
    } else {
        // Ajouter du debug dans fetchData
        const debugCode = `  const fetchData = async () => {
    try {
      console.log('🔍 DEBUG MARIE: Début fetchData');
      const projectsData = await projectService.getProjects();
      console.log('🔍 DEBUG MARIE: Données reçues:', projectsData);
      console.log('🔍 DEBUG MARIE: Type des données:', typeof projectsData);
      console.log('🔍 DEBUG MARIE: Est un tableau?', Array.isArray(projectsData));
      console.log('🔍 DEBUG MARIE: Longueur:', projectsData?.length);
      
      // S'assurer que projectsData est un tableau
      const finalProjects = Array.isArray(projectsData) ? projectsData : [];
      console.log('🔍 DEBUG MARIE: Projets finaux:', finalProjects);
      setProjects(finalProjects);
    } catch (error) {
      console.error('🔍 DEBUG MARIE: Erreur lors du chargement des projets:', error);
      setProjects([]); // Définir un tableau vide en cas d'erreur
    } finally {
      setLoading(false);
    }
  };`;

        // Remplacer la fonction fetchData
        content = content.replace(
            /const fetchData = async \(\) => \{[\s\S]*?\};/,
            debugCode
        );

        fs.writeFileSync(dashboardPath, content, 'utf8');
        console.log('✅ Debug ajouté au ClientDashboard');
    }
} catch (error) {
    console.error('❌ Erreur ClientDashboard:', error.message);
}

// 2. Ajouter du debug au ClientProjectsPage
const projectsPagePath = path.join(__dirname, 'src', 'pages', 'client', 'ClientProjectsPage.js');

console.log('\n2. Ajout de debug au ClientProjectsPage...');

try {
    let content = fs.readFileSync(projectsPagePath, 'utf8');
    
    if (content.includes('DEBUG MARIE PROJECTS')) {
        console.log('✅ Debug déjà présent dans ClientProjectsPage');
    } else {
        // Ajouter du debug dans fetchProjects
        const debugCode = `  const fetchProjects = async () => {
    try {
      console.log('🔍 DEBUG MARIE PROJECTS: Début fetchProjects');
      const projectsData = await projectService.getProjects();
      console.log('🔍 DEBUG MARIE PROJECTS: Données reçues:', projectsData);
      console.log('🔍 DEBUG MARIE PROJECTS: Type:', typeof projectsData);
      console.log('🔍 DEBUG MARIE PROJECTS: Longueur:', projectsData?.length);
      
      // S'assurer que projectsData est un tableau
      const finalProjects = Array.isArray(projectsData) ? projectsData : [];
      console.log('🔍 DEBUG MARIE PROJECTS: Projets finaux:', finalProjects);
      setProjects(finalProjects);
    } catch (error) {
      console.error('🔍 DEBUG MARIE PROJECTS: Erreur:', error);
      toast.error('Erreur lors du chargement des projets');
      setProjects([]); // Définir un tableau vide en cas d'erreur
    } finally {
      setLoading(false);
    }
  };`;

        content = content.replace(
            /const fetchProjects = async \(\) => \{[\s\S]*?\};/,
            debugCode
        );

        fs.writeFileSync(projectsPagePath, content, 'utf8');
        console.log('✅ Debug ajouté au ClientProjectsPage');
    }
} catch (error) {
    console.error('❌ Erreur ClientProjectsPage:', error.message);
}

// 3. Ajouter du debug au projectService
const servicePath = path.join(__dirname, 'src', 'services', 'projectService.js');

console.log('\n3. Ajout de debug au projectService...');

try {
    let content = fs.readFileSync(servicePath, 'utf8');
    
    if (content.includes('DEBUG API')) {
        console.log('✅ Debug déjà présent dans projectService');
    } else {
        // Ajouter du debug dans getProjects
        const debugCode = `  async getProjects() {
    console.log('🔍 DEBUG API: Appel getProjects()');
    console.log('🔍 DEBUG API: URL:', api.defaults.baseURL + '/projects/');
    
    try {
      const response = await api.get('/projects/');
      console.log('🔍 DEBUG API: Réponse status:', response.status);
      console.log('🔍 DEBUG API: Réponse headers:', response.headers);
      console.log('🔍 DEBUG API: Réponse data:', response.data);
      console.log('🔍 DEBUG API: Type de data:', typeof response.data);
      
      return response.data;
    } catch (error) {
      console.error('🔍 DEBUG API: Erreur getProjects:', error);
      console.error('🔍 DEBUG API: Status:', error.response?.status);
      console.error('🔍 DEBUG API: Data:', error.response?.data);
      throw error;
    }
  },`;

        content = content.replace(
            /async getProjects\(\) \{[\s\S]*?\},/,
            debugCode
        );

        fs.writeFileSync(servicePath, content, 'utf8');
        console.log('✅ Debug ajouté au projectService');
    }
} catch (error) {
    console.error('❌ Erreur projectService:', error.message);
}

console.log('\n🎉 DEBUG AJOUTÉ!');
console.log('\nÉtapes suivantes:');
console.log('1. Redémarrez le frontend: npm start');
console.log('2. Ouvrez F12 → Console');
console.log('3. Connectez-vous comme Marie');
console.log('4. Regardez les messages "DEBUG MARIE" dans la console');
console.log('5. Cela nous dira exactement ce qui se passe!');
