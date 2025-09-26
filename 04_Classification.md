# Classification pollution-météo

## Objectif
Prédire si la concentration de différents polluants atmosphériques (NO₂, O₃, PM₁₀, PM₂.₅) est au-dessus ou en-dessous de la médiane à partir de variables météorologiques.

## Méthodologie
- Préparation des données
  - Séparation en jeu d’entraînement (80%) et de test (20%).
  - SMOTE appliqué pour équilibrer les classes.
  - Standardisation des données pour les modèles linéaires.
- Modèles testés
  - Régression Logistique
  - RandomForest
  - XGBoost
- Évaluation
  - Accuracy, Precision, Recall, F1-score (moyenne pondérée).

## Résultats

| Polluant | Modèle              | Accuracy | Precision | Recall | F1-score |
|----------|---------------------|----------|-----------|--------|----------|
| NO₂      | LogisticRegression  | 0.74     | 0.74      | 0.74   | 0.74     |
| NO₂      | RandomForest        | 0.96     | 0.96      | 0.96   | 0.96     |
| NO₂      | XGBoost             | 0.94     | 0.94      | 0.94   | 0.94     |
| O₃       | LogisticRegression  | 0.80     | 0.80      | 0.80   | 0.80     |
| O₃       | RandomForest        | 0.99     | 0.99      | 0.99   | 0.99     |
| O₃       | XGBoost             | 0.97     | 0.97      | 0.97   | 0.97     |
| PM₁₀     | LogisticRegression  | 0.70     | 0.70      | 0.70   | 0.70     |
| PM₁₀     | RandomForest        | 0.90     | 0.90      | 0.90   | 0.90     |
| PM₁₀     | XGBoost             | 0.92     | 0.92      | 0.92   | 0.92     |
| PM₂.₅    | LogisticRegression  | 0.72     | 0.72      | 0.72   | 0.72     |
| PM₂.₅    | RandomForest        | 0.98     | 0.98      | 0.98   | 0.98     |
| PM₂.₅    | XGBoost             | 0.93     | 0.93      | 0.93   | 0.93     |

## Interprétation
- Les modèles non-linéaires (RandomForest, XGBoost) surpassent largement la Régression Logistique.
- O₃ est le polluant le plus prédictible à partir des conditions météorologiques.
- Les particules (PM₁₀, PM₂.₅) sont plus difficiles à modéliser linéairement mais donnent de bons résultats avec des algorithmes avancés.
- Globalement, la météo joue un rôle déterminant dans les concentrations de polluants, bien que l’importance varie selon le polluant.
