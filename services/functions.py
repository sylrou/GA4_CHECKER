import string
import streamlit as st

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

def launch():
    """
    Initialise la connexion à la base DuckDB si elle existe.

    Returns:
        duckdb.DuckDBPyConnection: Connexion à la base DuckDB en lecture seule.

    Raises:
        streamlit.StopException: Arrête l'exécution si la base n'existe pas ou échoue à se connecter.
    """
    db_path = os.path.abspath("../ga4.duckdb")

    with st.spinner("🔌 Connexion à la base DuckDB en cours..."):
        if not os.path.exists(db_path):
            ui_warning()
            st.stop()

        return safe_query_wrapper(
            lambda: duckdb.connect(database=db_path, read_only=True),
            "❌ Erreur lors de la connexion à la base DuckDB."
        )
