import streamlit as st
import duckdb
import pandas as pd
import os
import string
import altair as alt
from streamlit import columns

from services import sql_requests
from services import google_analytics_catalogue as dc
from assets.ui import ui_warning, ui_caption
from services.functions import safe_query_wrapper

st.title("🗺️ Analyse - Vue globale")

# Vérification de la base de données
db_path = os.path.abspath("../ga4.duckdb")
if not os.path.exists(db_path):
    ui_warning()
    st.stop()

# Connexion à la base
GA4_DATA = "ga4_data"
with st.spinner("Connexion à DuckDB..."):
    con = safe_query_wrapper(
        lambda :duckdb.connect(database=db_path, read_only=True),
        "Erreur lors de la connexion"
    )


    # -- Construction des colonnes ---
    users_col, sessions_col, date_col = st.columns(3)

    # --- Utilisateurs ---
    with users_col:
        st.subheader("👤 Nombre d'utilisateurs")
        with st.spinner("Requête en cours..."):
            total_user = safe_query_wrapper(
                lambda: con.execute(sql_requests.m_users(GA4_DATA)).fetchone()[0]
            )
            st.metric("Utilisateurs uniques", total_user if total_user else 0, help="Basé sur user_pseudo_id", border=True)

    # --- Sessions ---
    with sessions_col:
        st.subheader("📊 Nombre de sessions")
        with st.spinner("Requête en cours..."):
            total_session = safe_query_wrapper(
                lambda:con.execute(sql_requests.m_sessions(GA4_DATA)).fetchone()[0]
            )
            st.metric("Sessions uniques", total_session if total_session else 0, help="Basé sur session_id", border=True)

    # --- Dates ---
    with date_col:
        st.subheader("📅 Période couverte")
        with st.spinner("Requête en cours..."):
            total_date = safe_query_wrapper(
                lambda:con.execute(sql_requests.m_date(GA4_DATA)).fetchone()
            )
            df_event_date = safe_query_wrapper(
                lambda:con.execute(sql_requests.d_event_date(GA4_DATA)).fetchdf()
            )
            st.metric("Nombre de dates différentes", total_date[0], border=True)
            st.info(f"Période du {min(df_event_date['event_date'])} au {max(df_event_date['event_date'])}")



    # --- Noms des événements ---
    st.subheader("🎯 Noms d'événements détectés")
    with st.spinner("Requête en cours..."):
        df_event_name = safe_query_wrapper(
                lambda:con.execute(sql_requests.m_event_name(GA4_DATA)).fetchdf()
        )
    event_col1, event_col2, event_col3 = st.columns(3)
    with event_col1:
        st.metric("Nombre d'événements différents", len(df_event_name), border=True)
    with event_col2:
        st.metric("Nombre total d'événements", df_event_name['event_count'].sum(), border=True)
    with st.expander("Afficher les événements"):
        df_event_name_sorted = df_event_name.copy().sort_values("event_count", ascending=False)

        #Préparation du graphique altair
        base = alt.Chart(df_event_name_sorted).encode(
            x="event_count:Q",
            y=alt.Y("event_name:N", sort="-x")
        )

        bars = base.mark_bar(color="#00cc66")

        labels = base.mark_text(
            align="left",
            baseline="middle",
            dx=3, # décalage horizontal pour ne pas coller à la barre
            color = "white"
        ).encode(
            text="event_count:Q"
        )
        #Affichage du graphique
        st.altair_chart(bars + labels, use_container_width=True)

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
        df_event_params = safe_query_wrapper(
                lambda:con.execute(sql_requests.distinct_event_params_list(GA4_DATA)).fetchdf()
        )
        #Préparation de la liste pour mcol1 (metric colonnes 1)
        key_event_params_list = sorted([k.replace('"', '') for k in df_event_params['key']])
        # Préparation de la liste pour mcol1 (metric colonnes 2)
        count_standard = 0
        extract_standard = [k for k in dc.event_params_dict.keys()]
        for x in key_event_params_list:
            if x in extract_standard:
                count_standard += 1

        # Gestion de l'affichage des colonnes
        mcol1, mcol2, mcol3 = columns(3)
        with mcol1:
            st.metric("Nombre total de paramètres dans event_params", len(key_event_params_list), border=True)
        with mcol2:
            st.metric("Nombre total de paramètres classiques", int(count_standard), border=True)
        with mcol3:
            st.metric("Nombre total de paramètres personnalisés", len(key_event_params_list) - count_standard, border=True)
        # Gestion de l'affichage de la liste des event_params
        with st.expander("💡 Affichez la liste des paramètres d'événements disponibles dans le Dateset :"):
            st.data_editor(pd.DataFrame(key_event_params_list, columns=["event_param"]), use_container_width=True)
        st.download_button("📥 Télécharger les event_params", data=pd.DataFrame(key_event_params_list).to_csv(index=False), file_name="ga4_event_params.csv")

    con.close()

ui_caption()