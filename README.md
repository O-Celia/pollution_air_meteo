# Pollution de l’air et météo en France

## Analyse croisée : qualité de l’air et conditions météorologiques

### Cas d’étude : Région Île-de-France

---

## Objectifs du projet

Ce projet vise à analyser l’impact des conditions météorologiques (température, humidité, vent) sur la pollution de l’air (particules fines, NO₂, O₃).
Il s’appuie sur un cas d’étude en Île-de-France, région fortement concernée par les pics de pollution atmosphérique.

Les objectifs principaux sont :

* Identifier les **zones et périodes les plus polluées**
* Analyser l’**évolution temporelle** de la pollution
* Étudier les **corrélations** entre météo et pollution
* Localiser les **zones à risques** pour la santé publique
* Construire un **modèle prédictif** de pollution basé sur la météo
* Créer un **dashboard interactif** via Power BI

---

## Données utilisées

| Domaine                                     | Source                            | Lien                                                                                                                              |
| ------------------------------------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Pollution atmosphérique (PM10, PM2.5, NO₂, O₃)     | AirParif                          |[https://data-airparif-asso.opendata.arcgis.com](https://data-airparif-asso.opendata.arcgis.com) |
| Données météo (température, humidité, vent) | Météo Data Gouv                   | [https://meteo.data.gouv.fr/](https://meteo.data.gouv.fr/)                                                                  |
| Données géographiques                       | IGN / OpenStreetMap               | [https://www.geoportail.gouv.fr](https://www.geoportail.gouv.fr) / [https://www.openstreetmap.org](https://www.openstreetmap.org) |

---

## Outils techniques

* **Langage** : Python 3.11
* **Librairies** : `pandas`, `geopandas`, `matplotlib`, `seaborn`, `scikit-learn`
* **Visualisation** : Power BI
* **IDE** : VSCode

---

## Structure du dépôt

```bash
pollution_air_meteo/
├── data/                   # Données brutes (CSV, shapefiles)
├── scripts/                # Scripts Python organisés par étape
│   ├── 01_meteo_clean.py
│   ├── 02_pollution_clean.py
│   ├── 03_analyse_statistique.py
│   ├── 04_cartographie.py
│   ├── 05_performances_modeles.py
│   ├── 06_modelisation_classification.py
│   └── 07_random_forest.py
├── explication_resultats/  # Explication des résultats des scripts
│   ├── 01_Analyse_statistique
│   ├── 02_Cartographie
│   ├── 03_Performances_modeles
│   ├── 04_Classification
│   └── 05_Random_Forest
├── exports/                # Données nettoyées et graphiques
│   ├── intermediaire
│   └── final
├── dashboard/              # Fichier Power BI (.pbix)
├── images/                 # Cartes & visualisations générées
│   ├── cartes
│   ├── correlation
│   ├── meteo
│   ├── polluants
│   └── predictions
├── requirements.txt        # Dépendances Python
└── README.md               # Ce fichier
```

---

## Étapes du projet

### 1. **Collecte et exploration des données**

La première étape a consisté à rassembler des sources hétérogènes : <br>

Les mesures de pollution atmosphérique (AirParif) sont fournies station par station, avec une granularité horaire. <br>

Les données météorologiques (Météo Data Gouv) sont issues de plusieurs postes, avec des variables météorologiques différentes selon les fichiers, avec une granularité quotidienne. <br>

Un fichier a été créé, listant pour chaque station de suivi de pollution de AirParif le département associé. <br>

Plutôt que de travailler directement au niveau des stations, j’ai choisi d’agréger les données par département et par jour. Cela permet de réduire le bruit lié à la localisation précise des capteurs et de rendre les jeux de données météo et pollution comparables. <br>

### 2. **Nettoyage et préparation**

Cette étape a été la plus technique, car les formats bruts différaient fortement.

- Harmonisation des colonnes :
   * Conversion des dates en format unique YYYY-MM-DD.
   * Uniformisation des polluants (NO₂, O₃, PM10, PM2.5).
   * Association des stations de suivi de la pollution atmosphérique avec les départements.
   * Extraction des départements du numéro des postes.

- Traitement des valeurs manquantes et doublons:
   * Suppression des lignes sans valeur de pollution.
   * Suppression des doublons
   * Pour la météo, suppression des lignes incomplètes sur les variables principales afin de garder un dataset robuste.

- Agrégation par département :
   * Calcul de la moyenne et de la médiane des mesures pour chaque couple (date, département, polluant) : la moyenne capture la tendance générale, mais elle est sensible aux valeurs extrêmes. La médiane permet de mieux contrôler l’impact d’éventuelles stations anormales.
   * Ajout d’une colonne nb_station_* pour conserver la trace du nombre de capteurs disponibles dans l’agrégation (important pour juger de la fiabilité des mesure).

Ces choix permettent d’avoir un jeu de données homogène, comparable et robuste aux anomalies locales.

### 3. **Analyse statistique**

Une fois les données nettoyées, j’ai réalisé plusieurs analyses :

- Distributions et boxplots :
   * Par polluant et par département pour identifier les zones les plus touchées et repérer des valeurs extrêmes.
   * Par variables météo pour détecter des anomalies (par ex. valeurs aberrantes de température ou vent).
   * Choix de de conserver les valeurs extrêmes (outliers) car elles correspondent généralement à de vrais épisodes de pollution ou d’événements météo intenses (pics d’ozone en été, particules en hiver, pluies orageuses, tempêtes, etc.).

- Séries temporelles :
   * Évolution des polluants au fil des jours (pics saisonniers de NO₂ en hiver, O₃ en été, etc.).
   * Comparaison avec les tendances météo (ex. chaleur et absence de vent = accumulation d’ozone).

- Corrélations :
   * Corrélations linéaires et visuelles entre météo et pollution (par ex. pluie = baisse de particules, chaleur = hausse d’ozone).
   * Utilisation des deux colonnes moyenne et médiane pour vérifier la robustesse des relations.

- Régressions temporelles :
   * Ajustement de modèles linéaires simples (2020–2025) pour détecter des tendances globales par polluant.
   * Identification des périodes les plus polluées (top 5 mois par polluant) et du département le plus pollué en moyenne pour chaque polluant.

Ces analyses servent de base pour la modélisation prédictive, en identifiant quelles variables météo expliquent le mieux la pollution.

### 4. **Cartographie avec GeoPandas**

   * Localisation des stations de mesure
   * Cartes choroplèthes par arrondissement/commune
   * Évolution spatio-temporelle

Afin d’intégrer une dimension spatiale à l’analyse, j’ai utilisé GeoPandas pour représenter les polluants sur des cartes de la France métropolitaine au niveau départemental.

- Choroplèthes annuels :
   * Fusion entre les moyennes annuelles de concentration par département et les polygones issus du shapefile administratif.
   * Cartes produites pour chaque polluant (NO₂, O₃, PM10, PM2.5), permettant d’identifier visuellement les zones les plus exposées.
   * Mise en évidence des contrastes géographiques (départements plus urbains plus touchées par le NO₂, sud exposé à l’ozone, etc.).

- Évolution spatio-temporelle mensuelle :
   * Calcul des moyennes mensuelles par département.
   * Génération de cartes mensuelles permettant de suivre l’évolution saisonnière des polluants.
   * Standardisation des échelles de couleur (valeur minimum / valeur maximum constants) afin de garantir la comparabilité entre mois.

Ces visualisations permettent de relier les pics temporels observés à des dynamiques régionales (par ex. pics d’ozone récurrents dans le sud en été, concentrations de particules dans le nord en hiver).

### 5. **Performances des modèles**

Après la phase d’exploration et de cartographie, j’ai évalué différents modèles de régression et de classification afin de prédire les concentrations de polluants ou de détecter des dépassements de seuils.

- Jeux de données :
   * Données météo + concentrations moyennes de polluants par département et par jour.
   * Découpage aléatoire 80 % train / 20 % test.

- Régression (prédiction des concentrations) :
   * Objectif : estimer les valeurs réelles des polluants à partir des variables météo.
   * Modèles testés : Random Forest Regressor et XGBoost Regressor.
   * Métriques utilisées :
      - MAE (erreur absolue moyenne, en µg/m³)
      - RMSE (racine de l’erreur quadratique moyenne)
      - R² (coefficient de détermination).

- Classification (dépassement de seuils OMS) :
   * Objectif : détecter automatiquement si un seuil est dépassé.
   * Seuils simplifiés utilisés (µg/m³) :
      - NO₂ : 25
      - O₃ : 100
      - PM10 : 45
      - PM2.5 : 15
   * Modèles testés :
      - Régression logistique (avec standardisation des variables)
      - Random Forest Classifier
      - XGBoost Classifier
   * Métriques utilisées :
      - Accuracy (précision globale)  
      - F1-score (équilibre entre précision et rappel, adapté aux classes déséquilibrées).

Cette étape permet de sélectionner les modèles les plus robustes pour chaque polluant, en fonction des variables météo disponibles, et d’orienter les analyses suivantes.

### 6. **Test des modèles de classification**

Après les tests de régression et de classification sur la base des seuils OMS, une deuxième approche a été réalisée afin d’évaluer la capacité des modèles à distinguer des niveaux relatifs de pollution (au-dessus ou en dessous de la médiane des concentrations observées).

- Préparation des données :
   * Les concentrations des polluants ont été pivotées par date et département.
   * Les variables météo ont été fusionnées pour constituer l’ensemble explicatif.
   * Pour chaque polluant (NO₂, O₃, PM10, PM2.5), une cible binaire a été construite :
     - `1` = concentration au-dessus de la médiane
     - `0` = concentration au-dessous ou égale à la médiane

- Découpage et équilibrage :
   * Découpage 80 % train / 20 % test avec mélange aléatoire.  
   * Application de SMOTE pour équilibrer les classes dans l’ensemble d’entraînement.
   * Mise à l’échelle des variables par standardisation.

- Modèles évalués :
   * Régression logistique
   * Random Forest Classifier (200 arbres)
   * XGBoost Classifier

- Métriques utilisées :
   * Accuracy (précision globale)
   * Précision (moyenne pondérée)
   * Rappel (moyenne pondérée)
   * F1-score (moyenne pondérée)

Cette étape permet de comparer la performance relative des modèles de classification sur une catégorisation relative des niveaux de pollution, pour évaluer leur robustesse.

### 7. **Prédictions Random Forest : régression et classification**

J’ai choisi d'utiliser un Random Forest à la fois pour la régression (prédiction des concentrations) et pour la classification (zones à risque).

#### a. Régression : prédiction des concentrations
- Préparation des données :
   * Les données météo servent de variables explicatives.
   * Les cibles sont les concentrations de chaque polluant (NO₂, O₃, PM10, PM2.5).
   * Découpage 80 % / 20 % avec standardisation des variables.

- Évaluation :
   * RMSE et R² calculés sur le jeu de test.

- Visualisations :
   * Scatter plots valeurs réelles vs prédites sur le jeu de test.
   * Scatter plots avec prédictions sur l’ensemble du dataset.
   * Courbes temporelles montrant l’évolution des concentrations réelles et prédites pour chaque polluant.

- Prédictions sur tout le jeu de données :
   * Les concentrations réelles et prédites sont sauvegardées.
   * Calcul des moyennes globales par polluant et des moyennes par département pour comparer les tendances spatiales.

---

#### b. Classification : détection des zones à risque
Deux approches ont été mises en œuvre :

1. Classification par rapport à la médiane des concentrations
   - Objectif : tester la capacité du modèle à distinguer des situations de pollution relative (haut/bas risque).
   - Avantage : équilibre des classes, utile pour valider le fonctionnement du modèle.
   - Méthodologie :
      * Découpage aléatoire 80 % / 20 %.
      * Standardisation des variables météo.
      * Entraînement d’un Random Forest Classifier (200 arbres).
   - Évaluation :
      * Accuracy et F1-score pour chaque polluant.
      * Rapports de classification et matrices de confusion sauvegardés.

2. Classification par rapport aux seuils de l’OMS (2021)
   - Objectif : évaluer directement la capacité du modèle à identifier les dépassements par rapport aux recommandations sanitaires.
   - Méthodologie, évaluation et résultats identiques.

Cette double approche permet à la fois de valider le modèle (médiane, équilibre statistique) et de tirer des conclusions environnementales et sanitaires (OMS). 

### 8. **Dashboard Power BI**

   * Visualisation interactive par polluant, année, lieu
   * Évolution temporelle
   * Comparaison météo / pollution
   * Zones à risque prédictives

## Conclusion

L’analyse menée met en évidence plusieurs points clés sur la pollution atmosphérique entre 2020 et 2025 :
- **Zones et périodes les plus polluées** : 
Parmi les départements étudiés, certains se distinguent selon le polluant dominant :
   - l’Essonne pour le dioxyde d’azote (NO₂) et les particules fines (PM2.5),
   - le Val-d’Oise pour l’ozone (O₃),
   - la Seine-et-Marne pour les particules inhalables (PM10).
Les polluants liés au trafic et au chauffage (NO₂, PM10, PM2.5) connaissent leurs pics en hiver et au début du printemps, tandis que l’ozone, polluant secondaire formé par réaction photochimique, atteint ses maximums en été.
- **Évolution temporelle** : 
on observe une tendance générale à la baisse pour la plupart des polluants, bien que celle-ci reste faible et masquée par des variations saisonnières importantes. Les dépassements du seuil sanitaire de l'OMS restent récurrents pour le NO₂ et le PM2.5.
- **Rôle de la météo** : 
   - la formation de l’ozone est fortement influencée par les conditions météorologiques (ensoleillement, chaleur),
   - la dispersion des polluants comme le NO₂ dépend du vent et de la température,
   - les particules (PM10, PM2.5) reflètent à la fois les conditions atmosphériques et les sources locales d’émissions.
- **Zones à risques sanitaires** : 
Les concentrations moyennes de NO₂ et de PM2.5 dépassent régulièrement les recommandations de l’OMS, ce qui représente un risque pour la santé. Les PM10 restent proches du seuil et doivent être surveillées, tandis que l’ozone, bien qu’en moyenne inférieur aux recommandations, peut générer des épisodes ponctuels dangereux lors des périodes estivales.
- **Modélisation prédictive** : 
Les modèles Random Forest appliqués aux données permettent de prédire efficacement l’ozone et les particules fines (PM2.5) à partir des données météo, et d’identifier les zones et périodes à risque. Pour NO₂ et PM10, l’ajout d’informations sur le trafic et les activités humaines permettrait d’améliorer la précision.

En résumé, la pollution de l’air reste un enjeu majeur :
- **NO₂** et **PM2.5** constituent les principaux risques chroniques,
- **O₃** représente un danger lors d’épisodes estivaux,
- **PM10** demande une vigilance particulière en période hivernale et printanière.

Ces résultats soulignent l’importance de la surveillance locale, de l’intégration des données d’émissions, et de la prise en compte des conditions météorologiques pour anticiper et gérer les épisodes de pollution.