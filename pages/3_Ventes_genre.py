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
