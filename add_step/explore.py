import streamlit as st
import duckdb
import os
from streamlit_ace import st_ace
from services.functions import  safe_query_wrapper

from st_pages import add_page_title, get_nav_from_toml
from services import sql_requests
from services.functions import launch
from assets.ui import ui_caption

st.title("🧠 Exploration SQL libre")

# --- Connexion à la base de données (compute) : vérifie existence et connecte ---
con = launch()

# Requêtes prédéfinies
st.markdown("### 📋 Requêtes pré-enregistrées")
preset_queries = {
    "Nombre total de sessions": sql_requests.m_sessions("ga4_data"),
    "Nombre total d'utilisateurs uniques": sql_requests.m_users("ga4_data"),
    "Nombre de jours uniques dans les données": sql_requests.m_date("ga4_data"),
    "Nombre d'événement": sql_requests.m_event_name("ga4_data"),
    "Liste des dates d'événements": sql_requests.d_event_date("ga4_data"),
    "Liste des custom_dimensions dans event_params": sql_requests.distinct_event_params_list("ga4_data"),
    "Liste des événements distincts": sql_requests.event_name_extract("ga4_data"),
    "Liste des urls distinctes (page_location)": sql_requests.page_location_extract("ga4_data")
}

options = ["Aucune requête pré-remplie (écriture libre)"] + list(preset_queries.keys())
selected_preset = st.selectbox("Sélectionnez une requête :", options)

if selected_preset == "Aucune requête pré-remplie (écriture libre)":
    # Éditeur libre avec coloration
    query = st_ace(
        value="SELECT * FROM ga4_data LIMIT 10",
        language="sql",
        theme="solarized_dark",
        height=300,
        key="sql_editor_free"
    )
else:
    query = preset_queries[selected_preset]
    st.code(query, language="sql")

if st.button("▶️ Exécuter la requête"):
    try:
        with st.spinner("Requête en cours..."):
            result = safe_query_wrapper(
                lambda:con.execute(query).df()
            )
            st.dataframe(result, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Erreur dans la requête : {e}")

con.close()


st.markdown("---")
st.subheader("💡 Proposer votre requête pour l'ajouter en feature dans l'app !")
st.markdown(
    """
    Utilisez le formulaire pour proposer une **feature**,une **requête**, suggérer une **amélioration UX**, ou signaler un **bug** :
    """
)
st.link_button("📝 Remplir le formulaire Google", "https://docs.google.com/forms/d/e/1FAIpQLSflgaNI4c_SjCECVzIM78DQuqd-UmyuNyHSFbDZ99YGe58pbQ/viewform?usp=header")

ui_caption()


