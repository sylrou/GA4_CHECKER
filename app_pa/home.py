# 2025-04-21 - Page d'accueil principale de l'application GA4 Checker

import streamlit as st

def show():
    # Titre principal de la page
    st.title("Bienvenue sur **GA4 Checker** 🕵️")

    # Introduction générale
    st.markdown("""
    GA4 Checker est une application conçue pour vous accompagner dans l’analyse et l’audit de vos données **Google Analytics 4**, à partir des exports bruts de BigQuery.

    ---
    """)

    # Badge de nouveauté
    st.badge("Nouveau : 20/04/2025")

    # Bloc sur la démonstration et l'import
    st.markdown("""
    Vous pouvez désormais utiliser un jeu de données de démonstration pour tester l'application.  
    Rendez-vous dans l’onglet dédié pour importer votre propre fichier ou explorer l'exemple fourni.

    Il est également possible d’utiliser la fonction d’exploration libre pour consulter en détail votre jeu de données
    via des requêtes SQL.

    Pour les fichiers supérieurs à 1Go, contactez-moi pour une utilisation en local.  
    Cela permet de débloquer la limite de taille imposée par Streamlit (mais reste dépendant des performances de votre machine).

    ---
    """)

    # Badge de mise à jour
    st.badge("Mise à jour : 21/04/2025", icon=":material/check:", color="gray")

    # Description du premier module disponible
    st.markdown("""
    Le **premier module** est désormais disponible en phase de test :  
    🔍 Il vous permet d’extraire et d’analyser les URLs `page_location` du dataset, avec les informations suivantes :
    - paramètres présents,
    - domaines et fragments,
    - URLs en doublon ou trop longues,
    - résumé synthétique par URL.

    👉 Ce module est accessible via l’onglet **Validity : page_location**.

    ---
    """)

    # Présentation du fonctionnement par chapitres
    st.markdown("""
    ### 📚 Une approche par chapitres

    Cette application évoluera progressivement sous la forme de **chapitres**.  
    Chaque module viendra enrichir votre audit GA4, avec un focus précis (comme un livre que vous écrivez, page après page).

    🎯 **Objectif final :** vous permettre d’automatiser un audit complet GA4 à partir des données brutes, **sans modification manuelle** de la structure source.

    ---

    🧪 N'hésitez pas à tester le module actuel et à partager vos retours.  
    D'autres chapitres arrivent très bientôt ! 🚧
    """)

    # Pied de page avec contact
    st.markdown("""
        <div class="footer">
            💬 Une question, un besoin ou envie d’échanger sur la donnée ?<br>
            👉 <a href="https://www.linkedin.com/in/empirik-sylvain-rouxel/" target="_blank">Contactez-moi sur LinkedIn</a><br><br>
            Créé avec ❤️ par <strong>Sylvain Rouxel</strong>
        </div>
    """, unsafe_allow_html=True)
