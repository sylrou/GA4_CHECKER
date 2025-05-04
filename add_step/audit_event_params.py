# Analyser les paramètres d'URL à partir de GA4 (event_params)
import streamlit as st
import duckdb
import pandas as pd
import os

from services import sql_requests
from assets.ui import ui_warning

GA4_DATA = "ga4_data"

st.title("🔍 Analyse - `event_params` du dataset")
st.markdown("""
Objectif : vérifier la présence systématique d’une `dimension` dans votre `event_params` sur un événement donné (ex. page_view).
Cela permet d’identifier d’éventuelles erreurs d’implémentation ou des absences inattendues de données.

👉 Si une `dimension` (comme category_page) est censée apparaître sur chaque page_view,
alors le nombre d'événements page_view devrait être égal au nombre d'occurrences où cette dimension est présente.

➡️ Le delta (écart) permet d’identifier s’il y a un problème. Un delta important peut révéler une anomalie.
""")

# --- Étape de vérification (compute) : vérifier l'existence de la base de données ---
db_path = os.path.abspath("../ga4.duckdb")
if not os.path.exists(db_path):
    ui_warning()
    st.stop()

# --- Connexion à la base de données (compute) ---
with st.spinner("🔌 Connexion à la base DuckDB en cours..."):
    con = duckdb.connect(database=db_path, read_only=True)

with st.spinner("Requête en cours..."):
    df_custom_dimension = con.execute(sql_requests.event_and_customdim_checker(GA4_DATA)).df()

st.markdown("""### Tableau d'exploration - Consultez le delta""")
# --- Chargement de la table d'exploration
with st.spinner("Chargement de la table en cours..."):
    st.data_editor(df_custom_dimension, use_container_width=True)

# --- Téléchargement CSV ---
st.download_button("📥 Télécharger le détail des 'custom dimension'", data=df_custom_dimension.to_csv(index=False), file_name="ga4_custom_dimension.csv")

# --- Chargement de la table calculée (déjà jointe) ---
with st.spinner("📊 Chargement des custom dimensions..."):
    df = con.execute(sql_requests.event_and_customdim_checker(GA4_DATA)).df()
    df["key"] = df["key"].str.replace('"', '', regex=False)

# --- Liste unique des clés disponibles ---
available_keys = sorted(df["key"].unique())

st.markdown("""---""")
# --- Sélecteur de custom dimension ---
st.markdown("""### 🔑 Choisissez la clé du event_params à analyser""")
selected_key = st.selectbox("Lorem", options=available_keys, label_visibility="hidden")
st.markdown("""---""")

# --- Filtrage du DataFrame ---
filtered_df = df[df["key"] == selected_key].copy()

# --- Affichage des résultats ---
st.markdown(f"### Résultat pour la clé : `{selected_key}`")
st.data_editor(filtered_df, use_container_width=True)

# --- Téléchargement CSV ---
st.download_button(
    label="📥 Télécharger les résultats filtrés (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name=f"ga4_custom_dimension_{selected_key}.csv"
)

# --- Graphique avec un MultiIndex pour la gestion des couleurs
filtered_df["delta"] = filtered_df["total_event"] - filtered_df["custom_dim_number"]
st.markdown(f"""
### 📊 Visualisation pour la clé : `{selected_key}`

Ce graphique vous aide à **identifier rapidement les événements** pour lesquels la custom dimension sélectionnée est **partiellement manquante**.

- 🟩 **Barre verte** : représente le nombre d'événements où la dimension `{selected_key}` est bien présente.
- 🟥 **Barre rouge** : représente le nombre d'événements où **la dimension est absente** alors qu’elle est attendue.
- 📊 **Total (vert + rouge)** = nombre total d'événements (`total_event`).

Un **delta important** (barre rouge large) peut signaler :
- une erreur d'implémentation,
- une configuration incomplète,
- ou une condition non remplie côté dataLayer / GTM.

👉 **Objectif** : réduire au maximum la barre rouge pour garantir une donnée fiable et complète.
""")

st.bar_chart(filtered_df.set_index("event_name")[["custom_dim_number", "delta"]], color=["#00cc66","#cc0000"], horizontal=True, )

con.close()
