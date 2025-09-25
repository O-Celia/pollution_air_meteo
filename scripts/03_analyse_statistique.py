import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Fichiers sources
pollution_file = "../exports/intermediaire/pollution_fusion.csv"
meteo_file = "../exports/intermediaire/clim_fusion.csv"
output_file = "../exports/final/meteo_pollution.csv"

# Dossiers pour sauvegarder les images
polluants_folder = "../images/polluants"
meteo_folder = "../images/meteo"
correlation_folder = "../images/correlation"

# Charger les fichiers
df_pollution = pd.read_csv(pollution_file)
df_meteo = pd.read_csv(meteo_file)

# Filtrer jours avec peu de stations
df_pollution = df_pollution[df_pollution["nb_station_pollution"] >= 3]
df_meteo = df_meteo[df_meteo["nb_station_meteo"] >= 3]

# Fusion par date et département
df_full = df_pollution.merge(
    df_meteo,
    on=["date", "dep"],
    how="inner"
)

# Sans doublons
df_full = df_full.drop_duplicates()

# Supprimer les dates inexistantes
df_full = df_full[(df_full['date'] >= '2020-01-01') & (df_full['date'] <= '2024-12-31')]

# Sauvegarde du fichier fusionné
if os.path.exists(output_file):
    answer = input(f"Le fichier {output_file} existe déjà. Voulez-vous l'écraser ? (oui/non) : ").strip().lower()
    if answer == "oui":
        df_full.to_csv(output_file, index=False)
        print(f"Fichier créé : {output_file}")
    else:
        print(f"Fichier {output_file} non écrasé.")
else:
    df_full.to_csv(output_file, index=False)
    print(f"Fichier créé : {output_file}")

# Boxplots polluants
polluants = df_full["polluant"].unique()
for p in polluants:
    plt.figure(figsize=(10,5))
    sns.boxplot(data=df_full[df_full["polluant"] == p], x="dep", y="valeur_mean")
    plt.title(f"Distribution des valeurs de {p} par département")
    plt.ylabel(f"{p} (µg/m³)")
    plt.xlabel("Département")
    plt.savefig(os.path.join(polluants_folder, f"boxplot_{p}_dep.png"))
    plt.close()

# Boxplots variables météo par polluant
rename_vars = {
    "etpgrille_mean": "Evapotranspiration potentielle (etpgrille)",
    "rr_mean": "Précipitations (rr)",
    "tn_mean": "Température min (tn)",
    "tx_mean": "Température max (tx)",
    "tm_mean": "Température moyenne (tm)",
    "ffm_mean": "Vitesse moyenne du vent (ffm)",
    "fxy_mean": "Vitesse max du vent (fxy)",
    "dxy_mean": "Direction max du vent (dxy)"
}

cols_meteo = [c for c in df_meteo.columns if c.endswith("_mean")]

for col in cols_meteo:
    plt.figure(figsize=(12,6))
    sns.boxplot(x="dep", y=col, data=df_meteo[~df_meteo[col].isna()])
    plt.title(f"Distribution de {rename_vars.get(col, col)} par département")
    plt.xlabel("Département")
    plt.ylabel(rename_vars.get(col, col))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(meteo_folder, f"boxplot_{col}_par_departement.png"))
    plt.close()
        
# Outliers
def detect_outliers_iqr(series):
    """Retourne les indices des outliers selon la règle 1.5×IQR"""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return series[(series < lower) | (series > upper)]

print("\n=== Détection d'outliers ===")

# Polluants
for p in df_full["polluant"].unique():
    vals = df_full.loc[df_full["polluant"] == p, "valeur_mean"].dropna()
    outliers = detect_outliers_iqr(vals)
    print(f"\nPolluant {p} :")
    print(f"  Total valeurs = {len(vals)}")
    print(f"  Outliers = {len(outliers)} ({len(outliers)/len(vals)*100:.1f}%)")
    print(f"  Min = {vals.min():.2f}, Max = {vals.max():.2f}")
    if not outliers.empty:
        print(f"  Min outlier = {outliers.min():.2f}, Max outlier = {outliers.max():.2f}")

# Météo
cols_meteo = [c for c in df_meteo.columns if c not in ["date","dep","nb_station_meteo"] and "mediane" not in c]

for col in cols_meteo:
    vals = df_meteo[col].dropna()
    outliers = detect_outliers_iqr(vals)
    print(f"\nMétéo {col} :")
    print(f"  Total valeurs = {len(vals)}")
    print(f"  Outliers = {len(outliers)} ({len(outliers)/len(vals)*100:.1f}%)")
    print(f"  Min = {vals.min():.2f}, Max = {vals.max():.2f}")
    if not outliers.empty:
        print(f"  Min outlier = {outliers.min():.2f}, Max outlier = {outliers.max():.2f}")

