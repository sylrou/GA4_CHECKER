import string
import streamlit as st

from services import sql_requests

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