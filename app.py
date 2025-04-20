import streamlit as st

from app_pa import home, remerciement, page_location_validity, exploration, data_import

# Page configs
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
page = st.sidebar.radio(
    "Aller vers",
        [
        "📖 À propos de l'app",
        "📂 Choisissez votre donnée",
        "🔗 Audit du page_location",
        "🔍 Exploration libre",
        "🤝 Remerciements"
        ]
)
# Routage des app_pa
if page == "📖 À propos de l'app":
    home.show()
elif page == "📂 Choisissez votre donnée":
    data_import.show()
elif page == "🔗 Audit du page_location":
    page_location_validity.show()
elif page == "🤝 Remerciements":
    remerciement.show()
elif page == "🔍 Exploration libre":
    exploration.show()