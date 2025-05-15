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

def separer_velos_accessoires(df, path_velos, path_accessoires):
    """
    Sépare le DataFrame en deux fichiers : vélos et accessoires.
    
    Paramètres :
    - df (pd.DataFrame) : données brutes
    - path_velos (str) : chemin du fichier pour les vélos
    - path_accessoires (str) : chemin du fichier pour les accessoires
    """
    categories_velos = ['Mountain Bikes', 'Road Bikes', 'Touring Bikes']
    
    df_velos = df[df['Sub_Category'].isin(categories_velos)]
    df_accessoires = df[~df['Sub_Category'].isin(categories_velos)]
    
    df_velos.to_csv(path_velos, index=False)
    df_accessoires.to_csv(path_accessoires, index=False)
    
    print(f"✅ Fichier vélos sauvegardé : {path_velos}")
    print(f"✅ Fichier accessoires sauvegardé : {path_accessoires}")



def charger_donnees(path):
    """
    Charge un fichier CSV et retourne un DataFrame.
    
    Paramètre :
    - path (str) : chemin vers le fichier CSV
    
    Retour :
    - pd.DataFrame : les données chargées
    """
    return pd.read_csv(path)

def nettoyer_doublons(df):
    """
    Supprime les doublons strictement identiques dans le DataFrame.
    
    Paramètre :
    - df (pd.DataFrame) : DataFrame à nettoyer
    
    Retour :
    - pd.DataFrame : DataFrame sans doublons
    """
    return df.drop_duplicates()

def afficher_doublons(df):
    """
    Retourne les lignes strictement dupliquées (hors première occurrence).
    
    Paramètre :
    - df (pd.DataFrame)
    
    Retour :
    - pd.DataFrame contenant uniquement les doublons
    """
    return df[df.duplicated(keep=False)]

def traiter_valeurs_manquantes(df):
    """
    Supprime les lignes contenant des valeurs manquantes.
    (Tu peux remplacer par un autre traitement si besoin, ex : fillna)
    
    Paramètre :
    - df (pd.DataFrame)
    
    Retour :
    - pd.DataFrame : DataFrame nettoyé
    """
    return df.dropna()

def convertir_colonne_en_datetime(df, colonne):
    """
    Convertit une colonne en format datetime.
    
    Paramètres :
    - df (pd.DataFrame)
    - colonne (str) : nom de la colonne à convertir
    
    Retour :
    - pd.DataFrame avec la colonne convertie
    """
    df[colonne] = pd.to_datetime(df[colonne], errors='coerce')
    return df

def pipeline_nettoyage(df, colonne_date):
    """
    Exécute l'ensemble des étapes de nettoyage de données.
    
    Paramètres :
    - df (pd.DataFrame)
    - colonne_date (str) : nom de la colonne contenant la date à convertir
    
    Retour :
    - pd.DataFrame nettoyé
    """
    df = nettoyer_doublons(df)
    df = traiter_valeurs_manquantes(df)
    df = convertir_colonne_en_datetime(df, colonne_date)
    return df
