import streamlit as st

from app_pa import home, remerciement, page_location_validity

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
        "🔗 Audit page location",
        "🤝 Remerciement"
        ]
)
# Routage des app_pa
if page == "📖 À propos de l'app":
    home.show()
elif page == "🔗 Audit page location":
    page_location_validity.show()
elif page == " Remerciement":
    remerciement.show()