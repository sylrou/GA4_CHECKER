import streamlit as st
import duckdb
import pandas as pd
import os

from services import sql_requests
from services import google_analytics_catalogue as dc
from assets.ui import ui_warning

st.title("🗺️ Analyse - Vue globale")

# Vérification de la base de données
db_path = os.path.abspath("../ga4.duckdb")
if not os.path.exists(db_path):
    ui_warning()
    st.stop()

# Connexion à la base
GA4_DATA = "ga4_data"
with st.spinner("Connexion à DuckDB..."):
    con = duckdb.connect(database=db_path, read_only=True)


    # -- Construction des colonnes ---
    users_col, sessions_col, date_col = st.columns(3)

    # --- Utilisateurs ---
    with users_col:
        st.subheader("👤 Nombre d'utilisateurs")
        with st.spinner("Requête en cours..."):
            df_user = con.execute(sql_requests.m_users(GA4_DATA)).fetchone()[0]
            st.metric("Utilisateurs uniques", df_user if df_user else 0, help="Basé sur user_pseudo_id", border=True)

    # --- Sessions ---
    with sessions_col:
        st.subheader("📊 Nombre de sessions")
        with st.spinner("Requête en cours..."):
            df_session = con.execute(sql_requests.m_sessions(GA4_DATA)).fetchone()[0]
            st.metric("Sessions uniques", df_session if df_session else 0, help="Basé sur session_id", border=True)

    # --- Dates ---
    with date_col:
        st.subheader("📅 Période couverte")
        with st.spinner("Requête en cours..."):
            df_date = con.execute(sql_requests.m_date(GA4_DATA)).fetchone()
            df_event_date = con.execute(sql_requests.d_event_date(GA4_DATA)).fetchdf()
            st.metric("Nombre de dates différentes", df_date[0], border=True)
            st.info(f"Période du {min(df_event_date['event_date'])} au {max(df_event_date['event_date'])}")


    # --- Noms des événements ---
    st.subheader("🎯 Noms d'événements détectés")
    with st.spinner("Requête en cours..."):
        df_event_name = con.execute(sql_requests.m_event_name(GA4_DATA)).fetchdf()

    event_col1, event_col2, event_col3 = st.columns(3)
    with event_col1:
        st.metric("Nombre d'événements différents", len(df_event_name), border=True)
    with event_col2:
        st.metric("Nombre total d'événements", df_event_name['event_count'].sum(), border=True)
    with st.expander("Afficher les événements"):
        st.dataframe(df_event_name, use_container_width=True)

    # --- Typologie du dataset ---
    p_ecommerce = sum([1 for k in dc.GA4_RECOMMENDED_EVENT_ECOMMERCE.keys() if k in df_event_name['event_name'].values])
    p_lead_gen = sum([1 for k in dc.GA4_RECOMMENDED_EVENT_LEAD_GEN.keys() if k in df_event_name['event_name'].values])
    p_game = 0  # À implémenter plus tard

    p_dic = {"E-commerce": p_ecommerce, "Lead Generation": p_lead_gen, "Gaming": p_game}
    best_type = max(p_dic, key=p_dic.get)
    st.success(f"Ce dataset semble être de type **{best_type}** avec {p_dic[best_type]} événements correspondants")

    # --- Événements recommandés manquants ---
    st.subheader("📌 Événements recommandés manquants en fonction de votre type de donnée")

    if best_type == 'Lead Generation' and p_dic['E-commerce'] == 0:
        with st.expander("💡 Améliorez votre tracking Lead Generation en ajoutant les événements suivants :"):
            for k, v in dc.GA4_RECOMMENDED_EVENT_LEAD_GEN.items():
                if k not in df_event_name['event_name'].values:
                    st.write(f"- `{k}` : {v}")
    elif best_type == 'E-commerce' and p_dic['Lead Generation'] == 0:
        with st.expander("🛒 Améliorez votre tracking E-commerce en ajoutant les événements suivants :"):
            for k, v in dc.GA4_RECOMMENDED_EVENT_ECOMMERCE.items():
                if k not in df_event_name['event_name'].values:
                    st.write(f"- `{k}` : {v}")
    else :
        with st.expander("💡 Améliorez votre tracking Lead Generation en ajoutant les événements suivants :"):
            for k, v in dc.GA4_RECOMMENDED_EVENT_LEAD_GEN.items():
                if k not in df_event_name['event_name'].values:
                    st.write(f"- `{k}` : {v}")
        with st.expander("🛒 Améliorez votre tracking E-commerce en ajoutant les événements suivants :"):
            for k, v in dc.GA4_RECOMMENDED_EVENT_ECOMMERCE.items():
                if k not in df_event_name['event_name'].values:
                    st.write(f"- `{k}` : {v}")

    # --- Liste des event_params ---
    st.subheader("🧾 Liste des 'Dimensions personnalisées' distinctes")
    with st.spinner("Requête en cours..."):
        df_event_params = con.execute(sql_requests.distinct_event_params_list(GA4_DATA)).fetchdf()
        key_event_params_list = sorted([k.replace('"', '') for k in df_event_params['key']])
        st.metric("Paramètres distincts", len(key_event_params_list), border=True)
        st.data_editor(pd.DataFrame(key_event_params_list, columns=["event_param"]), use_container_width=True)
        st.download_button("📥 Télécharger les event_params", data=pd.DataFrame(key_event_params_list).to_csv(index=False), file_name="ga4_event_params.csv")

    con.close()
