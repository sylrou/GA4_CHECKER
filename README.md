# ------------------------------------------------------------
# 📘 Documentation du Projet GA4 Checker
# ------------------------------------------------------------

## 🎯 Objectif du Projet
L'objectif de ce projet est de mettre en place une série de **contrôles automatisés** permettant de vérifier la **qualité des données issues de Google Analytics 4 (GA4)** exportées depuis BigQuery.

📦 **Input attendu** : des exports GA4 au format **JSON brut** (via BigQuery UI ou Cloud Storage).

Les contrôles suivent les 6 axes du framework de qualité des données :
- Complétude
- Validité
- Unicité
- Disponibilité (Timeliness)
- Cohérence
- Exactitude

## ⚙️ Architecture du Projet
Le projet s'appuie sur :
- **DuckDB** pour le traitement SQL local sur fichiers JSON
- **Python** pour automatiser et encapsuler les analyses
- **Streamlit** pour une visualisation interactive par chapitre (ex: steamlist, validity...)
- **Pandas** pour les dataframes

## 🗂️ Structure des chapitres
Chaque chapitre du framework correspond à un **module de contrôle** avec sa propre logique métier, requêtes, et app Streamlit dédiée.

---

### 🔧 Phase 0 – Préparation du dataset
- [WIP] Préparer un data catalogue GA4 à partir des specs officielles Google
- [OK] Identifier le type de dataset via les événements (lead_gen, ecommerce, game...)
- [ ] Conditionner les recommandations en fonction du type de dataset
- [ ] Gérer l'importation et l'affichage des informations basiques de l'extraction dans streamlit
- [ ] Gérer la mise en place de la partie validity dans streamlit avec la librairie urllib.parse
- [ ] Définir un output pour l'utilisateur et avoir les informations dans un tableau avec une première analyse

---

### ✅ 1. Complétude (Completeness)
Vérifier que les données attendues sont bien présentes et disponibles.

Contrôles à implémenter :
- [OK] Lister les dimensions dans la donnée
- [OK] Lister les événements dans la donnée
- [OK] Lister les dates dans la donnée
- [OK] Comparer les événements de la donnée avec la liste d'événements standard recommandés par Google
- [ ] Comparer les dimensions par événements standards avec la liste des dimensions recommandées par Google
- [ ] Vérifier la couverture de la collecte en fonction des dates
- [ ] Vérifier la présence de `ga_session_id` (identifiant de session valide)
- [ ] Vérifier la couverture de la collecte des sessions sur la période de l'échantillon
- [ ] Vérifier la présence de `user_pseudo_id` (identifiant utilisateur anonyme)
- [ ] Vérifier la continuité de la collecte des utilisateurs (`user_pseudo_id`) sur la période de l'échantillon
- [ ] Vérifier la présence de `user_id` (si implémenté pour les utilisateurs connectés)
- [ ] Vérifier la couverture de la collecte des utilisateurs (`user_id`) sur la période de l'échantillon
- [ ] Vérifier la couverture des dimensions par événements (`event_name`, `event_params`)
- [ ] Vérifier la présence des événements et des dimensions recommandées (`event_name`, `event_params`)
- [ ] Vérifier la présence des `source/medium/campaign` dans l'URL de la landing page et dans les colonnes spécifiques (`gclid`, etc.)
- [ ] Vérifier la présence des `page_location` dans la donnée
- [ ] Vérifier la présence des événements `session_start` et `first_session` dans la donnée pour chaque session

---

### 🧪 2. Validité (Validity)
S'assurer que les données ont des valeurs cohérentes et dans un format attendu.

Contrôles à implémenter :
- [ ] Vérifier que 'user_id' respecte le bon format (UUID, email hashé, ou autre identifiant conforme)
- [ ] Vérifier que `ga_session_id` et `user_pseudo_id` ne contiennent pas de valeurs nulles ou erronées (`0`, `-1`, `undefined`, `null`)
- [ ] Vérifier que les dimensions clés ne contiennent pas de valeurs nulles ou erronées (`0`, `-1`, `undefined`, `null`)
- [ ] Vérifier la validité des valeurs numériques (`event_value`, `event_revenue`, `event_currency`)
- [ ] Vérifier la cohérence des paramètres d'URL de `source/medium/campagne` vs `source/medium` (gclid) → taux de matching
- [WIP] Vérifier dans le `page_location` qu'il n'y a pas de paramètres d'URL de type PII (email, nom, prénom...)
- [WIP] Vérifier la présence de fragment dans 'page_location' (tableau ou fragment ?)
- [WIP] Vérifier les domains présents dans la donnée (histograme ou tableau ?)
- [WIP] Vérifier que les urls ne sont pas trop longues (tableau avec les url > x char ?)
- [WIP] Vérifier que les urls sont en https => Histograme ?
- [WIP] Vérifier qu'il n'y a pas de doublons d'url
---

