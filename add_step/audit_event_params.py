# Analyse des paramètres event_params dans GA4
import streamlit as st
import altair as alt
import duckdb
import pandas as pd

from services import sql_requests
from services.functions import safe_query_wrapper, get_ga4_connection_or_stop
from assets.ui import ui_warning, ui_caption, ui_sep

GA4_DATA = "ga4_data"

# --- En-tête ---
st.title("🔍 Analyse des `event_params` (dimensions personnalisées)")

st.markdown("""
Cette analyse vous permet de vérifier si une **dimension personnalisée** (comme `category_page`) est bien envoyée sur chaque événement GA4 (ex : `page_view`).

Cela permet de :
- **Détecter des absences de données** sur des événements censés les contenir.
- **Identifier des erreurs d’implémentation** dans le dataLayer ou GTM.

### Explication :
Si une dimension est attendue sur un événement donné, alors :

> 🟢 Nombre d’événements = Nombre d’occurrences de cette dimension

Sinon, un **écart (delta)** est observé, signalant un problème potentiel.
""")

# --- Connexion à la base ---
with st.spinner("🔌 Connexion à la base DuckDB..."):
    con = get_ga4_connection_or_stop()

# --- Chargement des données ---
with st.spinner("📥 Récupération des données..."):
    df_custom_dimension = safe_query_wrapper(
        lambda: con.execute(sql_requests.event_and_customdim_checker(GA4_DATA)).df()
    )

# --- Nettoyage des clés ---
df_custom_dimension["key"] = df_custom_dimension["key"].str.replace('"', '', regex=False)

# --- Filtres dynamiques ---
available_events = sorted(df_custom_dimension["event_name"].unique())
available_keys = sorted(df_custom_dimension["key"].unique())

# Clés exclues de la sélection par défaut
excluded_keys_default = [
    "batch_ordering_id", "batch_page_id", "campaign",
    "engaged_session_event", "engagement_time_msec", "entrances",
    "ignore_referrer", "link_classes", "link_domain", "link_id", "link_url",
    "medium", "outbound", "page_referrer", "percent_scrolled",
    "session_engaged", "source", "term"
]
# Sélection par défaut : tout sauf celles exclues
default_keys = [key for key in available_keys if key not in excluded_keys_default]

ui_sep()
# --- Filtres dynamiques avec colonnes et checkboxes ---
st.markdown("## 🎯 Filtres d’analyse")

# Mise en page en deux colonnes
col1, col2 = st.columns(2)

with col1:
    st.subheader("Filtre via le nom de l'événement")
    select_all_events = st.checkbox("Sélectionner tous les événements (`event_name`)", value=True)
    selected_events = st.multiselect(
        "Événements à analyser (`event_name`) :",
        options=available_events,
        default=available_events if select_all_events else [],
        key="multiselect_event_name"
    )

with col2:
    st.subheader("Filtre via le nom de la dimension")
    select_all_keys = st.checkbox("Sélectionner toutes les dimensions (`event_params.key`)", value=True)
    selected_keys = st.multiselect(
        "Dimensions personnalisées (`event_params.key`) :",
        options=available_keys,
        default=default_keys if select_all_keys else [],
        key="multiselect_event_key"
    )
    st.caption("""
    ℹ️ Certaines dimensions sont exclues par défaut car elles n'ont pas vocation à être dans tous les événement.
    (ex. `campaign`, `source`, `link_url`, etc.).

    👉 Vous pouvez bien sûr les inclure manuellement si nécessaire.
    """)

ui_sep()
st.markdown("""
### Filtre pour afficher uniquement les lignes avec un delta > 0
""")
show_only_delta = st.checkbox("Afficher seulement les delta > 0", value=True)
ui_sep()

# --- Filtrage des données ---
filtered_df = df_custom_dimension[
    df_custom_dimension["event_name"].isin(selected_events) &
    df_custom_dimension["key"].isin(selected_keys)
].copy()

# --- Calcul du delta ---
filtered_df["delta"] = filtered_df["total_event"] - filtered_df["custom_dim_number"]

# --- Application du filtre delta > 0 si demandé ---
if show_only_delta:
    filtered_df = filtered_df[filtered_df["delta"] > 0]

# --- Exploration globale ---
st.markdown("## 📋 Exploration filtrée des dimensions")
st.data_editor(filtered_df, use_container_width=True)

st.download_button(
    label="📄 Télécharger les résultats filtrés (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="ga4_custom_dimensions_filtered.csv"
)

# --- Graphique si données présentes ---
if not filtered_df.empty:
    st.markdown(f"""
    ## 📊 Visualisation des clés sélectionnées

    Ce graphique compare le nombre total d’événements à celui où chaque dimension est bien renseignée.

    - 🟩 Présente : événements avec la dimension
    - 🟥 Absente : événements sans la dimension
    - Un écart (**delta**) important peut indiquer un problème d’implémentation ou de déclenchement.
    """)
    ui_sep()

    # Préparer les données pour Altair (empiler Présente / Absente)
    melted_df = pd.concat([
        filtered_df[["event_name", "key", "custom_dim_number"]]
        .rename(columns={"custom_dim_number": "value"})
        .assign(type="Présente"),

        filtered_df[["event_name", "key", "delta"]]
        .rename(columns={"delta": "value"})
        .assign(type="Absente")
    ])

    # Créer une clé combinée pour l'axe Y
    melted_df["event_key"] = melted_df["event_name"] + " | " + melted_df["key"]

    # Tri personnalisé : delta décroissant (événements les plus critiques en haut)
    order = (
        filtered_df
        .assign(event_key=filtered_df["event_name"] + " | " + filtered_df["key"])
        .sort_values("delta", ascending=False)["event_key"]
        .unique()
    )

    # Calcul plus rigoureux basé sur les combinaisons event_name + key
    n_combinations = filtered_df[["event_name", "key"]].drop_duplicates().shape[0]
    chart_height = max((n_combinations * 50),300)

    # Création du graphique Altair
    chart = alt.Chart(melted_df).mark_bar().encode(
        x=alt.X("value:Q", title="Nombre d'événements"),
        y=alt.Y("event_key:N", sort=order.tolist(), title="Événement | Dimension"),
        color=alt.Color("type:N", scale=alt.Scale(
            domain=["Présente", "Absente"],
            range=["#00cc66", "#cc0000"]
        )),
        tooltip=["event_name", "key", "type", "value"]
    ).properties(
        width=800,
        height=chart_height,
        title="Présence des dimensions personnalisées par événement"
    )

    # Affichage dans Streamlit
    st.altair_chart(chart, use_container_width=True)

else:
    st.info("Aucune donnée à afficher avec les filtres actuels.")

# --- Fermeture & pied de page ---
con.close()
ui_caption()
