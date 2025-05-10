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
    st.page_link(
        f"{path}",
        label=f"{label}",
        icon="🔗",
        help='Lien vers cette page'
    )

def ui_warning():
    return st.warning("⚠️ Vous n'avez encore importé aucune donnée. Pas de souci ! \n Allez sur la page d'import pour ajouter vos données, ou testez l'application avec notre exemple de démo.")

def ui_detective_tip(message: str):
    st.markdown(f"""
    <div style="display: flex; align-items: flex-start; margin: 1em 0;">
        <div style="font-size: 2rem; margin-right: 12px;">🕵️</div>
        <div style="
            background-color: #12293B;
            color: #FFFFFF;
            padding: 12px 16px;
            border-radius: 12px;
            border: 1px solid #d0d0d0;
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05);
            flex: 1;
        ">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def ui_caption():
    st.markdown("---")
    st.caption("✨ GA4Checker (version **Alpa**) est un projet open-source, évolutif, et fait avec passion.")

def ui_sep():
    st.markdown("---")

def ui_audit_netlinkink():
    st.markdown('Vous pouvez maintenant vous dirigez vers :')
    btn1, btn2, btn3 = st.columns(3)
    with btn1:
        ui_btn_link("add_step/audit_overview.py", "Analyse - Vue globale")
    with btn2:
        ui_btn_link("add_step/audit_page_location.py", "Analyse - page_location")
    with btn3:
        ui_btn_link("add_step/audit_event_params.py", "Analyse - event_params")

# ui.py ou assets/ui.py

