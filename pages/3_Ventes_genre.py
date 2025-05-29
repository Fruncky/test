import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fonctions import filtrer_annees_completes

st.header("🚹🚺 Ventes par genre, pays et sous-catégorie de vélo")

# Chargement des données
df = pd.read_csv("data/velos.csv")
df = filtrer_annees_completes(df)

# Menus pour choisir le pays et la sous-catégorie
pays_list = sorted(df["Country"].unique().tolist())
pays_choisi = st.selectbox("Choisissez un pays :", pays_list)

# On ne garde que les vélos (pas les accessoires)
categories_velos = ['Mountain Bikes', 'Road Bikes', 'Touring Bikes']
df_velos = df[df['Sub_Category'].isin(categories_velos)]
subcat_list = sorted(df_velos["Sub_Category"].unique().tolist())
subcat_choisie = st.selectbox("Choisissez la sous-catégorie de vélo :", subcat_list)

# Filtrage du dataframe selon le pays et la sous-catégorie
df_filtre = df_velos[
    (df_velos["Country"] == pays_choisi) & 
    (df_velos["Sub_Category"] == subcat_choisie)
]

# Groupement par genre
ventes_genre = df_filtre.groupby("Customer_Gender")["Order_Quantity"].sum().reset_index()

# Affichage du graphique
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(data=ventes_genre, x="Customer_Gender", y="Order_Quantity", palette="pastel", ax=ax)
ax.set_title(f"Ventes par genre ({pays_choisi}, {subcat_choisie})")
ax.set_xlabel("Genre")
ax.set_ylabel("Quantité vendue")
st.pyplot(fig)

# Trouver la dernière année complète du dataset filtré
annee_max = df_filtre["Date"].dt.year.max() if not df_filtre.empty else df["Date"].dt.year.max()

st.subheader(f"Saisonnalité des ventes par genre en {annee_max}")

if not df_filtre.empty:
    # On garde uniquement la dernière année complète
    df_filtre["Date"] = pd.to_datetime(df_filtre["Date"])
    df_annee = df_filtre[df_filtre["Date"].dt.year == annee_max].copy()
    df_annee["Month"] = df_annee["Date"].dt.month
    mois_ordre = [1,2,3,4,5,6,7,8,9,10,11,12]

    # Groupement par mois et genre
    ventes_mois_genre = (
        df_annee.groupby(["Month", "Customer_Gender"])["Order_Quantity"]
        .sum()
        .reset_index()
    )
    # Mapping pour affichage mois en français ou anglais selon ton choix
    mois_labels = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]

    # Affichage du graphique de saisonnalité
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.lineplot(
        data=ventes_mois_genre,
        x="Month",
        y="Order_Quantity",
        hue="Customer_Gender",
        marker="o",
        ax=ax2
    )
    ax2.set_title(f"Saisonnalité {annee_max} – {pays_choisi}, {subcat_choisie}")
    ax2.set_xlabel("Mois")
    ax2.set_ylabel("Quantité vendue")
    ax2.set_xticks(mois_ordre)
    ax2.set_xticklabels(mois_labels)
    ax2.legend(title="Genre")
    st.pyplot(fig2)
else:
    st.info("Pas de ventes sur cette sélection pour afficher la saisonnalité.")
