import streamlit as st
import random

def show():
    # 🎉 Petit effet sympa à chaque chargement
    st.balloons()

    # Titre principal
    st.title("🤝 Remerciements")

    # Introduction
    st.markdown("""
    Bienvenue sur la page des remerciements du projet **GA4Checker**.  
    Ce projet est open-source, mais surtout une belle aventure humaine 🙌  
    Merci à toutes celles et ceux qui, de près ou de loin, ont contribué à sa création et son évolution.
    """)

    st.markdown("---")

    # Special thanks
    st.subheader("🤍 Very special thanks")
    st.markdown("""
    - **Yannick Darcy** — Pour son soutien indéfectible et sans qui aucune ligne de code ne serait jamais en production.
    - **Jonathan Mary** — Pour m'avoir (généreusement 😅) forcé à suivre *Introduction to Computer Science with Python* du MIT.
    - **Corentin Deschamps** — Pour avoir partagé cette aventure de formation avec moi.
    """)

    # Contributions
    st.subheader("🧠 Contributions & Soutiens")
    st.markdown("""
    - **Christian Laville**
    - **Clément Tabard**
    - **Benjamin Dubreu et dataUpskill**
    - **Gaël Penessot et son livre**
    - **L'AADF - Association des analystes de France**
    
    - **Toutes les personnes qui partagent leurs idées, retours, et leur temps.**
    """)

    # Appel à contribution
    st.markdown("""
    **Et vous ?**  
    Si vous avez des idées, des remarques, ou l’envie de contribuer, n'hésitez pas à me contacter !
    """)

    # Footer light
    st.markdown("---")
    st.caption("✨ GA4Checker — un projet open-source, évolutif, et fait avec passion.")