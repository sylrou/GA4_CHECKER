import duckdb
import streamlit as st
import os
import gc

from assets.ui import ui_btn_link
from services.functions import safe_query_wrapper

dataset_type = 0
step = 1

st.header("📥 Importer les données GA4")

st.markdown("""
    Vous pouvez utiliser et importer votre propre donnée, mais si vous n'avez pas de fichier sous la main,  
    je vous invite à activer le jeu de données de démonstration, issu d’un ancien site.
    """)

#st.markdown('Importez votre propre donnée en suivant ce tutoriel : Lien vers le tutoriel')

if os.path.exists(os.path.abspath("raw_data/local_analysis.json")):
    data_file = os.path.abspath("raw_data/local_analysis.json")
    st.info(f"Etape {str(step)} : Mode local activé, le jeu de donnée local est sélectionné ✅")
    step += 1
    dataset_type = 1
else:
    user_test_data = st.toggle("🔧 Activer le jeu de données de démonstration")
    if user_test_data:
        data_file = os.path.abspath("raw_data/animalien_data.json")
        st.info(f"Etape {str(step)} : Jeu de démonstration sélectionné ✅")
        step += 1
        dataset_type = 2
    else:
        # Proposer un upload
        uploaded_file = st.file_uploader("Importez votre export GA4 (JSON)", type="json")

        # Sécurité : attendre l'upload
        if not uploaded_file:
            st.warning("Veuillez importer un fichier JSON pour continuer.")
            st.stop()

        dataset_type = 3

        # Sauvegarde temporaire du fichier JSON
        temp_path = os.path.abspath("temp_validity.json")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        data_file = temp_path
        st.info(f"Etape {str(step)} : Fichier json chargé et fichier temporaire crée ✅")
        step += 1

# --- Création de la base persistante DuckDB ---
db_path = os.path.abspath("../ga4.duckdb")
with st.spinner("⏳ Chargement du fichier dans DuckDB..."):
    con = safe_query_wrapper(
                lambda:duckdb.connect(database=db_path, read_only=False)
    )
    con.execute("INSTALL json; LOAD json;")

    con.execute("DROP TABLE IF EXISTS ga4_data;")  # Pour éviter conflits
    con.execute(f"""
        CREATE TABLE ga4_data AS
        SELECT * FROM read_ndjson('{data_file}', union_by_name=True)
    """)

    st.info(f"Etape {str(step)} : Base DuckDB créée avec succès ✅")
    step += 1
    st.info(f"Etape {str(step)} : 📂 Base DuckDB sauvegardée ici : `{db_path}`")
    step += 1

    # Affiche les infos de la table chargé (pour les debugs)
    with st.expander("💡 Affichez le schéma de votre import :"):
        st.dataframe(con.sql("PRAGMA table_info(ga4_data)").df())

    con.close()

# Supprimer le fichier temporaire (Evite le surstockage)
if "temp_validity.json" in data_file:
    try:
        os.remove(data_file)
        st.info(f"Etape {str(step)} - 🧹 Le fichier temporaire a été supprimé (libération de l'espace disque).")
        step += 1
    except Exception as e:
        st.warning(f"Erreur lors de la suppression du fichier temporaire : {e}")
else:
    pass

# Libération mémoire du fichier uploadé
if dataset_type == 3:
    del uploaded_file
    gc.collect()
    st.info(f"Etape {str(step)} - 💾 Mémoire libérée après chargement du fichier (libération de la RAM)")
    step += 1

st.success("🎉 Données importées avec succès. Vous êtes prêt pour l’analyse !")
st.markdown('### Vous pouvez maintenant vous dirigez vers :')
ui_btn_link("add_step/audit_overview.py", "Analyse - Vue globale")