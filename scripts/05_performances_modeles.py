import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    f1_score,
)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier

# Charger les données préparées
data_file = "../exports/final/meteo_pollution.csv"
df_full = pd.read_csv(data_file)

# Harmonisation des noms de polluants
df_full["polluant"] = df_full["polluant"].replace({"PM25": "PM2.5"})
polluants = ["NO2", "O3", "PM10", "PM2.5"]

results = []

# Seuils OMS 2021 (valeurs 24h)
thresholds = {"NO2": 25, "O3": 100, "PM10": 45, "PM2.5": 15}

# Boucle par polluant
for p in polluants:
    print(f"\n=== Modélisation pour {p} ===")

    df_sub = df_full[df_full["polluant"] == p].copy()
    X = df_sub[
        [c for c in df_sub.columns if c.endswith("_mean") and c not in ["valeur_mean"]]
    ]
    y = df_sub["valeur_mean"]

    # Split aléatoire train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=True, random_state=42
    )

    # Régression
    regressors = {
        "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42),
        "XGBoost": XGBRegressor(n_estimators=200, learning_rate=0.1, random_state=42),
    }

    for name, model in regressors.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        results.append([p, "Régression", name, mae, rmse, r2])

    # Classification : Seuils OMS simplifiés
    y_class = (y > thresholds[p]).astype(int)

    X_train, X_test, y_class_train, y_class_test = train_test_split(
        X, y_class, test_size=0.2, shuffle=True, random_state=42
    )

    # Standardisation
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    classifiers = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=200, learning_rate=0.1, random_state=42),
    }

    for name, model in classifiers.items():
        if name == "LogisticRegression":
            model.fit(X_train_scaled, y_class_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_class_train)
            y_pred = model.predict(X_test)

        acc = accuracy_score(y_class_test, y_pred)
        f1 = f1_score(y_class_test, y_pred)

        results.append([p, "Classification", name, acc, f1, None])

# Résultats finaux
df_results = pd.DataFrame(
    results, columns=["Polluant", "Tâche", "Modèle", "Score1", "Score2", "Score3"]
)
print(df_results)
df_results.to_csv(
    "../exports/intermediaire/modelisation/resultats_modelisation.csv",
    index=False,
    encoding="utf-8-sig",
)
