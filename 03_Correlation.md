# Modélisation des concentrations de polluants en fonction des variables météo

## 1. Objectif
L’objectif de cette étape est d’évaluer la capacité des variables météorologiques à expliquer et prédire les niveaux de pollution atmosphérique en Île-de-France.  
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
  - NO₂ : 40 µg/m³  
  - O₃ : 100 µg/m³  
  - PM10 : 40 µg/m³  
  - PM2.5 : 25 µg/m³  
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
| NO₂  | RF : 5.99<br>XGB : 5.54 | ~7 | ~7 | 0.19–0.30 | Faible pouvoir explicatif : dépend surtout du trafic. |
| O₃   | RF : 7.08<br>XGB : 6.99 | ~9 | ~9 | 0.70 | Bon modèle : O₃ fortement corrélé à la météo (soleil, T°C). |
| PM10 | RF : 5.09<br>XGB : 4.82 | ~6 | ~6 | ≈0 | Pas d’explication météo : dépend d’autres sources (chauffage, poussières). |
| PM2.5| RF : 2.78<br>XGB : 2.73 | ~3.6 | ~3.7 | 0.32–0.34 | Explication partielle : influence météo + autres sources. |

O₃ est le polluant le mieux prédit par la météo** (R² ~0.7).  
Les particules et le NO₂ dépendent beaucoup plus des émissions locales que des conditions atmosphériques.  

### Classification
| Polluant | Modèle        | Accuracy | F1-score | Interprétation |
|----------|--------------|----------|----------|----------------|
| NO₂  | RF, XGB, LR  | ~0.99    | 0.20–0.27 | Mauvaise détection des dépassements. |
| O₃   | RF, XGB, LR  | ~0.99    | 0.00 | Les dépassements sont trop rares : F1 nul. |
| PM10 | RF, XGB, LR  | ~0.99    | 0.00 | Même problème : classes trop déséquilibrées. |
| PM2.5| RF, XGB, LR  | ~0.98    | 0.18–0.26 | Faible détection des dépassements. |

Bien que l’accuracy soit très élevée, les modèles prédisent presque toujours "pas de dépassement" car les dépassements sont très rares.  
Les résultats sont donc non pertinents sans rééquilibrage des classes (oversampling, SMOTE, etc.).  

---

## 4. Conclusion
- **Ozone (O₃)** : la météo explique une grande partie de ses variations = bon candidat pour la modélisation prédictive.  
- **NO₂ et PM (PM10/PM2.5)** : mal expliqués par la météo = nécessitent des données supplémentaires (trafic, chauffage, industrie).  
- **Classification** : inutilisable en l’état = problème d’événements rares.  