# Distribution météo selon polluant
for p in polluants:
    df_sub = df_full[df_full["polluant"] == p].rename(columns={"valeur_mean": p})

    for col in cols_meteo:
        plt.figure(figsize=(7,5))
        sns.scatterplot(x=col, y=p, data=df_sub, alpha=0.5)
        X = df_sub[[col]].dropna()
        y = df_sub[p].loc[X.index]
        
        if len(X) > 10:
            model = LinearRegression()
            model.fit(X, y)
            y_pred = model.predict(X)

            # R² et coefficients
            r2 = r2_score(y, y_pred)
            slope = model.coef_[0]
            intercept = model.intercept_

            # Courbe de régression
            x_range = np.linspace(X[col].min(), X[col].max(), 100)
            x_range_df = pd.DataFrame(x_range, columns=[col])
            plt.plot(x_range, model.predict(x_range_df), color="red", linewidth=2)

            plt.text(0.05, 0.95,
                     f"y = {slope:.2f}x + {intercept:.2f}\nR² = {r2:.3f}",
                     transform=plt.gca().transAxes,
                     fontsize=10, verticalalignment="top",
                     bbox=dict(facecolor="white", alpha=0.6, edgecolor="gray"))

        plt.title(f"{rename_vars.get(col,col)} vs {p}")
        plt.xlabel(rename_vars.get(col,col))
        plt.ylabel(f"{p} (µg/m³)")
        plt.tight_layout()

        plt.savefig(os.path.join(meteo_folder, f"scatter_regression_{col}_vs_{p}.png"))
        plt.close()
        
print("\n=== Pente et coefficient de détermination")
results = []
for p in polluants:
    df_sub = df_full[df_full["polluant"] == p]
    for col in cols_meteo:
        if col in df_sub.columns:
            X = df_sub[[col]]
            y = df_sub["valeur_mean"]
            model = LinearRegression().fit(X, y)
            y_pred = model.predict(X)
            slope = model.coef_[0]
            intercept = model.intercept_
            r2 = r2_score(y, y_pred)
            print(f"Polluant={p}, Variable météo={col}, pente={slope:.3f}, intercept={intercept:.2f}, R²={r2:.3f}")
            results.append([p, col, slope, intercept, r2])

# Statistiques descriptives
print("\n=== Aperçu ===")
print(df_full.head(10))

print("\n=== Description des variables pollution ===")
pollutants = df_pollution["polluant"].unique()
for p in pollutants:
    print(f"\nPolluant : {p}")
    print(df_full[df_full["polluant"] == p]["valeur_mean"].describe())

# Pivot pour corrélation
df_pivot = df_full.pivot_table(index=["date","dep"], 
                               columns="polluant", 
                               values="valeur_mean").reset_index()

# Joindre avec les variables météo
cols_meteo = [c for c in df_meteo.columns if "mean" in c and c not in ["nb_station_meteo"]]
df_corr = df_pivot.merge(df_meteo, on=["date","dep"], how="left")

# Corrélation réduite
polluants = df_full["polluant"].unique().tolist()
vars_polluants = [p for p in polluants if p in df_corr.columns]
vars_meteo = cols_meteo

corr_reduite = df_corr[vars_polluants + vars_meteo].corr().loc[vars_polluants, vars_meteo]

plt.figure(figsize=(16, 10))
sns.heatmap(corr_reduite, annot=True, fmt=".2f", cmap="coolwarm")

plt.title("Corrélations réduites : Polluants / Météo", fontsize=16)
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig(os.path.join(correlation_folder, "correlation_reduite_polluant_meteo.png"))
plt.close()

# Corrélation complète
plt.figure(figsize=(18, 14))
corr_complete = df_corr.drop(columns=["date","dep"]).corr()
sns.heatmap(corr_complete, annot=False, cmap="coolwarm")

plt.title("Corrélations complètes : Polluants + Météo", fontsize=16)
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig(os.path.join(correlation_folder, "correlation_complete.png"))
plt.close()

# Evolution temporelle par polluant
polluants = ["NO2", "O3", "PM10", "PM2.5"]
df_full["polluant"] = df_full["polluant"].replace({"PM25": "PM2.5"})

for p in polluants:
    df_sub = df_full[df_full["polluant"] == p]
    daily_mean = df_sub.groupby("date")["valeur_mean"].mean()

    plt.figure(figsize=(14, 5))
    daily_mean.plot()
    plt.title(f"Évolution quotidienne de {p} en Île-de-France")
    plt.ylabel(f"{p} (µg/m³)")
    plt.xlabel("Date")
    plt.savefig(os.path.join(polluants_folder, f"evolution_{p}.png"))
    plt.close()