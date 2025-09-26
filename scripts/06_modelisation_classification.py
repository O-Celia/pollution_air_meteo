import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

from imblearn.over_sampling import SMOTE

# Dossiers
export_folder = "../exports/final"
df_full = pd.read_csv("../exports/final/meteo_pollution.csv")
df_full["polluant"] = df_full["polluant"].replace({"PM25": "PM2.5"})

# Pivot polluants
df_pivot = df_full.pivot_table(index=["date","dep"], 
                               columns="polluant", 
                               values="valeur_mean").reset_index()

# Variables météo
cols_meteo = [c for c in df_full.columns if c not in ["date","dep","polluant","valeur_mean","nb_station_pollution","nb_station_meteo"]]
df_merged = df_pivot.merge(df_full[["date","dep"] + cols_meteo].drop_duplicates(), on=["date","dep"], how="left")

polluants = ["NO2", "O3", "PM10", "PM2.5"]

results = []

for p in polluants:
    print(f"\n=== Classification pour {p} ===")

    # Cible : binaire (1 = au-dessus de la médiane, 0 sinon)
    median_val = df_merged[p].median()
    y = (df_merged[p] > median_val).astype(int)
    X = df_merged[cols_meteo]

    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=0.2, 
                                                        shuffle=True, 
                                                        random_state=42)

    # Appliquer SMOTE pour équilibrer
    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

    # Scaling
    scaler = StandardScaler()
    X_train_res = scaler.fit_transform(X_train_res)
    X_test = scaler.transform(X_test)

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
        "XGBoost": XGBClassifier(eval_metric="logloss", random_state=42)
    }

    for model_name, model in models.items():
        model.fit(X_train_res, y_train_res)
        y_pred = model.predict(X_test)

        report = classification_report(y_test, y_pred, output_dict=True)
        acc = report["accuracy"]
        prec = report["weighted avg"]["precision"]
        rec = report["weighted avg"]["recall"]
        f1 = report["weighted avg"]["f1-score"]

        results.append([p, model_name, acc, prec, rec, f1])

        with open(os.path.join(export_folder, f"{p}_{model_name}_report.txt"), "w") as f:
            f.write(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(5,4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Low","High"], yticklabels=["Low","High"])
        plt.title(f"Matrice de confusion - {p} ({model_name})")
        plt.ylabel("Vérité terrain")
        plt.xlabel("Prédiction")
        plt.savefig(os.path.join(export_folder, f"{p}_{model_name}_cm.png"))
        plt.close()

# Visualisation des performances globales
df_results = pd.DataFrame(results, columns=["Polluant","Modèle","Accuracy","Precision","Recall","F1-score"])
plt.figure(figsize=(12, 6))
sns.barplot(data=df_results, x="Polluant", y="F1-score", hue="Modèle")
plt.title("Comparaison des modèles - F1-score par polluant")
plt.ylabel("F1-score")
plt.ylim(0, 1.05)
plt.legend(title="Modèle")
plt.tight_layout()
plt.savefig(os.path.join(export_folder, "comparaison_modeles_f1.png"))
plt.close()


# Résumé global
df_results.to_csv(os.path.join(export_folder, "resultats_classification.csv"), index=False, encoding="utf-8-sig")
print("\n=== Sauvegarde terminée ===")
print(df_results)