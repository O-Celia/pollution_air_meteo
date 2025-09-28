# Modélisation avec Random Forest

Ce script applique des modèles Random Forest pour :
1. Prédire les concentrations journalières des principaux polluants atmosphériques (régression).
2. Classer les zones en fonction du risque de pollution (classification binaire haut/bas risque).

Les prédictions et les résultats des test d'évaluation des modèles sont disponibles dans **exports/final**, tandis que les images produites sont disponibles dans **images/predictions**.

---

## Préparation des données

- Les données météo et pollution sont fusionnées par date et département.
- Création d’un **pivot table** pour obtenir les colonnes de polluants (`NO2`, `O3`, `PM10`, `PM2.5`).
- Suppression des valeurs manquantes (`dropna()`).
- Les variables explicatives sont constituées des indicateurs météorologiques :  
  - Température (min, max, moyenne)  
  - Précipitations  
  - Vent (moyen, max, direction)  
  - Évapotranspiration potentielle  

---

## Modélisation

### Régression
- Objectif : prédire la valeur moyenne quotidienne des polluants.
- Modèle utilisé : RandomForestRegressor (200 arbres, `random_state=42`).
- Évaluation avec RMSE et R².  
- Données séparées en train/test (80/20).  
- Mise à l’échelle des variables avec `StandardScaler`.

Résultats :

| Polluant | RMSE  | R²   |
|----------|-------|------|
| NO2      | 4.22  | 0.814 |
| O3       | 2.26  | 0.985 |
| PM10     | 4.33  | 0.714 |
| PM2.5    | 1.92  | 0.893 |

Très bonnes performances pour O3, et PM2.5, un peu plus de variabilité pour NO2 et PM10.

### Prédictions sur l’ensemble du dataset 
   - Objectif : produire des valeurs prédites pour toutes les dates et départements, pour générer les graphiques temporels et calculer les moyennes sur 2020‑2025.  
   - Même modèle (`RandomForestRegressor`) réentraîné sur toutes les données, pour obtenir des prédictions complètes.  
   - Ces prédictions sont utilisées pour :
     - Les scatterplots valeurs réelles vs prédites.
     - Les graphiques d’évolution temporelle (réel vs prédit).
     - Les moyennes par polluant et département et leur comparaison aux seuils OMS.

### Classification (médiane)
- Objectif : déterminer si une zone est en haut risque (valeur > médiane) ou bas risque.
- Modèle utilisé : RandomForestClassifier (200 arbres, `random_state=42`).
- Évaluation avec Accuracy et F1-score pondéré.
- Génération de matrices de confusion pour chaque polluant.

**Résultats :**

| Polluant | Accuracy | F1-score |
|----------|----------|----------|
| NO2      | 0.958    | 0.958 |
| O3       | 0.992    | 0.992 |
| PM10     | 0.913    | 0.913 |
| PM2.5    | 0.982    | 0.982 |

Le modèle de classification présente une excellente précision, particulièrement pour O3 et PM2.5.

### Classification (OMS)

- Objectif : détecter si une concentration dépasse ou non le seuil fixé par l’OMS (2021).  
- Seuils utilisés :  
  - NO₂ : 10 µg/m³  
  - O₃ : 60 µg/m³ (pic saisonnier, indicatif)  
  - PM10 : 15 µg/m³  
  - PM2.5 : 5 µg/m³  

- Modèle : RandomForestClassifier (200 arbres, `random_state=42`).
- Evaluation : accuracy et F1-score, plus matrices de confusion.

**Résultats :**

| Polluant | Accuracy | F1-score |
|----------|----------|----------|
| NO₂      | 0.951    | 0.949 |
| O₃       | 0.993    | 0.993 |
| PM10     | 0.921    | 0.920 |
| PM2.5    | 0.978    | 0.978 |

Le modèle de classification présente une excellent précision également, particulièrement pour O3 et OM2.5

L’utilisation des seuils de l’OMS comme référence permet d’évaluer directement la proportion de dépassements dans les données étudiées, indépendamment du modèle.

- NO₂ : la matrice de confusion montre un grand nombre de dépassements du seuil OMS.
- O₃ : les données révèlent une majorité de valeurs en dessous du seuil OMS.
- PM10 : les résultats montrent un nombre non négligeable de dépassements.
- PM2.5 : les dépassements sont très largement majoritaires.


---

## Comparaison des moyennes (2020 - 2025) avec les seuils OMS (2021)

