import streamlit as st
import duckdb
import os

def show():
    st.title("Exploration SQL")

    temp_path = os.path.abspath("temp_validity.json")

    if os.path.exists(temp_path):
        with duckdb.connect() as con:
            # Charger extension JSON
            con.execute("INSTALL json; LOAD json;")

            # Charger ou recréer la table temporaire
            con.execute(f"""
                CREATE OR REPLACE TABLE ga4_data AS
                SELECT * FROM read_ndjson('{temp_path}', union_by_name=True, sample_size=1000000)
            """)
            st.success("Fichier chargé et DuckDB initialisé ✅")

            # Zone de requête utilisateur
            query = st.text_area("Écris ta requête SQL ici :", "SELECT * FROM ga4_data LIMIT 10")

            if st.button("Exécuter la requête"):
                try:
                    result = con.execute(query).df()
                    st.dataframe(result)
                except Exception as e:
                    st.error(f"Erreur dans la requête : {e}")
    else:
        st.warning("Fichier non trouvé. Va sur la page d'import pour charger le fichier.")
