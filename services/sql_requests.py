'''
Here is all function with the requests
'''


def m_sessions(table_name):
    '''
    Out : Number of sessions
    '''
    query = f'''
            WITH prep as (
                SELECT
                    user_pseudo_id
                    ,unnest.key as key
                    ,unnest.value.int_value as int_value
                FROM 
                    {table_name}, 
                    LATERAL UNNEST(event_params)
                WHERE key = 'ga_session_id'
            )
            SELECT
                COUNT(DISTINCT CONCAT(user_pseudo_id,int_value))
            FROM
                prep
    '''
    return query


def d_event_date(table_name):
    '''
    I/O : Table / Date DF
    '''
    try:
        query = f'''
        SELECT
            DISTINCT(event_date) as event_date
        FROM 
            {table_name}
        '''
        return query
    except Exception as e:
        print(f'Error in d_event_date: {e}')


def m_date(table_name):
    '''
    string: event_date value
    '''
    try:
        query = f'''
        SELECT
            COUNT(DISTINCT(event_date)) as event_date
        FROM 
            {table_name}
        '''
        return query
    except Exception as e:
        print(f'Error in num_date: {e}')


def m_users(table_name):
    '''
    I/O : Number of users per days
    '''
    try:
        query = f'''
        SELECT
            COUNT(DISTINCT user_pseudo_id) as num_user
        FROM
            {table_name}
        '''
        return query
    except Exception as e:
        print(f'Error in m_users: {e}')
        return None


def all(table_name):
    """
    I/O : table into all table in a DF
    """
    try:
        query = f"""
        SELECT * FROM {table_name}
        """
        return query
    except Exception as e:
        print(f'Error in all: {e}')
        return None


def distinct_event_params_list(table_name):
    '''
    I/O : Table => event_params DF
    '''
    try:
        query = f"""
        SELECT DISTINCT json_extract(t.key, '$.key') AS key
        FROM {table_name},
        UNNEST({table_name}.event_params) AS t(key, value)
                """
        return query
    except Exception as e:
        print(f'Error in event_params_list: {e}')
        return None


def event_name_extract(table_name):
    '''
        I/O : extract all distinct event_name in the dataSet
    '''
    try:
        query = f"""
        SELECT
            DISTINCT event_name as event_name
        FROM
            {table_name}
            """
        return query
    except Exception as e:
        print(f'Error in event_name: {e}')
        return None


def extract_event_params_unnest(table_name, params_extract):
    try:
        query = f'''
        SELECT
            event_name
            ,unnest.key as key
            ,unnest.value.int_value as int_value
            ,unnest.value.string_value as str_value

        FROM {table_name}, 
        LATERAL UNNEST(event_params)
        WHERE key = '{params_extract}'
        '''
        # ,unnest.value.double_value as double_value -> TBD
        return query
    except Exception as e:
        print(f'Error in extract_event_params_unnest : {e}')
        return None


'''
- Vérification du consentement bien en place dans le hit
- Vérification des duplications
- Vérification des valeurs null et l'impact possible
- Vérification du user_pseudo_id disponible à chaque fois
- Vérification du ga_session_id à chaque fois
'''