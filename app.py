import streamlit as st

from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide", page_icon="🕵️")

with st.sidebar:
    st.image("assets/logo.png", width=150)

nav = get_nav_from_toml(".streamlit/pages.toml")
pg = st.navigation(nav)

pg.run()

# Chargement du CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()