# Exploration des performances des modèles

## 1. Objectif
L’objectif de cette étape est d’évaluer plusieurs modèles sur la capacité des variables météorologiques à expliquer et prédire les niveaux de pollution atmosphérique en Île-de-France.  
Deux approches ont été testées :
- **Régression** : prédire la concentration moyenne journalière des polluants.  
- **Classification** : prédire si un seuil de concentration fixé par l’OMS est dépassé ou non.  

Polluants étudiés : NO₂, O₃, PM10, PM2.5
Variables explicatives : températures (min, max, moyenne), vent (vitesse/direction), précipitations, évapotranspiration potentielle, etc.

Les résultats sont disponibles dans **exports/final/resultats_modelisation.csv**

---

## 2. Méthodologie
### Régression
- Algorithmes testés :  
  - `RandomForestRegressor`  
  - `XGBoostRegressor`  
- Évaluation : **MAE**, **RMSE**, **R²**  

### Classification
- Seuils OMS :  
  - NO₂ : 25 µg/m³  
  - O₃ : 100 µg/m³  
  - PM10 : 45 µg/m³  
  - PM2.5 : 15 µg/m³  
- Algorithmes testés :  
  - `LogisticRegression`  
  - `RandomForestClassifier`  
  - `XGBoostClassifier`  
- Évaluation : **Accuracy**, **F1-score**

---

## 3. Résultats

### Régression
| Polluant | Modèle        | MAE   | RMSE  | R²    | Interprétation |
|----------|--------------|-------|-------|-------|----------------|
| NO₂  | RF : 5.63<br>XGB : 5.18 | ~7.3 | ~6.8 | 0.44–0.51 | Pouvoir explicatif moyen : la météo explique partiellement, mais le trafic reste dominant. |
| O₃   | RF : 6.19<br>XGB : 6.28 | ~8.2 | ~8.2 | 0.80-0.81 | Très bon pouvoir explicatif : O₃ est fortement corrélé à la météo (ensoleillement, température). |
| PM10 | RF : 4.51<br>XGB : 4.38 | ~6.3 | ~6.1 | 0.41-0.45 | Explication modérée : une partie liée à la météo, mais autres sources (chauffage, poussières, industrie) importantes. |
| PM2.5| RF : 2.61<br>XGB : 2.67 | ~3.9 | ~3.9 | 0.56–0.58 | Bon niveau d’explication : météo + autres sources (trafic, combustion). |

O₃ est le polluant le mieux prédit par la météo (R² ~0.7).  
Les particules (PM10, PM2.5) et le NO₂ montrent une dépendance plus forte aux émissions locales (trafic, chauffage) qu’aux conditions atmosphériques. 

### Classification
| Polluant | Modèle        | Accuracy | F1-score | Interprétation |
|----------|--------------|----------|----------|----------------|
| NO₂  | RF, XGB, LR  | ~0.82–0.83    | 0.50–0.55 | Bon compromis, détection correcte des dépassements OMS. |
| O₃   | RF, XGB, LR  | ~0.99    | 0.17–0.36 | Détection faible, dépassements rares : problème de classes déséquilibrées. |
| PM10 | RF, XGB, LR  | ~0.99    | 0.00–0.12 | Très mauvais : quasiment aucun dépassement détecté. |
| PM2.5| RF, XGB, LR  | ~0.92    | 0.56–0.63 | Bonne détection des dépassements. |

La classification n’est pas totalement inutile : 
- PM2.5 et NO₂ : F1-score corrects, donc détection partielle des dépassements.
- O₃ et PM10 : F1 très faible (dépassements rares, classes très déséquilibrées).
Il faudrait tenter un rééquilibrage des classes (oversampling, SMOTE, etc.).  

---

## 4. Conclusion
- **Ozone (O₃)** : la météo explique une grande partie de ses variations = bon candidat pour la modélisation prédictive.  
- **NO₂** : pouvoir explicatif moyen, mais classification correcte des dépassements. Peut nécessiter des données supplémentaires (trafic, chauffage, industrie).  
- **PM10** : résultats mitigés = dépend trop de sources non météorologiques (chauffage, poussières)
- **PM2.5** : régression correcte et bonne performance en classification.
- **Classification** : correct, mais il y a un problème de déséquilibre des classes pour PM10 et O₃.  

Pour la suite, je vais retester uniquement les modèles de classification avec des techniques de rééquilibrage des classes :
- Les modèles de régression ont déjà montré leurs limites : on atteint un plafond de performance avec les seules variables météo.
- La classification souffre surtout d’un déséquilibre des données. C’est un problème méthodologique, qui peut être corrigé en retravaillant les données d’entraînement.