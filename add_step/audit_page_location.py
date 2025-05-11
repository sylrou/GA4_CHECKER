# Analyser les paramètres d'URL à partir de GA4 (event_params)
import streamlit as st
import duckdb
import pandas as pd
import os
import altair as alt

from services.url_inspector import URLInspector
from services.query_classifier import *
from services import sql_requests
from assets.ui import ui_warning, ui_caption, ui_sep, ui_detective_tip
from services.functions import safe_query_wrapper, get_ga4_connection_or_stop

GA4_DATA = "ga4_data"
detective_bubble = []

st.title("🔍 Analyse - `page_location` du dataset")

# --- Connexion à la base de données (compute) ---
with st.spinner("🔌 Connexion à la base DuckDB en cours..."):
    con = get_ga4_connection_or_stop()

# --- Requête SQL (compute) : extraire les valeurs uniques de 'page_location' ---
st.subheader("Extraction des URLs depuis 'page_location'")

with st.spinner("Requête en cours..."):
    df_page_location = safe_query_wrapper(
        lambda :con.execute(sql_requests.page_location_extract(GA4_DATA)).df(),
        "Erreur dans l'extraction du page_location"
    )

con.close()

# --- Affichage (display) : visualisation des URLs extraites ---
st.subheader("Liste des 'page_location'")
st.metric(
    label="URLs uniques extraites",
    value=len(df_page_location),
    border=True
)
with st.expander('📊 Affichez la liste des pages_location dans le dataset'):
    st.data_editor(df_page_location, use_container_width=True)
    st.download_button(
        "📥 Télécharger les URLs",
        data=df_page_location.to_csv(index=False),
        file_name="ga4_page_location.csv"
    )
ui_sep()

# --- Analyse des paramètres d'URL (compute) ---
with st.spinner("🔍 Analyse des paramètres d'URL en cours..."):
    simple_query = set()
    for page in df_page_location['page_location']:
        inspector = URLInspector(page)
        simple_query.update(inspector.get_unique_param_keys())

# --- Affichage (display) : liste des paramètres détectés ---
st.subheader("Liste des paramètres détectés")
query_df = pd.DataFrame(sorted(list(simple_query)), columns=["query_param"])
query_df["categorie"] = query_df["query_param"].apply(classify_query_param)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Nombre de paramètres uniques",
        value=len(simple_query),
        border=True
    )
with col2:
    nb_crit = (query_df["categorie"] == "critical").sum()
    st.metric(
        label="Nombre de paramètres critiques",
        value=nb_crit,
        border=True
    )
    if nb_crit > 0:
        detective_bubble.append("❌ Vérifiez les paramètres d'urls s'il n'y a pas des informations critiques")
with col3:
    nb_other = (query_df["categorie"] == "other").sum()
    st.metric(
        label="Nombre de paramètres autres",
        value=nb_other,
        border=True)

if detective_bubble:
    text = "\n\n".join(detective_bubble)
    ui_detective_tip(text)
    detective_bubble = []

with st.expander("📊 Affichez la liste des paramètres de l'url"):
    st.data_editor(query_df, use_container_width=True)
    st.download_button(
        "📥 Télécharger les paramètres",
        data=query_df.to_csv(index=False),
        file_name="ga4_query_params.csv"
    )
ui_sep()
# --- Résumé technique par URL (compute) ---
st.subheader("Résumé technique par URL")
with st.spinner("📊 Génération du résumé technique par URL..."):
    summaries = [URLInspector(url).summary() for url in df_page_location['page_location']]
    summary_df = pd.DataFrame(summaries)

# --- Affichage (display) : métriques techniques ---
col4, col5, col6 = st.columns(3)
with col4:

    http_number = (summary_df['https'].value_counts().get("❌", 0))
    st.metric(
        label="Nombre d'URLs en HTTP",
        value=http_number,
        border=True
    )
    if http_number > 0:
        detective_bubble.append("❌ Vous avez des url en http:// au lieu de https://")

with col5:
    hostname_number = len(summary_df['hostname'].unique())
    st.metric(
        label="Nombre d'hôtes différents",
        value=hostname_number,
        border=True
    )
    if hostname_number > 1:
        detective_bubble.append("❌ Vous avez plusieurs domaines dans votre tracking, \n vérifiez qu'il n'y a pas de préproduction ou de domaine involontaire")

with col6:
    max_param_count = summary_df['param_count'].max()
    st.metric(
        label="Nombre max de paramètres",
        value= max_param_count,
        border=True
    )

if detective_bubble:
    text = "\n\n".join(detective_bubble)
    ui_detective_tip(text)
    detective_bubble = []

ui_sep()

col7, col8, col9 = st.columns(3)
with col7:
    dup_params_number = summary_df['dup_params_count'].max()
    st.metric(
        label="Nombre de paramètres d'URL dupliqués",
        value=dup_params_number,
        border=True
    )
    if dup_params_number > 0:
        detective_bubble.append("❌ Vous avez des paramètres en double dans vos urls")

with col8:
    max_url_too_long = summary_df['url_too_long'].max()
    st.metric(
        label="Nombre de longueur max d'url rencontrée",
        value=max_url_too_long,
        border=True
    )
    if max_url_too_long >= 1000:
        detective_bubble.append("❌ Il y a des urls trop longue, vous devriez vérifier cette partie !")

if detective_bubble:
    text = "\n\n".join(detective_bubble)
    ui_detective_tip(text)
    detective_bubble = []

with st.spinner("📊 Génération du résumé technique par URL..."):
    with st.expander("📊 Afficher le tableau récapitulatif"):
        st.data_editor(summary_df, use_container_width=True)
        st.download_button(
        "📥 Télécharger le résumé complet",
        data=summary_df.to_csv(index=False),
        file_name="ga4_url_summary.csv"
        )
ui_caption()