import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fonctions import filtrer_annees_completes

# 🧪 Titre du dashboard
st.title("🚲 Dashboard interactif des ventes de vélos")

# 📁 Chargement des données
df = pd.read_csv("data/velos.csv")

# 🧼 Nettoyage via pipeline
df = filtrer_annees_completes(df)
df["Date"] = pd.to_datetime(df["Date"])
df["Month_num"] = df["Date"].dt.month
df["Month"] = df["Month_num"].map({
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
})

# 🌍 Sélecteur de pays
pays_list = df["Country"].unique().tolist()
pays_choisi = st.selectbox("Choisissez un pays :", pays_list)

# 📊 Agrégation des ventes
df_pays = df[df["Country"] == pays_choisi].copy()
mois_ordre = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
df_pays["Month"] = pd.Categorical(df_pays["Month"], categories=mois_ordre, ordered=True)
ventes_mensuelles = df_pays.groupby("Month", observed=True)["Order_Quantity"].sum()

# 📈 Affichage du graphique
st.subheader(f"Saisonnalité des ventes – {pays_choisi}")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=ventes_mensuelles.index, y=ventes_mensuelles.values, ax=ax)
ax.set_ylabel("Quantité vendue")
ax.set_xlabel("Mois")
ax.set_title("Ventes par mois")
plt.xticks(rotation=45)
st.pyplot(fig)

st.markdown("---")
st.subheader("🛍️ Analyse des produits les plus vendus")

choix_produit = st.selectbox("Choisissez l'analyse produit :", [
    "Top 10 produits (quantité vendue)",
    "Ventes par catégorie et sous-catégorie"
])

if choix_produit == "Top 10 produits (quantité vendue)":
    top_produits = df.groupby("Product")["Order_Quantity"].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_produits.values, y=top_produits.index, palette="viridis", ax=ax)
    ax.set_title("Top 10 produits les plus vendus")
    ax.set_xlabel("Quantité vendue")
    ax.set_ylabel("Produit")
    st.pyplot(fig)

elif choix_produit == "Ventes par catégorie et sous-catégorie":
    df_cat = df.groupby(["Product_Category", "Sub_Category"])["Order_Quantity"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=df_cat,
        x="Order_Quantity", y="Sub_Category",
        hue="Product_Category", dodge=False,
        palette="Set2", ax=ax
    )
    ax.set_title("Ventes par sous-catégorie et catégorie")
    ax.set_xlabel("Quantité vendue")
    ax.set_ylabel("Sous-catégorie")
    st.pyplot(fig)
