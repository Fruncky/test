import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def format_usd(x, pos):
    return "${:,.0f}".format(x)

def plot_ca_par_annee(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df["Année"] = df["Date"].dt.year
    ca_par_annee = df.groupby("Année")["Revenue"].sum()

    plt.figure(figsize=(10,6))
    ca_par_annee.plot(kind="bar", color="skyblue")
    plt.title("Chiffre d'affaires par année")
    plt.ylabel("CA ($)")
    plt.xlabel("Année")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_usd))
    plt.tight_layout()
    plt.show()

def plot_ca_par_mois(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df["Mois"] = df["Date"].dt.month
    ca_par_mois = df.groupby("Mois")["Revenue"].sum()

    plt.figure(figsize=(10,6))
    ca_par_mois.plot(kind="bar", color="orange")
    plt.title("Chiffre d'affaires par mois")
    plt.ylabel("CA ($)")
    plt.xlabel("Mois")
    plt.xticks(ticks=range(12), labels=["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"], rotation=45)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_usd))
    plt.tight_layout()
    plt.show()


def plot_ca_par_pays(df):
    ca_pays = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False)

    plt.figure(figsize=(12,6))
    ca_pays.plot(kind="bar", color="mediumseagreen")
    plt.title("Chiffre d'affaires par pays")
    plt.xlabel("Pays")
    plt.ylabel("CA ($)")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_usd))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_ca_par_genre(df):
    ca_genre = df.groupby("Customer_Gender")["Revenue"].sum().sort_values(ascending=False)

    plt.figure(figsize=(6,5))
    ca_genre.plot(kind="bar", color=["royalblue", "lightpink"])
    plt.title("Chiffre d'affaires par genre")
    plt.xlabel("Genre")
    plt.ylabel("CA ($)")
    plt.xticks(rotation=0)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_usd))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_ca_par_pays_et_genre(df):
    pivot = df.pivot_table(values="Revenue", index="Country", columns="Customer_Gender", aggfunc="sum").fillna(0)
    pivot = pivot.sort_values(by=pivot.columns.tolist(), ascending=False)

    pivot.plot(kind="bar", figsize=(12,6))
    plt.title("Chiffre d'affaires par pays et par genre")
    plt.ylabel("CA ($)")
    plt.xlabel("Pays")
    plt.legend(title="Genre")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_usd))
    plt.tight_layout()
    plt.show()

