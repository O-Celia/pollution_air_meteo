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

## Étapes du projet

### 1. **Collecte et exploration des données**

La première étape a consisté à rassembler des sources hétérogènes : <br>

Les mesures de pollution atmosphérique (AirParif) sont fournies station par station, avec une granularité horaire. <br>

Les données météorologiques (Météo Data Gouv) sont issues de plusieurs postes, avec des variables météorologiques différentes selon les fichiers, avec une granularité quotidienne. <br>

Un fichier a été créé, listant pour chaque station de suivi de pollution de AirParif le département associé. <br>

Plutôt que de travailler directement au niveau des stations, j’ai choisi d’agréger les données par département et par jour. Cela permet de réduire le bruit lié à la localisation précise des capteurs et de rendre les jeux de données météo et pollution comparables. <br>

### 2. **Nettoyage et préparation**


   * Suppression des doublons et normalisation des valeurs


Cette étape a été la plus technique, car les formats bruts différaient fortement.

- Harmonisation des colonnes :
   * Conversion des dates en format unique YYYY-MM-DD.
   * Uniformisation des polluants (NO₂, O₃, PM10, PM2.5).
   * Association des stations de suivi de la pollution atmosphérique avec les départements.
   * Extraction des départements du numéro des postes.

- Traitement des valeurs manquantes :
   * Suppression des lignes sans valeur de pollution.
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
   * Comparaison avec les tendances météo (ex. chaleur et absence de vent ↔ accumulation d’ozone).

- Corrélations :
   * Corrélations linéaires et visuelles entre météo et pollution (par ex. pluie ↔ baisse de particules, chaleur ↔ hausse d’ozone).
   * Utilisation des deux colonnes moyenne et médiane pour vérifier la robustesse des relations. <br>

Ces analyses servent de base pour la modélisation prédictive, en identifiant quelles variables météo expliquent le mieux la pollution.

### 4. **Cartographie avec GeoPandas**

   * Localisation des stations de mesure
   * Cartes choroplèthes par arrondissement/commune
   * Évolution spatio-temporelle

### 5. **Modélisation prédictive**

   * Variables explicatives : météo
        - Températures (tx, tn, tm) : chaleur favorise O₃.
        - Vent (ffm, fxy, dxy) : dispersion ou accumulation des polluants.
        - Précipitations (rr) : nettoyage de l’atmosphère.
        - Evotranspiration (etpgrille) : liée à l’ozone et particules.
   * Variable cible : concentration en polluants
   * Modèle ML : Régression (RandomForestRegressor, XGBoost) et classification (RandomForestClassifier, Logistic Regression)
   * Validation croisée
   * Prédiction des pics de pollution

### 6. **Dashboard Power BI**

   * Visualisation interactive par polluant, année, lieu
   * Évolution temporelle
   * Comparaison météo ↔ pollution
   * Zones à risque prédictives

---

## Structure du dépôt

```bash
pollution_air_meteo/
├── data/                   # Données brutes (CSV, API exports)
├── scripts/                # Scripts Python organisés par étape
│   ├── 01_meteo_clean.py
│   ├── 02_pollution_clean.py
│   ├── 03_analyse_statistique.py
│   ├── 04_cartographie.py
│   ├── 05_correlation_meteo.py
│   └── 06_modelisation_ml.py
├── exports/                # Données nettoyées et graphiques
│   ├── intermediaire
│   └── final
├── dashboard/              # Fichier Power BI (.pbix)
├── images/                 # Cartes & visualisations générées
├── requirements.txt        # Dépendances Python
└── README.md               # Ce fichier
```

---
