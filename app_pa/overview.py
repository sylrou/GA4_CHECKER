import streamlit as st
import duckdb
import pandas as pd
import os

from services import sql_requests
from services import google_analytics_catalogue as dc

def show():
    st.title("🗺️ Overview - Premier coup d'oeil")

    # Vérification de la base de données
    db_path = os.path.abspath("ga4.duckdb")
    if not os.path.exists(db_path):
        st.error("Aucune base de données trouvée. Veuillez d'abord importer un fichier via la page d'import.")
        st.stop()

    # Connexion à la base
    with st.spinner("Connexion à DuckDB..."):
        con = duckdb.connect(database=db_path, read_only=True)

    GA4_DATA = "ga4_data"

    # --- Utilisateurs ---
    st.subheader("👤 Nombre d'utilisateurs")
    df_user = con.execute(sql_requests.m_users(GA4_DATA)).fetchone()[0]
    st.metric("Utilisateurs uniques", df_user if df_user else 0, help="Basé sur user_pseudo_id")

    # --- Sessions ---
    st.subheader("📊 Nombre de sessions")
    df_session = con.execute(sql_requests.m_sessions(GA4_DATA)).fetchone()[0]
    st.metric("Sessions uniques", df_session if df_session else 0, help="Basé sur session_id")

    # --- Dates ---
    st.subheader("📅 Période couverte")
    df_date = con.execute(sql_requests.m_date(GA4_DATA)).fetchone()
    df_event_date = con.execute(sql_requests.d_event_date(GA4_DATA)).fetchdf()
    st.metric("Nombre de dates différentes", df_date[0])
    st.info(f"Période allant du {min(df_event_date['event_date'])} au {max(df_event_date['event_date'])}")

    # --- Noms des événements ---
    st.subheader("🎯 Noms d'événements détectés")
    df_event_name = con.execute(sql_requests.event_name_extract(GA4_DATA)).fetchdf()
    st.metric("Nombre d'événements différents", len(df_event_name))
    with st.expander("Afficher les événements"):
        st.dataframe(df_event_name, use_container_width=True)

    # --- Typologie du dataset ---
    p_ecommerce = sum([1 for k in dc.GA4_RECOMMENDED_EVENT_ECOMMERCE.keys() if k in df_event_name['event_name'].values])
    p_lead_gen = sum([1 for k in dc.GA4_RECOMMENDED_EVENT_LEAD_GEN.keys() if k in df_event_name['event_name'].values])
    p_game = 0  # À implémenter plus tard

    p_dic = {"E-commerce": p_ecommerce, "Lead Gen": p_lead_gen, "Gaming": p_game}
    best_type = max(p_dic, key=p_dic.get)
    st.success(f"Ce dataset semble être de type **{best_type}** avec {p_dic[best_type]} événements correspondants")

    # --- Événements recommandés manquants ---
    st.subheader("📌 Événements recommandés manquants")
    with st.expander("E-commerce"):
        for k, v in dc.GA4_RECOMMENDED_EVENT_ECOMMERCE.items():
            if k not in df_event_name['event_name'].values:
                st.write(f"\- `{k}` : {v}")
    with st.expander("Lead Gen"):
        for k, v in dc.GA4_RECOMMENDED_EVENT_LEAD_GEN.items():
            if k not in df_event_name['event_name'].values:
                st.write(f"\- `{k}` : {v}")

    # --- Liste des event_params ---
    st.subheader("🧾 Liste des event_params distincts")
    df_event_params = con.execute(sql_requests.distinct_event_params_list(GA4_DATA)).fetchdf()
    key_event_params_list = sorted([k.replace('"', '') for k in df_event_params['key']])
    st.metric("Paramètres distincts", len(key_event_params_list))
    st.dataframe(pd.DataFrame(key_event_params_list, columns=["event_param"]), use_container_width=True)
    st.download_button("📥 Télécharger les event_params", data=pd.DataFrame(key_event_params_list).to_csv(index=False), file_name="ga4_event_params.csv")

    con.close()
