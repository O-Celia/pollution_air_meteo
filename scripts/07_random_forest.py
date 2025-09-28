import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    classification_report,
    confusion_matrix,
)

# Chargement des données
export_folder = "../exports/final"
export_image = "../images/predictions"
df_full = pd.read_csv("../exports/final/meteo_pollution.csv")
df_full["polluant"] = df_full["polluant"].replace({"PM25": "PM2.5"})

# Pivot polluants
df_pivot = df_full.pivot_table(
    index=["date", "dep"], columns="polluant", values="valeur_mean"
).reset_index()

# Variables météo
cols_meteo = [
    c
    for c in df_full.columns
    if c
    not in [
        "date",
        "dep",
        "polluant",
        "valeur_mean",
        "nb_station_pollution",
        "nb_station_meteo",
    ]
]
df_merged = df_pivot.merge(
    df_full[["date", "dep"] + cols_meteo].drop_duplicates(),
    on=["date", "dep"],
    how="left",
)
df_merged = df_merged.dropna().copy()

polluants = ["NO2", "O3", "PM10", "PM2.5"]

# Régression : prédiction des concentrations
results_reg = []
predictions_list = []

for p in polluants:
    print(f"\n=== Régression pour {p} ===")

    X = df_merged[cols_meteo]
    y = df_merged[p]

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=True, random_state=42
    )

    # Réinitialiser les indices
    X_test = X_test.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)

    # Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Modèle
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Évaluation
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse**0.5
    r2 = r2_score(y_test, y_pred)
    results_reg.append([p, rmse, r2])

    # Sauvegarder les prédictions test
    df_pred_test = pd.DataFrame(
        {"valeur_reelle": y_test, "valeur_predite": y_pred, "polluant": p}
    )
    predictions_list.append(df_pred_test)

    # Scatter plot
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        "r--",
    )
    plt.xlabel("Valeurs réelles (test)")
    plt.ylabel("Valeurs prédites (test)")
    plt.title(f"Réel vs Prédit (80/20 test) - {p}")
    plt.tight_layout()
    plt.savefig(os.path.join(export_image, f"scatter_reel_vs_pred_test_{p}.png"))
    plt.close()

df_results_reg = pd.DataFrame(results_reg, columns=["Polluant", "RMSE", "R²"])
df_results_reg.to_csv(
    os.path.join(export_folder, "resultats_regression_randomforest.csv"),
    index=False,
    encoding="utf-8-sig",
)

print("\n=== Résultats Régression ===")
print(df_results_reg)

# Prediction sur tout le dataset
df_predictions_full = []

for p in polluants:
    X_full = df_merged[cols_meteo]
    y_full = df_merged[p]

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_full)

    # Modèle
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_scaled, y_full)

    y_pred_full = model.predict(X_scaled)

    df_pred_full = df_merged[["date", "dep"]].copy()
    df_pred_full["polluant"] = p
    df_pred_full["valeur_reelle"] = y_full.values
    df_pred_full["valeur_predite"] = y_pred_full

    df_predictions_full.append(df_pred_full)

df_predictions_full = pd.concat(df_predictions_full, ignore_index=True)
df_predictions_full.to_csv(
    os.path.join(export_folder, "predictions_randomforest_full.csv"),
    index=False,
    encoding="utf-8-sig",
)

# Plot valeurs réelles vs valeurs prédites
for p in polluants:
    df_sub = df_predictions_full[df_predictions_full["polluant"] == p]

    plt.figure(figsize=(6, 6))
    plt.scatter(df_sub["valeur_reelle"], df_sub["valeur_predite"], alpha=0.5)
    plt.plot(
        [df_sub["valeur_reelle"].min(), df_sub["valeur_reelle"].max()],
        [df_sub["valeur_reelle"].min(), df_sub["valeur_reelle"].max()],
        "r--",
    )
    plt.xlabel("Valeurs réelles")
    plt.ylabel("Valeurs prédites")
    plt.title(f"Réel vs Prédit - {p}")
    plt.tight_layout()
    plt.savefig(os.path.join(export_image, f"scatter_reel_vs_pred_{p}.png"))
    plt.close()

