import streamlit as st
from urllib.parse import urlparse
from pathlib import Path

# Page config
st.set_page_config(
    page_title="GA4 Checker",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement du CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Navigation
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Aller vers", ["📖 À propos de l'app", "🔎 Analyse d'URL"])

# PAGE 1 : Présentation
if page == "📖 À propos de l'app":
    st.title("GA4 Checker 🕵️")
    st.markdown("""
    Bienvenue sur **GA4 Checker** !

    Cette application vous permet d’analyser les URLs issues de vos exports GA4 (Google Analytics 4) afin de :

    - Le premier module à venir va vous permettre d'importer et analyser vos page_location
    - L'objectif final est d'automatiser votre audit GA4 au global depuis la donnée brute, sans modification des données sources

    D'autres modules viendront enrichir l'application bientôt 🚀
    """)

# PAGE 2 : URL Parser
elif page == "🔎 Page Location Checker":
    st.title("🔗 Analyse d'une URL")
    #user_input = st.text_input("Colle ici l’URL à analyser :")
    """
    if user_input:
        try:
            parsed = urlparse(user_input)
            st.subheader("Résultats du parsing")
            st.json({
                "scheme": parsed.scheme,
                "netloc": parsed.netloc,
                "path": parsed.path,
                "params": parsed.params,
                "query": parsed.query,
                "fragment": parsed.fragment
            })
        except Exception as e:
            st.error(f"Erreur de parsing : {e}")
    """

# FOOTER
st.markdown("""
    <div class="footer">
        Créé avec ❤️ par <a href="https://www.linkedin.com/in/empirik-sylvain-rouxel/" target="_blank">Sylvain Rouxel</a>
    </div>
""", unsafe_allow_html=True)
