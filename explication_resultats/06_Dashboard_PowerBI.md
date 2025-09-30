### 8. **Dashboard Power BI**

Un dashboard interactif sous Power BI a été créé, destiné à explorer les données et mettre en valeur les résultats des analyses et des modèles prédictifs.

#### a. Préparation des données
Après l’import de la table `meteo_pollution`, obtenue lors des analyses statistiques, dans Power BI, plusieurs traitements ont été effectués :
- Normalisation des formats numériques : transformation des séparateurs `.` en `,`, passage en nombres décimaux ou entiers selon le cas, standardisation des formats de dates.  
- Création de tables et colonnes en DAX :
  * Table `Datum` pour gérer le temps.  
  * Colonne `Seuil_OMS` dans la table `meteo_pollution` (en fonction du polluant).  
  * Colonne `Dépassement` (1 si dépassement du seuil, 0 sinon).  
  * Mesures :  
     - `% de dépassement` (proportion de jours dépassant le seuil),  
     - `AirQualitéScore` (1 – % de dépassement),  
     - `Nombre d’années de dépassement` pour chaque polluant.  
  * Table `Paramètre X` pour créer un slicer dynamique permettant de choisir la variable météo à afficher.  

- Import et transformations complémentaires :
  * Corrélations (fichier issu de l’analyse statistique).  
  * Prédictions (concentrations réelles et prédites).  
  * Résultats des modèles de régression et classification.  

#### b. Pages et visualisations du dashboard

1. **Accueil**  
Objectif : fournir une vue synthétique et rapide de la qualité de l’air.  
- KPI cards : concentrations annuelles moyennes (NO₂, O₃, PM10, PM2.5).  
- Bar chart : % de dépassement des seuils OMS par polluant.  
- Carte départementale : indicateur global de qualité de l’air.  
- Filtres : année, département.  

2. **Analyse spatio-temporelle**  
Objectif : identifier les zones et périodes les plus polluées.  
- Heatmap (X = mois, Y = polluant) pour mettre en évidence les pics saisonniers.  
- Timeline interactive : évolution temporelle des polluants.  
- Bar chart empilé : concentrations moyennes par département.  
- Filtres : polluant, année, département.  

3. **Dépassements des seuils sanitaires**  
Objectif : rendre visibles les dépassements par rapport aux recommandations de l’OMS.  
- KPI : nombre d’années avec dépassement par polluant.  
- Graphiques en barres pour chaque polluant : concentration moyenne par département vs seuil OMS.  
- Courbe temporelle : évolution du % annuel de dépassement.  
- Filtres : polluant, année.  

4. **Corrélations météo-pollution**  
Objectif : explorer le lien entre conditions météorologiques et pollution.  
- Scatterplots interactifs : concentration du polluant en fonction d’une variable météo.  
- Heatmap des coefficients de corrélation (polluants vs variables météo).  
- Slicers : choix du polluant et de la variable météo.  

5. **Prédictions et classification (Random Forest)**  
Objectif : illustrer les performances des modèles prédictifs.  
- Scatterplot : valeurs réelles vs valeurs prédites par polluant.  
- Graphiques temporels : évolution réelle vs prédite.  
- KPI :  
  * Régression = R² et RMSE par polluant.  
  * Classification = Accuracy et F1-score par polluant.  
- Filtres : année, département, polluant.  

#### c. Apports du dashboard
Ce dashboard offre une vision complète et interactive :
- Suivi global de la qualité de l’air et de son évolution.  
- Identification des zones et périodes à risque.  
- Analyse du rôle de la météo dans les épisodes de pollution.  
- Validation et interprétation des performances des modèles prédictifs.  
