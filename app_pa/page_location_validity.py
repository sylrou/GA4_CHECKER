# Streamlit app to analyze URL query parameters from GA4 event_params
import streamlit as st
import duckdb
import pandas as pd
import re
import os

from urllib.parse import urlparse, parse_qsl
from collections import Counter

def show():
    st.title("🔍 Audit des paramètres d’URL (`page_location`)")

    # --- Vérifie si le fichier ga4.duckdb existe ---
    db_path = os.path.abspath("ga4.duckdb")
    if not os.path.exists(db_path):
        st.error("Aucune base de données trouvée. Veuillez d'abord importer un fichier via la page d'import.")
        st.stop()

    # --- Connexion à la base existante ---
    with st.spinner("🔌 Connexion à la base DuckDB en cours..."):
        con = duckdb.connect(database=db_path, read_only=True)

    # -- Classe d’analyse des URLs --
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

    # --- Extraction des page_location ---
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

    st.subheader("📋 Liste des 'page_location'")
    st.dataframe(df_page_location, use_container_width=True)
    st.write(f"{len(df_page_location)} URLs uniques extraites")

    st.download_button("📥 Télécharger les URLs", data=df_page_location.to_csv(index=False),
                       file_name="ga4_page_location.csv")

    # --- Analyse des paramètres d’URL ---
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

    st.subheader("🧾 Liste des paramètres détectés")
    query_df = pd.DataFrame(sorted(list(simple_query)), columns=["query_param"])
    st.dataframe(query_df, use_container_width=True)
    st.download_button("📥 Télécharger les paramètres", data=query_df.to_csv(index=False), file_name="ga4_query_params.csv")

    # --- Résumés par URL ---
    st.subheader("🧪 Résumé technique par URL")
    summaries = [URLInspector(url).summary() for url in df_page_location['page_location']]
    summary_df = pd.DataFrame(summaries)
    st.dataframe(summary_df, use_container_width=True)
    st.download_button("📥 Télécharger le résumé complet", data=summary_df.to_csv(index=False), file_name="ga4_url_summary.csv")
