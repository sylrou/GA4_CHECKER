import streamlit as st
from assets.ui import ui_footer, ui_btn_link, ui_sep

st.title('Bienvenue sur GA4 Checker 🕵️ - 100% Gratuit & 100% Open source')

# Introduction générale
st.markdown("""
GA4 Checker est une application conçue pour vous accompagner dans l’analyse et l’audit de vos données **Google Analytics 4**, à partir des exports bruts de BigQuery.
""")

ui_sep()

# Comment utiliser l'application
st.markdown("""
## Comment utiliser l'application ?

Rendez-vous dans l’onglet **📂 Importer votre fichier** pour :
- utiliser le **jeu de démonstration**, ou
- **importer vos propres données GA4** exportées depuis BigQuery.

## Comment importer votre propre jeu de données ?

1. Dans **BigQuery**, effectuez la requête suivante (en filtrant si besoin pour rester sous **1 Go**).
""")
st.code(
        """
    SELECT * FROM `votre-projet.analytics_123456.events_YYYYMMDD`
    """,
        language="sql"
)
st.image('assets/how_to_import_0.png')
st.markdown("""
2. Cliquez sur **"Enregistrer les résultats"**, puis choisissez :
   - **Destination** : Google Drive
   - **Format** : **JSONL (JSON délimité par un retour à la ligne)**
   (Voir capture)
""")
st.image('assets/how_to_import_1.png')
st.warning("""⚠️ Attention : importer un fichier JSON classique au lieu du format JSONL provoquera une erreur.""")
st.markdown("""
    - Vous allez voir le message suivant de la part de BigQuery :
""")
st.image('assets/how_to_import_2.png')
st.markdown("""
    - Attendez de voir le message suivant et cliquez sur le lien pour accéder à la sauvegarde dans votre drive
""")
st.image('assets/how_to_import_3.png')
st.markdown("""
3. Téléchargez votre fichier JSON qui commence par 'bq-results...'
""")
st.image('assets/how_to_import_4.png')
st.markdown("""
4. Importez ce fichier dans **GA4Checker** via l'interface.
""")
st.warning("⚠️ Attention : importer un fichier JSON classique au lieu du format JSONL provoquera une erreur.")
st.markdown("""
Une fois le fichier importé :
- Consultez les **rapports d’audit** générés automatiquement
- Ou utilisez l’outil d’**exploration libre** pour analyser vos données comme vous le souhaitez.
""")

ui_sep()

# --- Bloc pour la dernière mise à jour ---
st.markdown("""
## Dernière mise à jour
""")

st.badge("📂 Nouvelle mise à jour du 11/05/2025")
st.markdown("""
🎉 **Long week-end productif pour GA4Checker** : plusieurs améliorations clés ont été apportées à l’outil pour le rendre plus fiable, plus pédagogique et plus simple à utiliser.

### Nouveau jeu de données de démonstration
- Mise à jour du dataset de démonstration avec des cas d’usage:
    - Duplication de paramètres d’URL
    - URLs trop longues
    - Présence de paramètres critiques (`token`, `id utilisateur`, etc.)
    - et bien plus encore…
- Permet à l’utilisateur de **tester l’application sans importer sa propre donnée**.

### Analyse avancée des `event_params`
- Ajout d’un **pourcentage de données manquantes** pour identifier les erreurs d’implémentation.
- Interface retravaillée pour plus de lisibilité et une meilleure interprétation des résultats.

### Interface enrichie avec le "mode détective"
- Les messages clés apparaissent désormais sous forme de **bulles “détective”** (emoji + conseil contextuel).
- Présent dans toute l’application (dates obsolètes, taux de complétion bas, etc.).

### Refonte complète de la page d’import
- Réinitialisation automatique de la base DuckDB possible à tout moment.
- Flux d’import repensé pour **éviter les erreurs de session**.
- Interface simplifiée avec des messages adaptés à chaque étape.

➡️ Testez ces nouveautés dès maintenant dans les sections **📂 Importer votre fichier** ou **Analyse des `event_params`** !
""")
ui_btn_link("add_step/data_import.py", "Importer votre fichier")

ui_sep()

# --- Mises à jour précédentes ---
st.markdown("""## Mises à jour précédentes""")

with st.expander("📂 Mise à jour du 04/05/2025 - Amélioration de l'exploration SQL libre"):
    st.markdown("""
    Une **nouvelle interface d'exploration SQL** vient enrichir votre outil d'analyse GA4 !  
    **Explorez librement vos données ou utilisez nos requêtes pré-remplies.**
    """)

    st.markdown("""
    ### Exploration SQL libre améliorée
    Vous pouvez maintenant :
    - **Écrire vos propres requêtes SQL** dans un éditeur enrichi avec **coloration syntaxique**
    - Choisir un thème foncé plus lisible (`tomorrow_night_blue`)
    - **Utiliser une liste de requêtes pré-enregistrées** pour obtenir rapidement des insights utiles

    ### Requêtes pré-enregistrées disponibles
    Accédez en un clic à des métriques clés comme :
    - Le nombre total de sessions
    - Le nombre d’utilisateurs uniques
    - Les événements distincts
    - Les pages consultées (`page_location`)
    - Et bien plus…

    ### Pourquoi c’est utile ?
    Cette nouvelle section permet :
    - de **tester vos hypothèses** directement sur vos exports JSON,
    - de **vérifier rapidement la qualité de vos données**,
    - ou tout simplement d’explorer votre tracking GA4 sans quitter l’interface.

    ➡️ Allez tester la nouvelle interface via l’onglet **Exploration SQL libre** dans le menu.
    """)

    ui_btn_link("add_step/explore.py", "Exploration libre")

