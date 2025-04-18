# Streamlit app to analyze URL query parameters from GA4 event_params
import streamlit as st
import duckdb
import pandas as pd
import re
import os

from urllib.parse import urlparse, parse_qsl
from collections import Counter

def show():
    # --- Streamlit Config ---
    st.title("🔍 GA4 Checker – Chapitre 'Validity'")

    #-- class init --
    class URLInspector:
        def __init__(self, url):
            self.url = url
            self.parsed = urlparse(url)
            self.query_params = parse_qsl(self.parsed.query, keep_blank_values=True)

        def is_https(self):
            return self.parsed.scheme == "https"

        def get_netloc(self):
            return self.parsed.netloc

        def get_duplicate_params(self):
            keys = [k for k, _ in self.query_params]
            return [k for k, v in Counter(keys).items() if v > 1]

        def get_param_keys(self):
            return [k for k, _ in self.query_params]

        def has_fragment(self):
            return bool(self.parsed.fragment)

        def is_url_too_long(self, limit=1000):
            return len(self.url) > limit

        def summary(self):
            return {
                "url": self.url,
                "https": self.is_https(),
                "netloc": self.get_netloc(),
                "param_count": len(self.query_params),
                "param_keys": self.get_param_keys(),
                "dup_params": self.get_duplicate_params(),
                "has_fragment": self.has_fragment(),
                "url_too_long": self.is_url_too_long()
            }


    # --- Upload fichier JSON ---
    uploaded_file = st.file_uploader("Uploadez votre export GA4 (JSON)", type="json")

    if uploaded_file:
        temp_path = os.path.abspath("temp_validity.json")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # --- Connexion DuckDB ---
        con = duckdb.connect()
        con.execute("INSTALL json; LOAD json;")
        con.execute(f"""
            CREATE OR REPLACE TABLE ga4_data AS
            SELECT * FROM read_ndjson('{temp_path}', union_by_name=True, sample_size=1000000)
        """)

        st.success("Fichier chargé et DuckDB initialisé ✅")

        # --- Extraction des page_location ---
        st.subheader("📍 Extraction des URLs depuis 'page_location'")
        query = f'''
               SELECT DISTINCT
                   unnest.value.string_value AS page_location
               FROM GA4_data, 
               LATERAL UNNEST(event_params)
               WHERE unnest.key = 'page_location'
               AND unnest.value.string_value IS NOT NULL
               '''

        st.subheader("📋 Liste des page_location du dataset'")
        df_page_location = con.execute(query).df()
        st.dataframe(df_page_location, use_container_width=True)

        st.write(f"{len(df_page_location)} valeurs de 'page_location' extraites uniques")
        st.download_button("📥 Télécharger la liste des url en CSV", data=df_page_location.to_csv(index=False),
                           file_name="ga4_query_params.csv")

        # --- Extraction des queries (regex) ---
        regex_query = r'\?(.*)'
        regex_param = r'([^=&]+)(?:=[^&]*)?'

        query_url = []
        simple_query = set()

        for page in df_page_location['page_location']:
            match = re.search(regex_query, page)
            query = match.group(1) if match else None
            if query and query not in query_url:
                query_url.append(query)

        for q in query_url:
            matches = re.findall(regex_param, q)
            for param in matches:
                simple_query.add(param)

        st.subheader("📋 Liste des paramètres d'url dans votre dataset'")
        query_df = pd.DataFrame(sorted(list(simple_query)), columns=["query_param"])
        st.dataframe(query_df, use_container_width=True)

        st.download_button("📥 Télécharger les paramètres en CSV", data=query_df.to_csv(index=False), file_name="ga4_query_params.csv")

        # Création des résumés pour chaque URL
        summaries = []

        for url in df_page_location['page_location']:
            inspector = URLInspector(url)
            summaries.append(inspector.summary())

        # Création du DataFrame global de résumé
        summary_df = pd.DataFrame(summaries)

        # Affichage du tableau
        st.subheader("🧾 Résumé des URLs")
        st.dataframe(summary_df, use_container_width=True)

        # Téléchargement en CSV
        st.download_button("📥 Télécharger le résumé en CSV", data=summary_df.to_csv(index=False),
                           file_name="ga4_url_summary.csv")

        # Facultatif : Histogramme ou analyse plus poussée ici

        con.close()
    else:
        st.info("Veuillez uploader un fichier JSON pour lancer l'analyse.")
