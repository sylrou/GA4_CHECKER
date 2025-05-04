from datetime import datetime
import streamlit as st

def ui_footer():
    st.markdown("""
    <div class="footer">
        💬 Une question, un besoin ou envie d’échanger ?<br>
        👉 <a href="https://www.linkedin.com/in/empirik-sylvain-rouxel/" target="_blank">Contactez-moi sur LinkedIn</a><br><br>
        Créé avec ❤️ par <strong>Sylvain Rouxel</strong> et l'aide de la communauté
    </div>
    """, unsafe_allow_html=True)

def ui_btn_link(path, label):
    st.page_link(f"{path}", label=f"{label}", icon="🔗", help='Lien vers cette page')

def ui_warning():
    return st.warning("⚠️ Vous n'avez encore importé aucune donnée. Pas de souci ! \n Allez sur la page d'import pour ajouter vos données, ou testez l'application avec notre exemple de démo.")

def ui_caption():
    st.markdown("---")
    st.caption("✨ GA4Checker (version **Alpa**) est un projet open-source, évolutif, et fait avec passion.")

def ui_sep():
    st.markdown("---")
