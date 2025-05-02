import streamlit as st
import duckdb
import os

from st_pages import add_page_title, get_nav_from_toml

st.title("🧠 Exploration SQL libre")

db_path = os.path.abspath("../ga4.duckdb")

if os.path.exists(db_path):
    # Connexion à la base existante en lecture seule
    with st.spinner("🔌 Connexion à la base DuckDB en cours..."):
        con = duckdb.connect(database=db_path, read_only=True)

    # Zone de requête utilisateur
    query = st.text_area("💬 Écris ta requête SQL ici :", "SELECT * FROM ga4_data LIMIT 10", height=500)

    if st.button("▶️ Exécuter la requête"):
        try:
            with st.spinner("Requête en cours"):
                result = con.execute(query).df()
                st.dataframe(result, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Erreur dans la requête : {e}")

    con.close()
else:
    st.warning("⚠️ Aucune base trouvée. Va sur la page d'import pour charger un fichier GA4.")
