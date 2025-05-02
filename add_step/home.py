import streamlit as st

st.title('Bienvenue sur GA4 Checker 🕵️')

# Introduction générale
st.markdown("""
GA4 Checker est une application conçue pour vous accompagner dans l’analyse et l’audit de vos données **Google Analytics 4**, à partir des exports bruts de BigQuery.

---
""")

# Comment utiliser l'application
st.markdown("""
### Comment utiliser l'application ?

Rendez-vous dans l'onglet **📂 Importer les données GA4** pour utiliser le jeu de données de démonstration de mon ancien site ou importer le vôtre.

### Comment importer votre propre jeu de données ?

1. Dans BigQuery, effectuez un `SELECT *` filtré pour ne pas dépasser **1 Go** de données.
2. Téléchargez le résultat au format **JSON**. Pour cela, enregistrez d'abord les résultats dans votre Google Drive, puis téléchargez-les manuellement.
3. Importez ce fichier dans GA4Checker via l’interface.

### Accéder aux audits

Une fois votre fichier importé, vous pouvez explorer vos données via les rapports disponibles.  
Vous pouvez maintenant utiliser les rapports suivants ou l'outil d'exploration de votre donnée.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("add_step/overview.py", label="Analyse - Vue globale", icon='🔗')
with col2:
    st.page_link("add_step/audit_page_location.py", label="Voir l'analyse page_location", icon='🔗')
with col3:
    st.page_link("add_step/explore.py", label="Outil d'exploration", icon='🔗')


st.markdown("""---""")

st.badge("Nouveau : 02/05/2025")

# Bloc sur les nouveautés du 02/05/2025 : Grosse refonte de la navigation
st.markdown("""
L'application évolue pour offrir une expérience plus fluide et intuitive :

- **Refonte du menu de navigation** : les rapports sont désormais accessibles via une interface claire et directe, pour une meilleure lisibilité.
- **Refonte des codes couleurs** : "Quitte à refactoriser l'app, autant éviter qu'elle pique les yeux." 😎
- **Netlinking interne optimisé** : les liens vers les pages principales sont désormais mieux intégrés dans l’interface, pour favoriser la circulation entre les modules.
- **Amélioration de l'outil d’exploration** : la zone de requête SQL a été retravaillée pour faciliter l’écriture, avec une meilleure mise en page et une vue plus confortable.
- **Système de feedback** : une première version du système de remontée de retours a été mise en place pour recueillir vos suggestions et améliorer l’outil en continu.

Merci d'avance pour vos retours 🙌
""")

st.markdown("""
### Avancement du projet et mise à jour
""")

# Badge de mise à jour
st.badge("Mise à jour : 22/04/2025", icon=":material/check:", color="gray")
# Nouvelle mise à jour : module d'audit technique
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

# Badge de mise à jour
st.badge("Mise à jour : 20/04/2025", icon=":material/check:", color="gray")

# Bloc sur la démonstration et l'import
st.markdown("""
Vous pouvez désormais utiliser un jeu de données de démonstration pour tester l'application.  
Rendez-vous dans l’onglet dédié pour importer votre propre fichier ou explorer l'exemple fourni.

Il est également possible d’utiliser la fonction d’exploration libre pour consulter en détail votre jeu de données
via des requêtes SQL.

Pour les fichiers supérieurs à 1Go, contactez-moi pour une utilisation en local.  
Cela permet de débloquer la limite de taille imposée par Streamlit (mais reste dépendant des performances de votre machine).
""")

# Badge de mise à jour
st.badge("Mise à jour : 18/04/2025", icon=":material/check:", color="gray")

# Description du premier module disponible
st.markdown("""
Le **premier module** est désormais disponible en phase de test :  
🔍 Il vous permet d’extraire et d’analyser les URLs `page_location` du dataset, avec les informations suivantes :
- paramètres présents,
- domaines et fragments,
- URLs en doublon ou trop longues,
- résumé synthétique par URL.

Ce module est accessible via l’onglet **🔗 Audit du page_location**.

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