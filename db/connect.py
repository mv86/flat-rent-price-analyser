import psycopg2, logging
from .config import config


def insert(sql, data):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, data)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        logging.error(f'Connection error: {e}')
    finally:
        if conn is not None:
            conn.close()


def select(sql, data):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if data:
            cur.execute(sql, data)
        else:
            cur.execute(sql)
        select_data = cur.fetchall()
        cur.close()
        return select_data
    except (Exception, psycopg2.DatabaseError) as e:
        logging.error(f'Connection error: {e}')
    finally:
        if conn is not None:
            conn.close()
