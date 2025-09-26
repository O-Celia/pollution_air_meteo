# Analyse spatio-temporelle

## Présentation
Cette partie du projet se concentre sur l’étude de la pollution atmosphérique en Île-de-France à travers :
- Des cartes choroplèthes par département,
- Une évolution mensuelle et annuelle des concentrations,
- Une analyse des patterns saisonniers en lien avec la météo.

Les polluants étudiés sont :
- **NO₂** (dioxyde d’azote),
- **O₃** (ozone troposphérique),
- **PM10** (particules ≤ 10 µm),
- **PM2.5** (particules ≤ 2.5 µm).

Les cartes sont visibles dans **images/cartes**

---

## Résultats cartographiques

### 1. Vue annuelle (2020-2024)
- NO₂ : plus élevé dans le 91 (26.6 µg/m³) car zones urbaines à fort trafic.
- O₃ : plus élevé dans le 95 (58 µg/m³) car polluant secondaire, typique des zones périurbaines/rurales.
- PM10 & PM2.5 : relativement homogènes (PM10 ~13-18, PM2.5 ~8-9), légèrement plus hauts dans le 91 et 95.

**Conclusion annuelle** :
- NO₂ : trafic routier et urbanisation.
- O₃ : formation secondaire, davantage en zones moins denses.
- Particules : homogènes mais influencées par chauffage et conditions météo.

### 2. Vue mensuelle (exemple département 77)
- **NO₂** :
  - Haut en hiver (janvier, février, décembre).
  - Bas en été (juillet-août).
  - Exemple : janvier 2021 ~23 µg/m³ vs août 2021 ~12 µg/m³.

- **O₃** :
  - Haut en été/printemps (mai-juillet).
  - Bas en hiver.
  - Exemple : juin 2023 ~78 µg/m³ vs décembre 2023 ~30 µg/m³.

- **PM10/PM2.5** :
  - Plus irréguliers, mais pics fréquents en hiver/printemps.
  - Exemple : PM2.5 janvier 2022 ~13.3 µg/m³, mars 2022 ~18.4 µg/m³.

**Conclusion mensuelle** :
- NO₂ : trafic + chauffage en hiver.
- O₃ : ensoleillement + photolyse en été.
- PM : chauffage résidentiel + conditions météorologiques (stagnation, vent faible).

---

## Synthèse

- Les analyses confirment les patterns classiques de pollution atmosphérique :  
  - NO₂ : pics en hiver, urbain/traﬁc.
  - O₃ : pics en été, zones périurbaines.
  - Particules : pics irréguliers, souvent liés au chauffage ou événements particuliers.
- La météo joue un rôle majeur : froid, ensoleillement, vent et pression influencent directement les niveaux de pollution.