| Polluant | Département | Moyenne réelle | Moyenne prédite | Seuil OMS 2021 | Interprétation |
|----------|------------|-----------------------|------------------------|----------------|----------------|
| NO₂      | 77         | 16.97                 | 17.19                  | 10 µg/m³       | Dépassement important, impact santé potentiel. |
| NO₂      | 78         | 12.52                 | 13.37                  | 10 µg/m³       | Dépassement important, impact santé potentiel. |
| NO₂      | 91         | 26.59                 | 25.79                  | 10 µg/m³       | Dépassement important, impact santé potentiel. |
| NO₂      | 95         | 19.29                 | 18.90                  | 10 µg/m³       | Dépassement important, impact santé potentiel. |
| O₃       | 77         | 52.43                 | 52.52                  | 60 µg/m³ (pic saisonnier) | Bon respect du seuil annuel, vigilance sur épisodes ponctuels. |
| O₃       | 78         | 54.05                 | 54.06                  | 60 µg/m³ (pic saisonnier)      | Bon respect du seuil annuel, vigilance sur épisodes ponctuels. |
| O₃       | 91         | 54.78                 | 54.67                  | 60 µg/m³ (pic saisonnier)      | Moyenne proche du seuil, possible dépassement saisonnier. |
| O₃       | 95         | 57.99                 | 57.90                  | 60 µg/m³ (pic saisonnier)      | Moyenne proche du seuil, possible dépassement saisonnier. |
| PM10     | 77         | 18.57                 | 17.71                  | 15 µg/m³       | Dépassement important, impact santé potentiel. |
| PM10     | 78         | 13.13                 | 13.43                  | 15 µg/m³       | Moyenne proche du seuil, vigilance sur pics journaliers. |
| PM10     | 91         | 12.49                 | 13.14                  | 15 µg/m³       | Moyenne proche du seuil, vigilance sur pics journaliers. |
| PM10     | 95         | 14.28                 | 14.43                  | 15 µg/m³       | Moyenne proche du seuil, surveillance nécessaire. |
| PM2.5    | 77         | 8.58                  | 8.60                   | 5 µg/m³        | Dépassement important, impact santé potentiel. |
| PM2.5    | 78         | 8.33                  | 8.43                   | 5 µg/m³        | Dépassement important, impact santé potentiel. |
| PM2.5    | 91         | 9.23                  | 9.28                   | 5 µg/m³        | Dépassement important, impact santé potentiel. |
| PM2.5    | 95         | 8.86                  | 8.86                   | 5 µg/m³        | Dépassement important, impact santé potentiel. |

---

## Conclusion

- Les modèles Random Forest se montrent adaptés pour la prédiction et la classification des zones à risque de pollution.  
- L’approche permet de :
  - Obtenir une bonne précision prédictive pour la plupart des polluants.
  - Identifier clairement les zones à haut risque, ce qui est utile pour la prévention sanitaire et la gestion environnementale.  

Sur le plan environnemental, les résultats montrent que :  
- Les moyennes réelles et prédites sont très proches pour l’ensemble des polluants, ce qui confirme la robustesse du modèle.  
- Les écarts sont particulièrement faibles pour O₃ et PM2.5, ce qui souligne l’importance du rôle de la météo dans la formation et la dispersion de ces polluants.  
- Les différences observées par département et par année révèlent des dynamiques locales : par exemple, le NO₂ et le PM10 présentent plus de variabilité interannuelle, traduisant une influence des émissions locales (trafic routier, chauffage, industrie par exemple) au-delà des seules conditions météorologiques.  
- La stabilité des prédictions pour l’ozone (O₃) reflète le fait que ce polluant secondaire est fortement conditionné par les paramètres météorologiques (ensoleillement, température), plutôt que par des émissions directes.

Sur le plan de la santé :
- Concernant le NO₂ et PM2.5, les niveaux moyens (≈19 µg/m³ et ≈9 µg/m³ respectivement, selon les départements et années) restent au-dessus de la valeur guide de l’OMS pour l’exposition annuelle (10 µg/m³ et 5 µg/m³). Ces polluants, liés majoritairement au trafic routier et au chauffage urbain, restent donc préoccupant en termes de santé publique, en particulier dans les zones urbaines denses.
- À l’inverse, les valeurs moyennes de PM10 (≈14,7 µg/m³) se situent légèrement en dessous du seuil OMS pour l'exposition annuelle (15 µg/m³), mais à la limite de la recommandation. Elles montrent que de faibles hausses pourraient entraîner un dépassement, surtout lors d’épisodes de pollution locaux (trafic, chauffage, poussières).  
- Pour l’ozone (O₃), les concentrations moyennes (≈55 µg/m³) restent sous le seuil OMS pour l’exposition à long terme (100 µg/m³ en 8h), mais il convient de noter que des pics journaliers estivaux peuvent ponctuellement dépasser les recommandations.  

Globalement, l’utilisation de ces modèles permet donc non seulement d’anticiper les pics de pollution, mais aussi de mieux comprendre la part de la variabilité attribuable à la météo par rapport aux sources locales. Cela ouvre des perspectives en matière de gestion environnementale.