def plot_ventes_par_mois_2015_par_pays(df, pays):
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Filtrage année 2015 et pays
    df_filtre = df[(df["Date"].dt.year == 2015) & (df["Country"] == pays)]

    # Groupement par mois
    ventes_par_mois = df_filtre.groupby(df_filtre["Date"].dt.month)["Order_Quantity"].sum()

    plt.figure(figsize=(10,6))
    ventes_par_mois.plot(kind="bar", color="cornflowerblue")
    plt.title(f"Volume de ventes mensuel en 2015 - {pays}")
    plt.xlabel("Mois")
    plt.ylabel("Quantité vendue")
    plt.xticks(ticks=range(0,12), labels=["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"], rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_saisonnalite_2011_2015_par_pays(df, top_pays=2):
    import seaborn as sns
    import matplotlib.pyplot as plt

    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month_name()
    df["Month_num"] = df["Date"].dt.month

    df_periode = df[(df["Year"] >= 2011) & (df["Year"] <= 2015)]

    top_countries = df_periode.groupby("Country")["Order_Quantity"].sum().nlargest(top_pays).index
    df_filtre = df_periode[df_periode["Country"].isin(top_countries)].copy()

    mois_ordre = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    df_filtre["Month"] = pd.Categorical(df_filtre["Month"], categories=mois_ordre, ordered=True)

    plt.figure(figsize=(12,6))
    sns.lineplot(
        data=df_filtre,
        x="Month",
        y="Order_Quantity",
        hue="Country",
        errorbar="sd"
    )

    plt.title("Saisonnalité des ventes de vélos (2011–2015) par pays")
    plt.xlabel("Mois")
    plt.ylabel("Quantité vendue")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def plot_saisonnalite_par_pays_input(df):
    import seaborn as sns
    import matplotlib.pyplot as plt
    from fonctions import filtrer_annees_completes

    # Étape 1 : filtrer les années complètes
    df = filtrer_annees_completes(df)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month_num"] = df["Date"].dt.month
    df["Month"] = df["Month_num"].map({
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
    })

    # Étape 2 : récupérer les pays encore présents après filtrage
    pays_disponibles = df["Country"].unique().tolist()

    if not pays_disponibles:
        print("❌ Aucun pays avec années complètes.")
        return

    print("🌍 Pays disponibles après filtrage global :")
    for i, pays in enumerate(pays_disponibles, start=1):
        print(f"{i} = {pays}")

    try:
        choix = int(input(f"👉 Entrez un numéro entre 1 et {len(pays_disponibles)} : "))
        if not 1 <= choix <= len(pays_disponibles):
            print("❌ Numéro invalide.")
            return
        pays_choisi = pays_disponibles[choix - 1]
    except:
        print("❌ Entrée invalide.")
        return

    # Étape 3 : filtrer pour le pays choisi
    df_pays = df[df["Country"] == pays_choisi].copy()

    if df_pays.empty or df_pays["Order_Quantity"].sum() == 0:
        print(f"❌ Aucune donnée valable pour {pays_choisi} après filtrage.")
        return

    # Étape 4 : afficher
    mois_ordre = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    df_pays["Month"] = pd.Categorical(df_pays["Month"], categories=mois_ordre, ordered=True)

    plt.figure(figsize=(10,6))
    sns.lineplot(data=df_pays, x="Month", y="Order_Quantity", errorbar="sd", color="teal")
    plt.title(f"Saisonnalité des ventes – {pays_choisi} (années complètes)")
    plt.xlabel("Mois")
    plt.ylabel("Quantité vendue")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_saisonnalite_bar_par_pays_input(df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    from fonctions import filtrer_annees_completes

    # ✅ Filtrage global des années complètes
    df = filtrer_annees_completes(df)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month_num"] = df["Date"].dt.month
    df["Month"] = df["Month_num"].map({
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
    })

    # ✅ Liste des pays valides
    pays_disponibles = df["Country"].unique().tolist()

    if not pays_disponibles:
        print("❌ Aucun pays avec données valides.")
        return

    print("🌍 Choisissez un pays :")
    for i, pays in enumerate(pays_disponibles, start=1):
        print(f"{i} = {pays}")

    try:
        choix = int(input(f"👉 Entrez un numéro entre 1 et {len(pays_disponibles)} : "))
        if not 1 <= choix <= len(pays_disponibles):
            print("❌ Numéro invalide.")
            return
        pays_choisi = pays_disponibles[choix - 1]
    except:
        print("❌ Entrée invalide.")
        return

    # ✅ Filtrage par pays
    df_pays = df[df["Country"] == pays_choisi].copy()
    if df_pays.empty or df_pays["Order_Quantity"].sum() == 0:
        print(f"❌ Aucune vente enregistrée pour {pays_choisi}.")
        return

    # ✅ Agrégation des ventes par mois
    df_pays["Month"] = pd.Categorical(df_pays["Month"], categories=[
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ], ordered=True)
    
    ventes_mensuelles = df_pays.groupby(["Year", "Month"], observed=True)["Order_Quantity"].sum().groupby("Month").mean()


    # ✅ Affichage en histogramme sans warning
    plt.figure(figsize=(10,6))
    sns.barplot(x=ventes_mensuelles.index, y=ventes_mensuelles.values)
    plt.title(f"Saisonnalité Moyenne des ventes – {pays_choisi} (années complètes)")
    plt.xlabel("Mois")
    plt.ylabel("Quantité vendue")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
