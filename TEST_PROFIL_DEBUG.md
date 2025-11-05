# 🔍 Debug - Erreur Modification Mot de Passe

## ❌ Erreur Actuelle

```
127.0.0.1:8000/api/auth/profile/update/:1  
Failed to load resource: the server responded with a status of 400 (Bad Request)
```

---

## 📋 Étapes de Diagnostic

### **Étape 1 : Voir les détails de l'erreur dans la console**

1. Ouvrir la console du navigateur (F12)
2. Chercher la ligne : `Détails de l'erreur: Object`
3. **Cliquer sur le petit triangle ▶ pour développer l'objet**
4. **Prendre une capture d'écran** de ce qui s'affiche

Vous devriez voir quelque chose comme :
```javascript
{
  current_password: ["Le mot de passe actuel est incorrect."]
  // OU
  new_password: ["Ce champ est requis."]
  // OU autre erreur
}
```

---

### **Étape 2 : Vérifier l'onglet Network**

1. F12 → Onglet **Network**
2. Cocher "Preserve log"
3. Essayer de modifier le mot de passe
4. Chercher la ligne `profile/update/` (en rouge)
5. Cliquer dessus
6. Aller dans l'onglet **Payload** (ou **Request**)
7. **Prendre une capture d'écran** des données envoyées
8. Aller dans l'onglet **Response**
9. **Prendre une capture d'écran** de la réponse

---

## 🧪 Test Manuel

### **Test 1 : Modifier SEULEMENT le prénom (sans mot de passe)**

```bash
1. Aller dans Profil → Modifier
2. Changer UNIQUEMENT le prénom
3. NE PAS toucher aux champs mot de passe
4. Enregistrer
```

**Question** : Est-ce que ça fonctionne ?
- ✅ Oui → Le problème est uniquement avec le changement de mot de passe
- ❌ Non → Le problème est plus général

---

### **Test 2 : Changer le mot de passe**

```bash
1. Aller dans Profil → Modifier
2. Remplir "Mot de passe actuel" : [votre mot de passe actuel]
3. Remplir "Nouveau mot de passe" : Test123!
4. Remplir "Confirmer" : Test123!
5. Enregistrer
```

**Question** : Quelle erreur s'affiche ?
- "Le mot de passe actuel est incorrect"
- "Les mots de passe ne correspondent pas"
- "Ce champ est requis"
- Autre ?

---

## 🔧 Vérifications Backend

### **Vérifier que le serveur est bien démarré**

```bash
# Dans le terminal backend
# Vous devriez voir :
Starting development server at http://127.0.0.1:8000/
```

Si vous voyez des erreurs en rouge, **copiez-les et envoyez-les moi**.

---

### **Vérifier les logs du serveur**

Quand vous essayez de modifier le mot de passe, regardez le terminal backend.
Vous devriez voir quelque chose comme :

```bash
[31/Oct/2025 09:43:00] "PUT /api/auth/profile/update/ HTTP/1.1" 400 XX
```

**Copiez toutes les lignes qui apparaissent** quand vous cliquez sur "Enregistrer".

---

## 🐛 Causes Possibles

### **Cause 1 : Mot de passe actuel incorrect**
Vous entrez un mauvais mot de passe actuel.

**Solution** : Vérifiez que vous utilisez le bon mot de passe (celui avec lequel vous vous connectez).

---

### **Cause 2 : Validation du mot de passe**
Le nouveau mot de passe ne respecte pas les règles de validation.

**Règles Django par défaut** :
- Au moins 8 caractères
- Pas trop similaire aux autres informations
- Pas trop commun
- Pas entièrement numérique

**Solution** : Utilisez un mot de passe fort comme `Test123!@#`

---

### **Cause 3 : Champs vides non supprimés**
Le frontend envoie des champs vides qui ne sont pas correctement supprimés.

**Solution** : Déjà corrigée dans le code, mais vérifiez que le serveur a été redémarré.

---

### **Cause 4 : Problème de sérialisation**
Le sérialiseur ne gère pas correctement les données.

**Solution** : Vérifier les logs backend pour voir l'erreur exacte.

---

## 📸 Informations Nécessaires

Pour résoudre le problème, envoyez-moi :

### **1. Capture d'écran de la console**
- Développer "Détails de l'erreur: Object"
- Montrer ce qui est à l'intérieur

### **2. Capture d'écran du Network**
- Onglet **Payload** : Données envoyées
- Onglet **Response** : Réponse du serveur

### **3. Logs du terminal backend**
- Copier les lignes qui apparaissent quand vous cliquez sur "Enregistrer"

### **4. Répondre aux questions**
- Le changement de prénom seul fonctionne-t-il ?
- Quel est votre mot de passe actuel (pour que je puisse tester) ?
- Quel nouveau mot de passe essayez-vous de mettre ?

---

## 🚀 Actions Immédiates

### **1. Redémarrer le serveur backend**

```bash
cd "c:\Users\Miguel\Desktop\Applikcation Octobre\Gestion de Projet IT\backend"
# Arrêter (Ctrl+C)
python manage.py runserver
```

### **2. Vider le cache du navigateur**

```bash
Ctrl + Shift + Delete → Effacer tout
```

### **3. Tester avec un mot de passe simple**

Essayez de changer le mot de passe avec :
- Mot de passe actuel : [celui que vous utilisez pour vous connecter]
- Nouveau mot de passe : `TestPassword123!`
- Confirmer : `TestPassword123!`

---

## 📝 Checklist

- [ ] Serveur backend redémarré
- [ ] Cache navigateur vidé
- [ ] Console ouverte (F12)
- [ ] Network ouvert avec "Preserve log"
- [ ] Test modification prénom seul
- [ ] Test modification mot de passe
- [ ] Capture d'écran console (erreur détaillée)
- [ ] Capture d'écran Network (Payload + Response)
- [ ] Logs backend copiés

---

**Une fois que vous aurez ces informations, je pourrai identifier exactement le problème et le corriger ! 📸**