# Evolution temporelle réelle vs prédite
for p in polluants:
    df_sub = df_predictions_full[df_predictions_full["polluant"] == p].sort_values(
        "date"
    )
    df_sub["date"] = pd.to_datetime(df_sub["date"])

    plt.figure(figsize=(12, 5))
    plt.plot(df_sub["date"], df_sub["valeur_reelle"], label="Réel", alpha=0.7)
    plt.plot(df_sub["date"], df_sub["valeur_predite"], label="Prédit", alpha=0.7)

    # Formater l'axe x pour n'afficher que l'année
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    plt.xlabel("Année")
    plt.ylabel("Concentration")
    plt.title(f"Évolution temporelle - {p}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(export_image, f"evolution_temporelle_{p}.png"))
    plt.close()

# Classification : zones à risque médiane
results_clf = []

for p in polluants:
    print(f"\n=== Classification pour {p} ===")

    median_val = df_merged[p].median()
    y = (df_merged[p] > median_val).astype(int)  # 1 = haut risque, 0 = bas risque
    X = df_merged[cols_meteo]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=True, random_state=42
    )

    # Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Modèle
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Évaluation
    report = classification_report(y_test, y_pred, output_dict=True)
    acc = report["accuracy"]
    f1 = report["weighted avg"]["f1-score"]

    results_clf.append([p, acc, f1])

    # Sauvegarde matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Bas risque", "Haut risque"],
        yticklabels=["Bas risque", "Haut risque"],
    )
    plt.title(f"Matrice de confusion - {p}")
    plt.ylabel("Vérité terrain")
    plt.xlabel("Prédiction")
    plt.savefig(os.path.join(export_image, f"{p}_randomforest.png"))
    plt.close()

df_results_clf = pd.DataFrame(results_clf, columns=["Polluant", "Accuracy", "F1-score"])
df_results_clf.to_csv(
    os.path.join(export_folder, "resultats_classification_randomforest.csv"),
    index=False,
    encoding="utf-8-sig",
)

print("\n=== Résultats Classification médiane===")
print(df_results_clf)

# Classification : Seuils OMS (annuels)
thresholds_oms = {"NO2": 10, "O3": 60, "PM10": 15, "PM2.5": 5}

results_clf_oms = []

for p in polluants:
    print(f"\n=== Classification OMS pour {p} ===")

    y = (df_merged[p] > thresholds_oms[p]).astype(int)  # 1 = dépassement OMS
    X = df_merged[cols_meteo]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=True, random_state=42
    )

    # Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Modèle
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Évaluation
    report = classification_report(y_test, y_pred, output_dict=True)
    acc = report["accuracy"]
    f1 = report["weighted avg"]["f1-score"]

    results_clf_oms.append([p, acc, f1])

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["≤ seuil OMS", "> seuil OMS"],
        yticklabels=["≤ seuil OMS", "> seuil OMS"],
    )
    plt.title(f"Matrice de confusion - {p} (Seuil OMS)")
    plt.ylabel("Vérité terrain")
    plt.xlabel("Prédiction")
    plt.savefig(os.path.join(export_image, f"{p}_randomforest_oms.png"))
    plt.close()

df_results_clf_oms = pd.DataFrame(
    results_clf_oms, columns=["Polluant", "Accuracy", "F1-score"]
)

df_results_clf_oms.to_csv(
    os.path.join(export_folder, "resultats_classification_randomforest_oms.csv"),
    index=False,
    encoding="utf-8-sig",
)

# Moyenne réelle et prédite par polluant
print("\n=== Moyenne des valeurs réelles et prédites par polluant ===")
print(
    df_predictions_full.groupby("polluant")[["valeur_reelle", "valeur_predite"]].mean()
)

# Moyenne réelle et prédite par polluant et département
moyenne_dep = (
    df_predictions_full.groupby(["polluant", "dep"])[
        ["valeur_reelle", "valeur_predite"]
    ]
    .mean()
    .reset_index()
)

print("\n=== Moyenne par polluant et département ===")
print(moyenne_dep)
