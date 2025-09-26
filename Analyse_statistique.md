# Analyse statistique

## Objectif

L’objectif de ce travail est d’étudier les liens entre les concentrations de polluants atmosphériques et les variables météorologiques (température, vent, pluie, évapotranspiration…) à partir de données collectées en Île-de-France.
L’analyse repose sur plusieurs méthodes statistiques et graphiques, afin de :

- Explorer les distributions et valeurs extrêmes (outliers).
- Étudier les relations entre polluants et météo (régressions, corrélations).
- Identifier des dépendances et interactions entre polluants.
- Mettre en évidence les principaux déterminants météorologiques de la pollution.

Les polluants étudiés sont :
- **NO₂** (dioxyde d’azote),
- **O₃** (ozone troposphérique),
- **PM10** (particules ≤ 10 µm),
- **PM2.5** (particules ≤ 2.5 µm).

---

## Étapes de l’analyse

### 1. Préparation des données

- Fusion des données polluants et météo par date et département.
- Création de jeux de données pivotés pour faciliter les calculs de corrélations.
- Nettoyage et homogénéisation (ex : remplacement PM25 par PM2.5).

### 2. Analyse descriptive

**Méthodes utilisées :**
- Statistiques de base (moyenne, médiane, min, max, écart-type).
- Calcul du pourcentage d’outliers via l’IQR (valeurs hors de [Q1 - 1.5×IQR ; Q3 + 1.5×IQR]).
- Visualisation des distributions avec boxplots et histogrammes dans **images/météo** et **images/polluants**.

**Résultats :**

Polluants
- NO2 : pollution chronique modérée, données assez stables, valeurs extrêmes limitées (moy 19 µg/m³, max 63 µg/m³, 2.6% d’outliers).
- O3 : reflète la forte variabilité de l’ozone (épisodes estivaux), moyenne plus élevée (55 µg/m³) mais pics importants, avec 1.7% d’outliers mais certains très bas (1,23 µg/m³) et très hauts (124 µg/m³).
- PM10 : pics plus fréquents, moyenne 15 µg/m³, max 64 µg/m³, mais 3.9% d’outliers. La plupart du temps bas, mais épisodes de pollution marqués.
- PM2.5 : polluant le plus instable, moyenne 9 µg/m³, max 49 µg/m³, variabilité forte, 6.5% d’outliers. Plus bas que PM10, mais beaucoup d’outliers, ce qui traduit des épisodes d’accumulation.

Météo :
- Pluie (rr_mean) = distribution très asymétrique (13% d’outliers), mais la pluie est très asymétrique : la plupart du temps 0, mais parfois des averses intenses.
- Températures(tn, tx, tm) = distributions régulières, pratiquement pas d'outliers.
- Vent (ffm_mean et fxy_mean) = valeurs extrêmes ponctuelles, avec 2/3% d'outliers : quelques épisodes de vent fort, mais globalement régulier.
- Evapotranspiration (etpgrille) = très peu d’outliers, valeurs élevées liées aux journées chaudes et ensoleillées.

### 3. Relations polluants / météo

**Méthodes utilisées :**
- Pour chaque couple (polluant, variable météo), ajustement d’un modèle de régression linéaire : **y=α+βX+ϵ**, avec estimation de la pente (β), de l’ordonnée à l’origine (α) et du coefficient de détermination (R²).
- Ajout d’une droite de régression sur les nuages de points.
Les graphiques sont disponibles dans **images/correlation**.

**Résultats :**
- NO2 : relations négatives avec T (R²=0.0.145) et vent (R²=0.188). 
- O3 : Très fortes corrélations positives avec évapotranspiration (R²=0.473), température max (R²=0.288) et moyenne (R²=0.269). 
- PM10 : aucune relation nette. R² < 0.1 pour toutes les variables.
- PM2.5 : dépendance modérée avec les températures (R²=0.225 pour Tmin, 0.157 pour Tm).

**Interprétation :**
- O3 dépend fortement de la chaleur et du rayonnement solaire (mécanisme photochimique).
- NO2 se dilue avec vent/températures élevées. Effet clair mais faible à modéré. La météo explique au mieux 19% de la variabilité du NO2.
- PM10/PM2.5 reflètent davantage les sources locales qu’une influence météo directe. Pour PM10 : Légère sensibilité au vent et aux précipitations, mais rien de majeur. Pour PM2.5 : Légère influence du vent et de la pluie.

### 4. Corrélations croisées

**Méthodes utilisées :**
- Corrélations réduites entre polluants et météo (heatmap).
- Corrélations complètes entre toutes les variables (polluants + météo).
Les graphiques sont disponibles dans **images/correlation**.

**Résultats principaux :**
- NO2 : corrélations négatives avec T et vent (-0.3 à -0.4).
- O3 : corrélations positives avec Tx, Tm, ETP (0.3 à 0.5).
- PM10 & PM2.5 : forte corrélation mutuelle (0.80), mais souvent négatives avec température et vent.

**Interprétation :**
- Météo = facteur déterminant pour O3.
- NO2 = sensible à la dispersion.
- PM10/PM2.5 = pollution de fond urbaine, moins météo-dépendante.

### 5. Évolution temporelle

**Méthodes utilisées :**
- Calcul des moyennes quotidiennes par polluant.
- Séries temporelles sur toute la période étudiée.
Les graphiques sont disponibles dans **images/polluants**.

**Résultats :**
- O3 = forte saisonnalité, pics estivaux (chaleur/soleil).
- NO2 = valeurs plus stables, tendance urbaine (trafic).
- PM10/PM2.5 = pics ponctuels liés à épisodes particuliers.

---

## Synthèse générale

| Polluant |	Dépendance météo |	Variables clés |	R² max |	Corrélations notables |
|-------------|-------------|-------------|-------------|-------------|
NO2	| Modérée |	T°, vent |	0.19 |	Corr négative T°, vent |
O3 |	Forte |	Tx, Tm, ETP |	0.47 |	Corr positive T°, ETP |
PM10 |	Faible |	– |	<0.1 |	Corr forte avec PM2.5 |
PM2.5 |	Modérée |	Tmin, Tm, vent |	0.22 |	Corr forte avec PM10 |

---

## Conclusion

- L’ozone (O3) est le polluant le plus dépendant de la météo (soleil, chaleur, photochimie). Faible lien avec pluie ou direction du vent.
- Le NO2 est influencé par la dispersion (vent, chaleur) et la dilution par la météo, qui le réduit, mais de façon plus modérée.
- Les particules fines (PM10/PM2.5) dépendent moins des conditions météo : les PM10 dépendent probablement davantage des émissions locales (trafic, chauffage, chantiers) que des conditions météo seules; effet météo plus marqué pour PM2.5, probablement lié à leur capacité à s’accumuler dans des conditions de stagnation atmosphérique.
- Les relations entre polluants (NO2/O3, PM10/PM2.5) sont cohérentes avec leurs mécanismes chimiques ou sources communes.