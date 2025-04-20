import streamlit as st

def show():
    st.title("Bienvenue sur **GA4 Checker** 🕵️")
    st.markdown("""
    GA4 Checker est une application pensée pour vous accompagner dans l’analyse et l’audit de vos données **Google Analytics 4**, à partir des exports bruts de BigQuery.
    
    ---
    """)
    st.badge("New: 20/04/2025")
    st.markdown("""
        Vous pouvez maintenant utiliser un jeu de donnée de démonstration pour tester l'application
        Rendez-vous dans l'onglet dédié pour l'import de votre fichier ou utiliser la donnée de démonstration
        
        Vous pouvez également utilisez la fonction d'exploration libre pour consulter votre jeu de donnée

        ---
        """)
    st.badge("Update: 18/04/2025", icon=":material/check:", color="gray")
    st.markdown("""
    Le **premier module** est désormais disponible en phase de test :
    🔍 Vous pouvez extraire et analyser les URLs `page_location` du dataset avec les informations suivantes :
    - les paramètres présents,
    - les domaines et fragments,
    - les URLs en doublon ou trop longues,
    - ainsi qu'un résumé synthétique par URL.

    ---
    """)

    st.markdown("""
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
