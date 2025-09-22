import os
import pandas as pd

# Dossier pollution
folder_path = "../data/pollution_airparif"
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

df_list = []

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    
    # Lire les 5 premières lignes
    meta = pd.read_csv(file_path, header=None, nrows=5)
    nom_stations = meta.iloc[1, 1:].tolist()
    numero_stations = meta.iloc[2, 1:].tolist()
    polluant = meta.iloc[4, 1]
    
    # Lire les vraies données
    df = pd.read_csv(file_path, skiprows=5)
    
    # Vérifier si la première ligne est une vraie date
    if pd.to_datetime(df.iloc[0, 0], errors="coerce") is pd.NaT:
        df = df.iloc[1:]
    
    # Renommer colonnes
    df.columns = ["date"] + numero_stations
    
    # Passer en format long
    df_long = df.melt(id_vars=["date"], 
                      value_vars=numero_stations, 
                      var_name="numero_station", 
                      value_name="valeur")
    
    # Ajouter métadonnées
    mapping_nom = dict(zip(numero_stations, nom_stations))
    df_long["nom_station"] = df_long["numero_station"].map(mapping_nom)
    df_long["polluant"] = polluant
    
    # Conversion en datetime et agrégation par jour
    df_long["date"] = pd.to_datetime(df_long["date"], errors="coerce")
    df_long["date"] = df_long["date"].dt.date

    df_list.append(df_long)

# Concaténer tous les fichiers
df_pollution = pd.concat(df_list, ignore_index=True)

# Importer le mapping des départements
df_dep = pd.read_excel("../data/pollution_airparif/dep_station.xlsx")
df_pollution = df_pollution.merge(df_dep, on="numero_station", how="left")

# Supprimer les colonnes de station
df_pollution = df_pollution.drop(columns=["numero_station", "nom_station"])

# Conversion de la colonne 'valeur' en float
df_pollution["valeur"] = pd.to_numeric(df_pollution["valeur"], errors="coerce")

# Supprimer les lignes où 'valeur' est NaN
df_pollution = df_pollution.dropna(subset=["valeur"])

# Moyenne, médiane et nombre de stations par département et polluant
df_pollution_dep_jour = (
    df_pollution
    .groupby(["date", "dep", "polluant"], as_index=False)
    .agg(
        valeur_mean=("valeur", "mean"),
        valeur_mediane=("valeur", "median"),
        nb_station_pollution=("valeur", "count")
    )
)

# --- Sauvegarde finale ---
output_file = "../exports/intermediaire/pollution_fusion.csv"
if os.path.exists(output_file):
    answer = input(f"Le fichier {output_file} existe déjà. Voulez-vous l'écraser ? (oui/non) : ").strip().lower()
    if answer == "oui":
        df_pollution_dep_jour.to_csv(output_file, index=False)
        print(f"Fichier créé : {output_file}")
        print(df_pollution_dep_jour.head(20))
    else:
        print(f"Fichier {output_file} non écrasé.")
else:
    df_pollution_dep_jour.to_csv(output_file, index=False)
    print(f"Fichier créé : {output_file}")