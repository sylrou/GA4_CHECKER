import string
import streamlit as st
import duckdb

from services import sql_requests
from assets.ui import ui_warning

def generate_letter_labels(n):
    letters = string.ascii_lowercase
    result = []
    i = 0
    while len(result) < n:
        prefix = ''
        q = i
        while True:
            q, r = divmod(q, 26)
            prefix = letters[r] + prefix
            if q == 0:
                break
        result.append(prefix)
        i += 1
    return result

def safe_query_wrapper(query_func, message="Une erreur est survenue."):
    """
    Exécute une fonction de requête avec gestion d'erreur et arrêt propre.

    Args:
        query_func (callable): Une fonction sans argument qui retourne un résultat.
        message (str): Message à afficher en cas d'erreur.

    Returns:
        Le résultat de la fonction si succès, sinon None (l'exécution s'arrête).
    """
    try:
        return query_func()
    except Exception as e:
        st.error(message)
        with st.expander("🛠️ Détails de l’erreur (debug)"):
            st.exception(e)
        st.stop()

# --- Fonction utilitaire pour lancer la base de données ---
# Date: 2025-05-10

import os
import duckdb
import streamlit as st
from services.functions import safe_query_wrapper
from assets.ui import ui_warning

def get_ga4_connection_or_stop(table_name: str = "ga4_data"):
    """
    Vérifie si la base GA4 est prête dans la session et retourne une connexion DuckDB.
    Sinon, arrête l'exécution avec un message d'avertissement.

    Parameters
    ----------
    table_name : str
        Nom attendu de la table GA4 dans la base.

    Returns
    -------
    duckdb.DuckDBPyConnection
    """
    if "db_path" not in st.session_state or not st.session_state.get("ga4_ready"):
        st.warning("❌ Aucune base de données disponible. Veuillez d'abord importer vos données.")
        st.stop()

    db_path = st.session_state.db_path
    con = duckdb.connect(database=db_path, read_only=False)

    # Vérifie que la table attendue existe
    tables = [row[0] for row in con.execute("SHOW TABLES").fetchall()]
    if table_name not in tables:
        st.error(f"⚠️ La table `{table_name}` est introuvable dans la base.")
        st.stop()

    return con
