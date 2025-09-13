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
| Pollution atmosphérique (PM10, NO₂, O₃)     | AirParif                          | [https://data-airparif-asso.opendata.arcgis.com](https://data-airparif-asso.opendata.arcgis.com) |
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

1. **Collecte et exploration des données**

   * Import pollution (CSV)
   * Import météo (CSV)

2. **Nettoyage et préparation**

   * Harmonisation des colonnes
   * Suppression des doublons et normalisation des valeurs
   * Traitement des valeurs manquantes (interpolation, suppression)
   * Jointure pollution ↔ météo sur date + localisation

3. **Analyse statistique**

   * Distribution des niveaux de pollution
   * Séries temporelles (pics de pollution, saisonnalité)
   * Corrélations météo ↔ pollution

4. **Cartographie avec GeoPandas**

   * Localisation des stations de mesure
   * Cartes choroplèthes par arrondissement/commune
   * Évolution spatio-temporelle

5. **Modélisation prédictive**

   * Variables explicatives : météo (T°, humidité, vent)
   * Variable cible : concentration en polluants
   * Modèle ML : Régression (RandomForestRegressor, XGBoost), Classification (RandomForestClassifier, Logistic Regression)
   * Validation croisée
   * Prédiction des pics de pollution

6. **Dashboard Power BI**

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
│   ├── 01_clean_data.py
│   ├── 02_analyse_statistique.py
│   ├── 03_cartographie.py
│   ├── 04_correlation_meteo.py
│   └── 05_modelisation_ml.py
├── exports/                # Données nettoyées et graphiques
├── dashboard/              # Fichier Power BI (.pbix)
├── images/                 # Cartes & visualisations générées
├── requirements.txt        # Dépendances Python
└── README.md               # Ce fichier
```

---
