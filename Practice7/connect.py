import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS

def test_connection():
    try:
        # Пытаемся установить соединение
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("✅ Ура! Успешное подключение к PostgreSQL!")
        
        # Запрашиваем версию базы данных, чтобы точно убедиться, что всё работает
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(f"Версия БД: {db_version[0]}")
        
        # Закрываем подключение
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == '__main__':
    test_connection()