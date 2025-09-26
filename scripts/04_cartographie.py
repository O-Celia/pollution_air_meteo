import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Fichiers sources
data_file = "../exports/final/meteo_pollution.csv"
shapefile = "../data/shapefiles/geoflar-departements.shp"
output_folder = "../images/cartes"

# Charger les données
df = pd.read_csv(data_file)

# Conversion en datetime
df["date"] = pd.to_datetime(df["date"])

# Charger les polygones des départements/communes
gdf_dep = gpd.read_file(shapefile)

# S'assurer que le code département est au même format
gdf_dep["dep"] = gdf_dep["code_dept"].astype(str)
df["dep"] = df["dep"].astype(str)

# Moyenne par département
df_mean = df.groupby(["dep", "polluant"])["valeur_mean"].mean().reset_index()

# Fusion spatiale
gdf_merge = gdf_dep.merge(df_mean, on="dep", how="left")

# Choroplèthes
polluants = df["polluant"].unique()

for p in polluants:
    gdf_p = gdf_merge[gdf_merge["polluant"] == p]
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    gdf_dep.boundary.plot(ax=ax, color="black", linewidth=0.5)
    gdf_p.plot(column="valeur_mean",
               cmap="OrRd",
               legend=True,
               ax=ax,
               legend_kwds={"label": f"{p} (µg/m³)", "shrink": 0.6})
    plt.title(f"Moyenne annuelle de {p} par département")
    plt.savefig(os.path.join(output_folder, f"choropleth_{p}.png"))
    plt.close()

# Évolution spatio-temporelle
df["month"] = df["date"].dt.to_period("M").astype(str)
df_monthly = df.groupby(["dep", "polluant", "month"])["valeur_mean"].mean().reset_index()

for p in polluants:
    for m in df_monthly["month"].unique():
        gdf_pm = gdf_dep.merge(
            df_monthly[(df_monthly["polluant"] == p) & (df_monthly["month"] == m)],
            on="dep",
            how="left"
        )
        
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        gdf_dep.boundary.plot(ax=ax, color="black", linewidth=0.5)
        gdf_pm.plot(column="valeur_mean",
                    cmap="OrRd",
                    legend=True,
                    ax=ax,
                    vmin=df_monthly["valeur_mean"].min(),
                    vmax=df_monthly["valeur_mean"].max(),
                    legend_kwds={"label": f"{p} (µg/m³)", "shrink": 0.6})
        plt.title(f"{p} - {m}")
        plt.savefig(os.path.join(output_folder, f"{p}_{m}.png"))
        plt.close()

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

print("\n=== Moyenne annuelle par département et polluant ===")
print(df_mean)

print("\n=== Moyenne mensuelle par département et polluant ===")
print(df_monthly)
