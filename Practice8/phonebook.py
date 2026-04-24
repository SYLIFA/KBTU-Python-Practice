import psycopg2
from connect import connect
import os

def setup_database(conn):
    """Создает таблицу и загружает функции/процедуры из .sql файлов"""
    cur = conn.cursor()
    # Создаем таблицу, если ее нет
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            surname VARCHAR(100),
            phone VARCHAR(20)
        );
    """)
    
    # Читаем и выполняем .sql файлы
    base_dir = os.path.dirname(__file__)
    for filename in ['functions.sql', 'procedures.sql']:
        with open(os.path.join(base_dir, filename), 'r') as file:
            cur.execute(file.read())
    conn.commit()
    print("✅ Таблица, функции и процедуры успешно загружены в БД.")
    cur.close()

def run_tests():
    conn = connect()
    if not conn:
        return

    setup_database(conn)
    cur = conn.cursor()

    try:
        # 1. Тест Upsert
        print("\n--- 1. Testing UPSERT ---")
        cur.execute("CALL upsert_contact(%s, %s, %s)", ("John", "Doe", "+12345678901"))
        cur.execute("CALL upsert_contact(%s, %s, %s)", ("John", "Doe", "+99999999999")) # Обновит телефон
        conn.commit()
        print("Upsert выполнен успешно.")

        # 2. Тест Bulk Insert с валидацией (один правильный, два неправильных телефона)
        print("\n--- 2. Testing BULK INSERT (with Validation) ---")
        names = ["Alice", "Bob", "Charlie"]
        surnames = ["Smith", "Brown", "Chaplin"]
        phones = ["+11111111111", "invalid_phone", "123"] # Bob и Charlie должны отлететь
        
        cur.execute("CALL bulk_insert_contacts(%s, %s, %s, NULL)", (names, surnames, phones))
        invalid_data = cur.fetchone()[0] # Ловим INOUT параметр
        conn.commit()
        print(f"Ошибочные записи (не добавлены): {invalid_data}")

        # 3. Тест поиска по паттерну
        print("\n--- 3. Testing PATTERN SEARCH ---")
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", ("Smi",))
        print("Найдено по паттерну 'Smi':", cur.fetchall())

        # 4. Тест пагинации (LIMIT 2, OFFSET 0)
        print("\n--- 4. Testing PAGINATION ---")
        cur.execute("SELECT * FROM get_contacts_paginated(2, 0)")
        print("Первая страница (2 записи):", cur.fetchall())

        # 5. Тест удаления
        print("\n--- 5. Testing DELETE ---")
        cur.execute("CALL delete_contact(%s)", ("Alice",))
        conn.commit()
        print("Контакт 'Alice' удален.")

    except Exception as e:
        print(f"❌ Ошибка во время тестов: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    run_tests()