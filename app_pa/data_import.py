import duckdb
import streamlit as st
import os

def show():
    st.header("📥 Importer les données GA4")

    if os.path.exists(os.path.abspath("local_analysis.json")):
        data_file = os.path.abspath("local_analysis.json")
        st.success("Mode local activé, le jeu de donnée local est sélectionné ✅")
    else:
        user_test_data = st.toggle("🔧 Utiliser un jeu de données de démonstration")
        if user_test_data:
            data_file = os.path.abspath("animalien_data.json")
            st.success("Jeu de démonstration sélectionné ✅")
        else:
            # Proposer un upload
            uploaded_file = st.file_uploader("Uploadez votre export GA4 (JSON)", type="json")

            # Sécurité : attendre l'upload
            if not uploaded_file:
                st.warning("Veuillez uploader un fichier JSON pour continuer.")
                st.stop()

            # Sauvegarde temporaire du fichier JSON
            temp_path = os.path.abspath("temp_validity.json")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            data_file = temp_path
            st.success("Fichier chargé ✅")

    # --- Création de la base persistante DuckDB ---
    db_path = os.path.abspath("ga4.duckdb")
    with st.spinner("⏳ Chargement du fichier dans DuckDB..."):
        con = duckdb.connect(database=db_path, read_only=False)
        con.execute("INSTALL json; LOAD json;")

        con.execute("DROP TABLE IF EXISTS ga4_data;")  # Pour éviter conflits
        con.execute(f"""
            CREATE TABLE ga4_data AS
            SELECT * FROM read_ndjson('{data_file}', union_by_name=True)
        """)

        con.close()

    st.success("Base DuckDB créée avec succès ✅")
    st.info(f"📂 Fichier sauvegardé : `{db_path}`")
