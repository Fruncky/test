import streamlit as st
import pandas as pd

st.header("Page de test")
st.write("Ceci est une page de test pour l'application.")

# Exemple simple : afficher les 5 premières lignes du jeu de données principal
try:
    df = pd.read_csv("data/velos.csv")
    st.subheader("Aperçu des données")
    st.write(df.head())
except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
