import psycopg2
from config import load_config

def connect():
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Ошибка подключения: {error}")
        return None