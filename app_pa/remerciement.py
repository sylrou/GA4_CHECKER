# 3_🤝_remerciements.py

import streamlit as st
import random

def show():
    # Animation random pour le fun 🎉
    st.balloons()


    # Titre de la page
    st.title("🤝 Remerciements")

    # Message d'intro
    st.markdown("""
    Bienvenue sur la page des remerciements du projet **GA4Checker**.  
    Ce projet est open-source, mais il est avant tout une aventure humaine 🙌  
    Merci à toutes celles et ceux qui ont contribué à le faire grandir !
    """)

    # Liste des remerciements
    st.markdown("---")
    st.subheader("💡 Very special thanks")
    st.markdown("""
    - **Yannick Darcy** — Pour son encouragement et sans qui jamais une seule ligne de code ne serait en production.
    """)

    st.subheader("💡 Contributions & Soutiens")

    st.markdown("""
    - **Christian Laville**
    - **Clément Tabard**
    - **Les personnes qui partagent**
    """)

    st.markdown("""
    **Et vous ?**  
    Si vous avez des idées, remarques ou que vous souhaitez contribuer, n'hésitez pas à me contacter ou à faire une *pull request* 🛠️
    """)

    # Option : pied de page app_pa
    st.markdown("---")
    st.caption("✨ Projet GA4Checker — open-source & évolutif.")
