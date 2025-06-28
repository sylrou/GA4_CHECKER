import streamlit as st
from assets.ui import ui_caption

# --- Petit effet sympa à chaque chargement ---
st.balloons()

# --- Titre principal ---
st.title("🤝 Remerciements")

# --- Introduction ---
st.markdown("""
Bienvenue sur la page des remerciements du projet **GA4Checker**.  
Ce projet est open-source, mais surtout une belle aventure humaine 🙌  
Merci à toutes celles et ceux qui, de près ou de loin, ont contribué à sa création et son évolution.
""")

st.markdown("---")

# --- Special thanks ---
st.subheader("🤍 Very special thanks")
st.markdown("""
- **Yannick Darcy** — Pour son soutien indéfectible et sans qui aucune ligne de code ne serait jamais en production.
- **Jonathan Mary** — Pour m'avoir (généreusement 😅) forcé à suivre *Introduction to Computer Science with Python* du MIT.
- **Corentin Deschamps** — Pour avoir partagé cette aventure de formation avec moi.
""")

# --- Contributions ---
st.subheader("🧠 Contributions & Soutiens")
st.markdown("""
- **Sébastien Monnier**
- **Lucas Rollin**
- **Daniel Valide**
- **Christian Laville**
- **Clément Tabard**
- **Benjamin Dubreu et dataUpskill**
- **Gaël Penessot et son livre**
- **L'AADF - Association des analystes de France**

- **Toutes les personnes qui partagent leurs idées, retours, et leur temps.**
""")

# --- Appel à contribution ---
st.markdown("""
**Et vous ?**  
Si vous avez des idées, des remarques, ou l’envie de contribuer, n'hésitez pas à me contacter !
""")

ui_caption()