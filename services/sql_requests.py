def m_sessions(table_name):
    """
    Génère une requête SQL pour calculer le nombre de sessions distinctes.

    Cette requête identifie les sessions en concaténant `user_pseudo_id` et
    la valeur du paramètre `ga_session_id`.

    Args:
        table_name (str): Le nom de la table GA4 (ex. 'ga4_data').

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f'''
            WITH prep as (
                SELECT
                    user_pseudo_id,
                    unnest.key as key,
                    unnest.value.int_value as int_value
                FROM 
                    {table_name}, 
                    LATERAL UNNEST(event_params)
                WHERE key = 'ga_session_id'
            )
            SELECT
                COUNT(DISTINCT CONCAT(user_pseudo_id, int_value))
            FROM
                prep
        '''
        return query
    except Exception as e:
        print(f'Error in m_sessions: {e}')
        return None

def d_event_date(table_name):
    """
    Extrait toutes les dates d'événements distinctes.

    Args:
        table_name (str): Le nom de la table GA4.

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f'''
        SELECT
            DISTINCT(event_date) AS event_date
        FROM 
            {table_name}
        '''
        return query
    except Exception as e:
        print(f'Error in d_event_date: {e}')
        return None

def m_date(table_name):
    """
    Compte le nombre de jours uniques dans les données.

    Args:
        table_name (str): Le nom de la table GA4.

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f'''
        SELECT
            COUNT(DISTINCT(event_date)) AS event_date
        FROM 
            {table_name}
        '''
        return query
    except Exception as e:
        print(f'Error in m_date: {e}')
        return None

def m_users(table_name):
    """
    Compte le nombre total d'utilisateurs uniques.

    Args:
        table_name (str): Le nom de la table GA4.

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f'''
        SELECT
            COUNT(DISTINCT user_pseudo_id) AS num_user
        FROM
            {table_name}
        '''
        return query
    except Exception as e:
        print(f'Error in m_users: {e}')
        return None

def distinct_event_params_list(table_name):
    """
    Extrait les clés distinctes dans les paramètres d’événement (event_params).

    Args:
        table_name (str): Le nom de la table GA4.

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f"""
        SELECT DISTINCT json_extract(t.key, '$.key') AS key
        FROM {table_name},
        UNNEST({table_name}.event_params) AS t(key, value)
        """
        return query
    except Exception as e:
        print(f'Error in distinct_event_params_list: {e}')
        return None

def event_and_customdim_list(table_name):
    """
    Retourne la fréquence de chaque paramètre par événement.

    Args:
        table_name (str): Le nom de la table GA4.

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f"""
        SELECT
            event_name,
            json_extract(t.key, '$.key') AS key,
            COUNT(event_name) AS event_count
        FROM {table_name},
        UNNEST({table_name}.event_params) AS t(key, value)
        GROUP BY event_name, key
        ORDER BY event_count DESC
        """
        return query
    except Exception as e:
        print(f'Error in event_and_customdim_list: {e}')
        return None

def event_name_extract(table_name):
    """
    Extrait les noms d'événements distincts.

    Args:
        table_name (str): Le nom de la table GA4.

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f"""
        SELECT DISTINCT event_name AS event_name
        FROM {table_name}
        """
        return query
    except Exception as e:
        print(f'Error in event_name_extract: {e}')
        return None

def m_event_name(table_name):
    """
    Calcule le nombre d’occurrences de chaque événement.

    Args:
        table_name (str): Le nom de la table GA4.

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f"""
        SELECT
            event_name,
            COUNT(event_name) AS event_count
        FROM {table_name}
        GROUP BY event_name
        ORDER BY event_count DESC
        """
        return query
    except Exception as e:
        print(f'Error in m_event_name: {e}')
        return None

