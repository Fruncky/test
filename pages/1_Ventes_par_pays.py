import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fonctions import filtrer_annees_completes

st.header("Saisonnalité des ventes par pays")

df = pd.read_csv("data/velos.csv")
df = filtrer_annees_completes(df)
df["Date"] = pd.to_datetime(df["Date"])
df["Month_num"] = df["Date"].dt.month
df["Month"] = df["Month_num"].map({
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
})

pays_list = df["Country"].unique().tolist()
pays_choisi = st.selectbox("Choisissez un pays :", pays_list)

df_pays = df[df["Country"] == pays_choisi].copy()
mois_ordre = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
df_pays["Month"] = pd.Categorical(df_pays["Month"], categories=mois_ordre, ordered=True)
ventes_mensuelles = df_pays.groupby("Month", observed=True)["Order_Quantity"].sum()

st.subheader(f"Saisonnalité des ventes – {pays_choisi}")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=ventes_mensuelles.index, y=ventes_mensuelles.values, ax=ax)
ax.set_ylabel("Quantité vendue")
ax.set_xlabel("Mois")
ax.set_title("Ventes par mois")
plt.xticks(rotation=45)
st.pyplot(fig)
