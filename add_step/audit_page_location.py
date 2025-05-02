# Analyser les paramètres d'URL à partir de GA4 (event_params)
import streamlit as st
import duckdb
import pandas as pd
import os

from services.url_inspector import URLInspector
from services.query_classifier import *

st.title("🔍 Audit des paramètres d'URL (`page_location`)")

# --- Étape de vérification (compute) : vérifier l'existence de la base de données ---
db_path = os.path.abspath("../ga4.duckdb")
if not os.path.exists(db_path):
    st.error("Aucune base de données trouvée. Veuillez d'abord importer un fichier via la page d'import.")
    st.stop()

# --- Connexion à la base de données (compute) ---
with st.spinner("🔌 Connexion à la base DuckDB en cours..."):
    con = duckdb.connect(database=db_path, read_only=True)

# --- Requête SQL (compute) : extraire les valeurs uniques de 'page_location' ---
st.subheader("📍 Extraction des URLs depuis 'page_location'")
query = '''
    SELECT DISTINCT
        unnest.value.string_value AS page_location
    FROM ga4_data, 
    LATERAL UNNEST(event_params) AS unnest
    WHERE unnest.key = 'page_location'
    AND unnest.value.string_value IS NOT NULL
'''
with st.spinner("Requête en cours..."):
    df_page_location = con.execute(query).df()
con.close()

# --- Affichage (display) : visualisation des URLs extraites ---
st.subheader("📋 Liste des 'page_location'")
st.metric(label="URLs uniques extraites", value=len(df_page_location), border=True)
st.data_editor(df_page_location, use_container_width=True)
st.download_button("📥 Télécharger les URLs", data=df_page_location.to_csv(index=False), file_name="ga4_page_location.csv")

# --- Analyse des paramètres d'URL (compute) ---
simple_query = set()
for page in df_page_location['page_location']:
    inspector = URLInspector(page)
    simple_query.update(inspector.get_unique_param_keys())

# --- Affichage (display) : liste des paramètres détectés ---
st.subheader("🧾 Liste des paramètres détectés")
query_df = pd.DataFrame(sorted(list(simple_query)), columns=["query_param"])
query_df["categorie"] = query_df["query_param"].apply(classify_query_param)

colA, colB, colC = st.columns(3)
colA.metric(label="Nombre de paramètres uniques", value=len(simple_query), border=True)
nb_crit = (query_df["categorie"] == "critical").sum()
colB.metric(label="Nombre de paramètres critiques", value=nb_crit, border=True)
nb_other = (query_df["categorie"] == "other").sum()
colC.metric(label="Nombre de paramètres autres", value=nb_other, border=True)
st.data_editor(query_df, use_container_width=True)
st.download_button("📥 Télécharger les paramètres", data=query_df.to_csv(index=False), file_name="ga4_query_params.csv")

# --- Résumé technique par URL (compute) ---
st.subheader("🧪 Résumé technique par URL")
summaries = [URLInspector(url).summary() for url in df_page_location['page_location']]
summary_df = pd.DataFrame(summaries)

# --- Affichage (display) : métriques techniques ---
col1, col2, col3 = st.columns(3)
col1.metric(label="Nombre d'URLs en HTTP", value=(summary_df['https'].value_counts().get("❌", 0)), border=True)
col2.metric(label="Nombre d'hôtes différents", value=len(summary_df['hostname'].unique()), border=True)
col3.metric(label="Nombre max de paramètres", value=summary_df['param_count'].max(), border=True)

st.data_editor(summary_df, use_container_width=True)
st.download_button("📥 Télécharger le résumé complet", data=summary_df.to_csv(index=False), file_name="ga4_url_summary.csv")