with st.expander("📂 Mise à jour du 03/05/2025 - Nouvelle fonctionnalité"):
    st.markdown("""
    Une **nouvelle fonctionnalité** fait son apparition :  
    🎯 **Audit des dimensions personnalisées (`event_params`)**
    """)
    st.markdown("""
    Cette page vous permet d’analyser la **présence et la cohérence des dimensions personnalisées** dans vos événements GA4.

    ### À quoi ça sert ?
    Certaines dimensions personnalisées (ex. `category_page`, `user_type`, etc.) devraient apparaître **systématiquement** sur certains événements comme `page_view`.  
    Ce module vous aide à **vérifier si c’est bien le cas**, et à identifier les anomalies.

    ### Ce que vous pouvez faire :
    - Choisir dynamiquement une dimension personnalisée à analyser
    - Comparer le nombre d’événements avec et sans cette dimension
    - Visualiser les résultats dans un **graphique empilé** :
        - 🟩 Vert : la dimension est bien présente
        - 🟥 Rouge : la dimension est absente (delta)
    - Filtrer les événements avec un delta significatif pour se concentrer sur les problèmes les plus importants
    - Exporter les résultats en CSV

    Ce module vous permet de détecter rapidement :
    - des erreurs dans le dataLayer ou dans GTM,
    - des implémentations partielles,
    - ou des données absentes non conformes au plan de marquage.

    ➡️ Accédez à ce rapport depuis :
    """)
    ui_btn_link("add_step/audit_event_params.py", "Analyse - event_params")

with st.expander("📂 Mise à jour du 02/05/2025 - Amélioration de l'UI/UX"):
    st.markdown("""
    L'application évolue pour offrir une expérience plus fluide et intuitive :

    - **Refonte du menu de navigation** : les rapports sont désormais accessibles via une interface claire et directe, pour une meilleure lisibilité.
    - **Refonte des codes couleurs** : "Quitte à refactoriser l'app, autant éviter qu'elle pique les yeux." 😎
    - **Netlinking interne optimisé** : les liens vers les pages principales sont désormais mieux intégrés dans l’interface, pour favoriser la circulation entre les modules.
    - **Amélioration de l'outil d’exploration** : la zone de requête SQL a été retravaillée pour faciliter l’écriture, avec une meilleure mise en page et une vue plus confortable.
    - **Système de feedback** : une première version du système de remontée de retours a été mise en place pour recueillir vos suggestions et améliorer l’outil en continu.
    
    Merci d'avance pour vos retours 🙌
    """)

with st.expander("📂 Mise à jour du 22/04/2025 - Vue d'ensemble du fichier"):
    st.markdown("""
    Une nouvelle page fait son apparition : **Premier coup d'oeil**  
    Elle permet d’obtenir une **vue d’ensemble immédiate** sur les éléments clés de votre fichier :
    - Nombre d’utilisateurs et de sessions  
    - Période couverte  
    - Liste des événements détectés  
    - Typologie supposée du dataset (e-commerce, lead gen…)  
    - Événements recommandés manquants  
    - Paramètres d’événements (`event_params`) distincts

    Ce module est idéal pour un **premier diagnostic rapide**, avant d’explorer plus en détail chaque aspect de vos données.
    """)

with st.expander("📂 Mise à jour du 20/04/2025 - Données de démonstration"):
    st.markdown("""
    Vous pouvez désormais utiliser un jeu de données de démonstration pour tester l'application.  
    Rendez-vous dans l’onglet dédié pour importer votre propre fichier ou explorer l'exemple fourni.

    Il est également possible d’utiliser la fonction d’exploration libre pour consulter en détail votre jeu de données
    via des requêtes SQL.

    Pour les fichiers supérieurs à 1Go, contactez-moi pour une utilisation en local.  
    Cela permet de débloquer la limite de taille imposée par Streamlit (mais reste dépendant des performances de votre machine).
    """)

with st.expander("📂 Mise à jour du 18/04/2025 - Audit du page_location"):
    st.markdown("""
    Le **premier module** est désormais disponible en phase de test :  
    Il vous permet d’extraire et d’analyser les URLs `page_location` du dataset, avec les informations suivantes :
    - paramètres présents,
    - domaines et fragments,
    - URLs en doublon ou trop longues,
    - résumé synthétique par URL.

    Ce module est accessible via l’onglet **🔗 Audit du page_location**.
    """)

ui_sep()

# Présentation du fonctionnement par chapitres
st.markdown("""
### Une application en évolution continue

Cette application évoluera progressivement sous la forme de **feature**.  
Chaque module viendra enrichir votre audit GA4, avec un focus précis (comme un livre que vous écrivez, page après page).

**Objectif final :** vous permettre d’automatiser un audit complet GA4 à partir des données brutes, **sans modification manuelle** de la structure source 
ou une exploration via des requêtes pré-programmées.
""")

ui_sep()

# Pied de page avec contact
ui_footer()