def extract_event_params_unnest(table_name, params_extract):
    """
    Extrait les valeurs d'un paramètre spécifique à partir d'event_params.

    Args:
        table_name (str): Le nom de la table GA4.
        params_extract (str): Le nom du paramètre à extraire (ex. 'page_location').

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f'''
        SELECT
            event_name,
            unnest.key AS key,
            unnest.value.int_value AS int_value,
            unnest.value.string_value AS str_value
        FROM {table_name}, 
        LATERAL UNNEST(event_params)
        WHERE key = '{params_extract}'
        '''
        return query
    except Exception as e:
        print(f'Error in extract_event_params_unnest: {e}')
        return None

def event_and_customdim_checker(table_name):
    """
    Vérifie la présence des dimensions personnalisées pour chaque événement.

    Cette requête compare les événements totaux à ceux ayant une dimension personnalisée.

    Args:
        table_name (str): Le nom de la table GA4.

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f"""
        WITH custom_dim AS (
            SELECT
                event_name,
                json_extract(t.key, '$.key') AS key,
                COUNT(*) AS custom_dim_count
            FROM {table_name},
            UNNEST({table_name}.event_params) AS t(key, value)
            GROUP BY event_name, key
        ),
        event AS (
            SELECT
                event_name,
                COUNT(*) AS total_event_count
            FROM {table_name}
            GROUP BY event_name
        )
        SELECT
            cd.event_name,
            cd.key,
            SUM(cd.custom_dim_count) AS custom_dim_number,
            MAX(evt.total_event_count) AS total_event,
            MAX(evt.total_event_count) - SUM(cd.custom_dim_count) AS delta,
            CASE 
                WHEN MAX(evt.total_event_count) != 0 THEN 
                    ROUND((1 - SUM(cd.custom_dim_count) * 1.0 / MAX(evt.total_event_count)) * 100, 2)
                ELSE NULL
            END AS missing_percent
        FROM custom_dim AS cd
        LEFT JOIN event AS evt ON evt.event_name = cd.event_name
        GROUP BY cd.event_name, cd.key
        ORDER BY missing_percent DESC
        """
        return query
    except Exception as e:
        print(f'Error in event_and_customdim_checker: {e}')
        return None

def page_location_extract(table_name):
    """
    Extrait les URLs (page_location) présentes dans les paramètres d’événements.

    Args:
        table_name (str): Le nom de la table GA4.

    Returns:
        str or None: Requête SQL, ou None en cas d'erreur.
    """
    try:
        query = f"""
        SELECT DISTINCT
            unnest.value.string_value AS page_location
        FROM {table_name}, 
        LATERAL UNNEST(event_params) AS unnest
        WHERE unnest.key = 'page_location'
        AND unnest.value.string_value IS NOT NULL
        """
        return query
    except Exception as e:
        print(f'Error in page_location_extract: {e}')
        return None

def source_medium_campaign_by_user(table_name):
    """
    Génère une requête SQL pour compter les utilisateurs distincts selon la source, le medium et la campagne.

    Cette fonction construit une requête SQL à exécuter sur une table d'export GA4 (par exemple chargée dans DuckDB),
    permettant de récupérer le nombre d'utilisateurs uniques (`user_pseudo_id`) pour chaque combinaison :
    - `traffic_source.source`
    - `traffic_source.medium`
    - `traffic_source.name` (renommée en campagne)

    Le résultat est trié par nombre d'utilisateurs décroissant.

    Args:
        table_name (str): Le nom de la table à interroger (non utilisé ici, la table est en dur : 'ga4_data').

    Returns:
        str: La chaîne contenant la requête SQL.

    Raises:
        Exception: En cas d'erreur lors de la génération de la requête.
    """
    try:
        query = f"""
        SELECT
          traffic_source.source AS source,
          traffic_source.medium AS medium,
          traffic_source.name AS campaign,
          COUNT(DISTINCT user_pseudo_id) AS users
        FROM {table_name}
        GROUP BY
          traffic_source.source,
          traffic_source.medium,
          traffic_source.name
        ORDER BY
          users DESC
        """
        return query
    except Exception as e:
        print(f'Erreur dans source_medium_campaign_by_user : {e}')
        return None


