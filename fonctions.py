# fonctions.py
import pandas as pd

def filtrer_annees_completes(df):
    """
    Filtre le DataFrame pour ne conserver que les années avec 12 mois de ventes.

    Paramètre :
    - df (pd.DataFrame)

    Retour :
    - pd.DataFrame contenant uniquement les années complètes
    """
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    # Nombre de mois distincts par année
    mois_par_annee = df.groupby("Year")["Month"].nunique()

    # Années avec les 12 mois présents
    annees_completes = mois_par_annee[mois_par_annee == 12].index

    df_filtre = df[df["Year"].isin(annees_completes)].copy()

    return df_filtre
