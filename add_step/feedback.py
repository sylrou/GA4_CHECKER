import streamlit as st
from datetime import date

# --- Contenu de la page ---
st.title("💡 Proposez une amélioration !")
st.markdown("---")

st.markdown(
    """
    Vous avez une idée, une suggestion ou un besoin spécifique pour améliorer l'app **GA4Checker** ?  
    Votre retour est essentiel pour faire évoluer l'outil au plus proche de vos usages. 🧠✨

    👉 Remplissez le formulaire ci-dessous pour proposer une **feature**, suggérer une **amélioration UX**, ou signaler un **bug** :
    """
)

st.link_button("📝 Remplir le formulaire Google", "https://docs.google.com/forms/d/e/1FAIpQLSflgaNI4c_SjCECVzIM78DQuqd-UmyuNyHSFbDZ99YGe58pbQ/viewform?usp=header")

st.markdown("---")
st.caption(f"Merci pour votre contribution ! 🙌 — {date.today().strftime('%d/%m/%Y')}")
