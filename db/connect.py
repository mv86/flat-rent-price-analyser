import psycopg2, logging
from db.config import config


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