### 🧬 3. Unicité (Uniqueness)
Éviter les doublons et collisions d’identifiants.

Contrôles à implémenter :
- [ ] Vérifier l’unicité des combinaisons `user_pseudo_id + ga_session_id + event_timestamp`
- [ ] Vérifier que les identifiants d’événements (`event_bundle_sequence_id`) ne sont pas dupliqués dans une même session
- [ ] Vérifier que les identifiants d’événements (`event_id`) ne sont pas dupliqués dans une même session

---

### ⏱️ 4. Disponibilité (Timeliness)
Vérifier que la donnée est collectée et disponible dans des délais acceptables, en respectant les autorisations utilisateurs (RGPD, consentement).

Contrôles à implémenter :
- [ ] Vérifier l'impact du consentement utilisateur sur la collecte des données
- [ ] Vérifier l'impact du CoMo sur la collecte

---

### 📈 5. Cohérence (Consistency)
S’assurer que les tendances et structures de la donnée restent cohérentes dans le temps.

Contrôles à implémenter :
- [ ] Vérifier la stabilité du volume d’événements collectés quotidiennement
- [ ] Comparer les données sur plusieurs jours pour détecter d’éventuelles anomalies ou pertes
- [ ] Vérifier la distribution des valeurs pour chaque dimension critique (`event_name`, `event_params`)

---

### 🎯 6. Exactitude (Accuracy)
S’assurer que les valeurs collectées correspondent bien à la réalité des transactions et interactions utilisateur.

Contrôles à implémenter :
- [ ] Vérifier la correspondance entre les revenus GA4 (`purchase_revenue`) et les transactions réelles du site e-commerce
- [ ] Comparer les données GA4 avec d’autres sources (CRM, backend...)
- [ ] Vérifier que les événements sont bien déclenchés au bon moment et avec les bons paramètres

---

## 🚀 Fonctionnalités actuelles
- [OK] Requête SQL automatique sur DuckDB
- [OK] Extraction de `event_params`, `event_name`, `page_location`
- [OK] Interface interactive via Streamlit pour `steamlist` (events) et `validity` (params URL)
- [OK] Séparation des fichiers par module (préparation d’un menu global Streamlit)
- [WIP] Faire une page spécifique pour l'import de la donnée
- [] Proposer un jeu de donnée de test pour l'utilisateur qui n'a pas de donnée sous la main et favoriser l'onboarding

## 📦 Environnement technique
- Python 3.11+
- DuckDB
- Streamlit
- pandas, re, urllib, etc.

---

## 📁 Étapes du projet
- [OK] Définir si le projet est faisable via un POC sur quelques critères et analyses
- [OK] Définir comment unnest la donnée du format JSON
- [ ] Définir comment unnest la donnée du format Parquet
- [ ] Développer les requêtes SQL nécessaires pour chaque contrôle dans BigQuery
- [ ] Automatiser les tests via un script Python utilisant DuckDB pour le traitement des exports JSON
- [ ] Automatiser les tests via un script Python utilisant DuckDB pour le traitement des exports Parquet
- [ ] Générer un rapport détaillé sur la qualité des données GA4
- [WIP] Ajouter en production une page de remerciement

---

## ⚠️ Limitations actuelles
- L’export JSON depuis BigQuery UI est limité à 1 Go
- Il faut utiliser Cloud Storage pour récupérer un fichier Parquet propre
- Streamlit Cloud limite l’upload à 200 Mo (contournable avec config ou fallback fichier local ou hébergement de streamlit sur un VPS perso ou utilisation en local)

## 🔗 Ressources utiles
- [Matplotlib cheatsheet](https://github.com/matplotlib/cheatsheets)
- Specs GA4 : [Google Analytics 4 documentation](https://support.google.com/analytics/answer/9322688)

---

👨‍💻 Auteur : **Sylvain Rouxel**
🗓️ Création : **2024-12-01**
🛠️ Dernière mise à jour : **2025-04-19**
