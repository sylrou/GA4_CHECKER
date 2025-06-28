import duckdb
import streamlit as st
import os
import gc
import tempfile
import uuid

from assets.ui import ui_btn_link, ui_audit_netlinkink
from services.functions import safe_query_wrapper

# --- Bannière d'état en haut de page ---
def show_database_status():
    if st.session_state.get("ga4_ready"):
        st.success("✅ Données GA4 chargées et prêtes à être analysées.")
    else:
        st.warning("⚠️ Aucune base de données chargée pour l’instant.")

show_database_status()

# --- Réinitialisation possible si base déjà chargée ---
if st.session_state.get("ga4_ready") and "db_path" in st.session_state:
    st.markdown("#### Vous avez déjà importé une base")
    if st.button("🧨 Réinitialiser et importer une nouvelle donnée"):
        try:
            if os.path.exists(st.session_state.db_path):
                os.remove(st.session_state.db_path)
        except Exception as e:
            st.warning(f"Erreur lors de la suppression de la base : {e}")
        # Nettoyage de session_state
        for key in ["ga4_ready", "ga4_info", "db_path"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("✅ La session a été réinitialisée.")
        st.rerun()
    else:
        st.stop()

# --- Titre et header ---
st.header("📥 Importer les données GA4")
step = 1
dataset_type = 0
data_file = None

# --- Créer une base DuckDB unique pour cette session ---
if "db_path" not in st.session_state:
    st.session_state.db_path = os.path.join(
        tempfile.gettempdir(), f"ga4checker_{uuid.uuid4().hex}.duckdb"
    )
db_path = st.session_state.db_path

# --- Étape 1 : Choix de la source de donnée ---
local_data_path = os.path.abspath("raw_data/local_analysis.json")
if os.path.exists(local_data_path):
    data_file = local_data_path
    dataset_type = 1
    st.info(f"Etape {step} : Donnée locale activée automatiquement ✅")
    step += 1
else:
    # Option utilisateur : jeu de démonstration
    user_test_data = st.toggle("🔧 Activer le jeu de données de démonstration")
    if user_test_data:
        demo_path = os.path.abspath("raw_data/animalien_data.json")
        data_file = demo_path
        dataset_type = 2
        st.info(f"Etape {step} : Jeu de démonstration sélectionné ✅")
        step += 1
    else:
        # Upload sécurisé
        uploaded_file = st.file_uploader("📤 Importez votre export GA4 (JSON)", type="json")
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
                tmp.write(uploaded_file.getbuffer())
                data_file = tmp.name
            dataset_type = 3
            st.info(f"Etape {step} : Fichier JSON uploadé avec succès ✅")
            step += 1
        else:
            st.stop()

# --- Étape 2 : Création de la base temporaire ---
with st.spinner("⏳ Chargement du fichier dans DuckDB..."):
    con = safe_query_wrapper(lambda: duckdb.connect(database=db_path, read_only=False))
    con.execute("INSTALL json; LOAD json;")
    con.execute("DROP TABLE IF EXISTS ga4_data;")
    con.execute(f"""
        CREATE TABLE ga4_data AS
        SELECT * FROM read_ndjson('{data_file}', union_by_name=True)
    """)
    st.info(f"Etape {step} : Base DuckDB créée avec succès ✅")
    step += 1
    st.info(f"Etape {step} : 📂 Base temporaire enregistrée ici : `{db_path}`")
    step += 1

    # ✅ Mise à jour de session pour les autres pages
    st.session_state.ga4_ready = True
    st.session_state.ga4_info = {
        "dataset_type": dataset_type,
        "path": db_path,
        "event_count": con.sql("SELECT COUNT(*) FROM ga4_data").fetchone()[0]
    }

    with st.expander("📊 Affichez le schéma de votre import :"):
        st.dataframe(con.sql("PRAGMA table_info(ga4_data)").df())

    con.close()

# --- Étape 3 : Nettoyage fichier temporaire JSON ---
if dataset_type == 3 and data_file and os.path.exists(data_file):
    try:
        os.remove(data_file)
        st.info(f"Etape {step} - 🧹 Fichier temporaire JSON supprimé ✅")
        step += 1
    except Exception as e:
        st.warning(f"Erreur lors de la suppression du fichier temporaire : {e}")

# --- Étape 4 : Nettoyage mémoire manuelle ---
if dataset_type == 3:
    del uploaded_file
    gc.collect()
    st.info(f"Etape {step} - 💾 Mémoire libérée après chargement du fichier ✅")
    step += 1

# --- Fin du process ---
st.success("🎉 Données importées avec succès. Vous êtes prêt pour l’analyse !")
ui_audit_netlinkink()
