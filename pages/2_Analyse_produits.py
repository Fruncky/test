import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from fonctions import filtrer_annees_completes

st.header("🛍️ Analyse des produits les plus vendus")

df = pd.read_csv("data/velos.csv")
df = filtrer_annees_completes(df)
df["Date"] = pd.to_datetime(df["Date"])
df["Month_num"] = df["Date"].dt.month
df["Month"] = df["Month_num"].map({
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
})

# 🌍 Sélecteur de pays pour filtrer l’analyse produits
pays_list = df["Country"].unique().tolist()
pays_choisi = st.selectbox("Choisissez un pays pour l’analyse produit :", pays_list)

df_pays = df[df["Country"] == pays_choisi].copy()

choix_produit = st.selectbox("Choisissez l'analyse produit :", [
    "Top 10 produits (quantité vendue)",
    "Ventes par catégorie et sous-catégorie"
])

if choix_produit == "Top 10 produits (quantité vendue)":
    def clean_product_name(name):
        return re.split(r",\s*\d+|,\s*(XS|S|M|L|XL|XXL)?$", name)[0]
    df_pays["Product_Type"] = df_pays["Product"].apply(clean_product_name)
    top_types = (
        df_pays.groupby("Product_Type")["Order_Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_types.values, y=top_types.index, palette="viridis", ax=ax)
    ax.set_title(f"Top 10 types de produits les plus vendus ({pays_choisi})")
    ax.set_xlabel("Quantité vendue")
    ax.set_ylabel("Type de produit")
    st.pyplot(fig)

elif choix_produit == "Ventes par catégorie et sous-catégorie":
    df_cat = (
        df_pays.groupby(["Product_Category", "Sub_Category"])["Order_Quantity"]
        .sum()
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=df_cat,
        x="Order_Quantity", y="Sub_Category",
        hue="Product_Category", dodge=False,
        palette="Set2", ax=ax
    )
    ax.set_title(f"Ventes par sous-catégorie et catégorie ({pays_choisi})")
    ax.set_xlabel("Quantité vendue")
    ax.set_ylabel("Sous-catégorie")
    st.pyplot(fig)
