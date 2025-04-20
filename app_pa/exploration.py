import streamlit as st
import duckdb
import os

def show():
    st.title("🧠 Exploration SQL libre")

    db_path = os.path.abspath("ga4.duckdb")

    if os.path.exists(db_path):
        # Connexion à la base existante en lecture seule
        con = duckdb.connect(database=db_path, read_only=True)

        # Zone de requête utilisateur
        query = st.text_area("💬 Écris ta requête SQL ici :", "SELECT * FROM ga4_data LIMIT 10")

        if st.button("▶️ Exécuter la requête"):
            try:
                result = con.execute(query).df()
                st.dataframe(result, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Erreur dans la requête : {e}")

        con.close()
    else:
        st.warning("⚠️ Aucune base trouvée. Va sur la page d'import pour charger un fichier GA4.")
