import streamlit as st

def show():
    st.title("GA4 Checker 🕵️")
    st.markdown("""
    Bienvenue sur **GA4 Checker** !
    
    Cette application vous permet d’analyser et d'avoir un audit automatisé de votre donnée GA4 :
    
    - Le premier module à venir va vous permettre d'importer et analyser vos page_location
    - L'objectif final est d'automatiser votre audit GA4 au global depuis la donnée brute, sans modification des données sources
    
    D'autres modules viendront enrichir l'application bientôt 🚀
    """)

    # FOOTER
    st.markdown("""
        <div class="footer">
            Créé avec ❤️ par <a href="https://www.linkedin.com/in/empirik-sylvain-rouxel/" target="_blank">Sylvain Rouxel</a>
        </div>
    """, unsafe_allow_html=True)