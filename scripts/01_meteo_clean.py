import os
import pandas as pd

def load_and_concat_csv(folder_path, prefix, colonnes_a_garder, output_file=None):
    # Liste des fichiers CSV correspondant au préfixe
    csv_files = [f for f in os.listdir(folder_path) if f.startswith(prefix) and f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError(f"Aucun fichier correspondant à {prefix} trouvé.")

    # Lire et concaténer tous les fichiers
    df_list = []
    for f in csv_files:
        df = pd.read_csv(os.path.join(folder_path, f), sep=",")
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df = combined_df[colonnes_a_garder]

    # Sauvegarde si demandé
    if output_file:
        if os.path.exists(output_file):
            answer = input(f"Le fichier {output_file} existe déjà. Voulez-vous l'écraser ? (oui/non) : ").strip().lower()
            if answer == "oui":
                combined_df.to_csv(output_file, index=False)
                print(f"Fichier créé : {output_file}")
            else:
                print(f"Fichier {output_file} non écrasé.")
        else:
            combined_df.to_csv(output_file, index=False)
            print(f"Fichier créé : {output_file}")

    return combined_df


# Paramètres
folder_path = "../data/meteo_ile_de_france"
export_folder = "../exports/intermediaire"

# Chargement datasets
df_autres_principal = load_and_concat_csv(
    folder_path,
    prefix="clim-base_quot_autres",
    colonnes_a_garder=['aaaammjj', 'num_poste', 'etpgrille'],
    #output_file=os.path.join(export_folder, "clim_autres_principal.csv")
    output_file=None
)

df_autres_secondaire = load_and_concat_csv(
    folder_path,
    prefix="clim-base_quot_autres",
    colonnes_a_garder=['aaaammjj', 'num_poste', 'pmerm', 'tsvm', 'brume', 'brou', 'fumee', 'etpgrille'],
    #output_file=os.path.join(export_folder, "clim_autres_secondaire.csv")
    output_file=None
)

df_vent = load_and_concat_csv(
    folder_path,
    prefix="clim-base_quot_vent",
    colonnes_a_garder=['aaaammjj', 'num_poste', 'rr', 'tn', 'tx', 'tm', 'ffm', 'fxy', 'dxy'],
    #output_file=os.path.join(export_folder, "clim_vent_prefusion.csv")
    output_file=None
)


# Fusion principal "autres" + vent
df_fusion = pd.merge(df_autres_principal, df_vent, on=["aaaammjj", "num_poste"], how="inner")
colonnes_meteo_vent = ['etpgrille','rr','tn','tx','tm','ffm','fxy','dxy']
df_fusion_clean = df_fusion.dropna(subset=colonnes_meteo_vent)

# conversion en datetime
df_fusion_clean = df_fusion_clean.rename(columns={"aaaammjj": "date"})
df_fusion_clean["date"] = pd.to_datetime(df_fusion_clean["date"], format="%Y%m%d", errors="coerce")
df_fusion_clean["date"] = df_fusion_clean["date"].dt.date

# Création de la colonne dep
df_fusion_clean["dep"] = df_fusion_clean["num_poste"].astype(str).str[:2]

# Réordonner les colonnes pour mettre dep juste après date
cols = df_fusion_clean.columns.tolist()
cols.remove("dep")
cols.insert(1, "dep")
df_fusion_clean = df_fusion_clean[cols]

# Conversion des valeurs en float
colonnes_float = ['etpgrille','rr','tn','tx','tm','ffm','fxy','dxy']
df_fusion_clean[colonnes_float] = df_fusion_clean[colonnes_float].apply(pd.to_numeric, errors="coerce")

# Agrégation : moyenne, médiane, nb de stations
df_fusion_dep_jour = (
    df_fusion_clean
    .groupby(["date", "dep"], as_index=False)
    .agg(
        etpgrille_mean=("etpgrille", "mean"),
        etpgrille_mediane=("etpgrille", "median"),
        rr_mean=("rr", "mean"),
        rr_mediane=("rr", "median"),
        tn_mean=("tn", "mean"),
        tn_mediane=("tn", "median"),
        tx_mean=("tx", "mean"),
        tx_mediane=("tx", "median"),
        tm_mean=("tm", "mean"),
        tm_mediane=("tm", "median"),
        ffm_mean=("ffm", "mean"),
        ffm_mediane=("ffm", "median"),
        fxy_mean=("fxy", "mean"),
        fxy_mediane=("fxy", "median"),
        dxy_mean=("dxy", "mean"),
        dxy_mediane=("dxy", "median"),
        nb_station_meteo=("date", "count")
    )
)

# --- Sauvegarde finale ---
output_fusion = os.path.join(export_folder, "clim_fusion.csv")
if os.path.exists(output_fusion):
    answer = input(f"Le fichier {output_fusion} existe déjà. Voulez-vous l'écraser ? (oui/non) : ").strip().lower()
    if answer == "oui":
        df_fusion_dep_jour.to_csv(output_fusion, index=False)
        print(f"Fichier fusionné créé : {output_fusion}")
        print(df_fusion_dep_jour.head(20))
    else:
        print(f"Fichier {output_fusion} non écrasé.")
else:
    df_fusion_dep_jour.to_csv(output_fusion, index=False)
    print(f"Fichier fusionné créé : {output_fusion}")
