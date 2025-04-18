import streamlit as st

def show():
    st.title("Bienvenue sur **GA4 Checker** 🕵️")
    st.markdown("""
    GA4 Checker est une application pensée pour vous accompagner dans l’analyse et l’audit de vos données **Google Analytics 4**, à partir des exports bruts de BigQuery.

    ---

    ### 🚀 Nouveauté (18/04/2025)

    Le **premier module** est désormais disponible en phase de test :
    🔍 **Chapitre "Validity"** – Analyse des URLs `page_location` de votre GA4 pour en extraire :
    - les paramètres présents,
    - les domaines et fragments,
    - les URLs en doublon ou trop longues,
    - ainsi qu'un résumé synthétique par URL.

    ---

    ### 📚 Une approche par chapitres

    Cette application évoluera progressivement sous la forme de **chapitres** :  
    Chaque module viendra enrichir votre audit GA4, avec un focus précis (comme un livre que vous écrivez, page après page).

    🎯 **Objectif final :** vous permettre d’automatiser un audit complet GA4 à partir de la donnée brute, **sans modification manuelle** de la structure source.

    ---

    🧪 N'hésitez pas à tester le module actuel, et à faire vos retours.
    D'autres chapitres arrivent très bientôt ! 🚧
    """)

    # FOOTER
    st.markdown("""
        <div class="footer">
            💬 Une question, un besoin ou envie d’échanger sur la donnée ?<br>
            👉 <a href="https://www.linkedin.com/in/empirik-sylvain-rouxel/" target="_blank">Contactez-moi sur LinkedIn</a><br><br>
            Créé avec ❤️ par <strong>Sylvain Rouxel</strong>
        </div>
    """, unsafe_allow_html=True)
