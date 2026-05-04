import sqlite3
import csv
import os

DB_NAME = 'phonebook.db'

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Создаем таблицу с первичным ключом и уникальным номером
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def add_contact(name, phone):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        conn.close()
        print(f"✅ Контакт {name} успешно добавлен!")
    except sqlite3.IntegrityError:
        print("⚠️ Ошибка: Контакт с таким номером уже существует.")

def search_contact(pattern):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?", (f'%{pattern}%', f'%{pattern}%'))
    results = cursor.fetchall()
    conn.close()
    return results

def update_contact(name, new_phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET phone = ? WHERE name = ?", (new_phone, name))
    if cursor.rowcount > 0:
        print(f"✅ Номер для {name} обновлен.")
    else:
        print("⚠️ Контакт не найден.")
    conn.commit()
    conn.close()

def delete_contact(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
    if cursor.rowcount > 0:
        print(f"🗑️ Контакт {name} удален.")
    else:
        print("⚠️ Контакт не найден.")
    conn.commit()
    conn.close()

def upload_from_csv(filename):
    if not os.path.exists(filename):
        print(f"⚠️ Файл {filename} не найден.")
        return
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.executemany('INSERT OR REPLACE INTO contacts (name, phone) VALUES (?, ?)', reader)
            conn.commit()
            conn.close()
            print(f"✅ Данные из {filename} загружены.")
    except Exception as e:
        print(f"⚠️ Ошибка при чтении CSV: {e}")

def show_paged(limit=5, offset=0):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM contacts LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- ИНТЕРФЕЙС МЕНЮ ---
def main_menu():
    create_db()
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Показать контакты (пагинация)")
        print("2. Добавить новый контакт")
        print("3. Поиск (по имени или номеру)")
        print("4. Обновить номер")
        print("5. Удалить контакт")
        print("6. Импорт из CSV")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ")

        if choice == '1':
            limit = int(input("Сколько записей показать? ") or 5)
            offset = int(input("Сколько записей пропустить? ") or 0)
            contacts = show_paged(limit, offset)
            for c in contacts: print(f"👤 {c[0]}: {c[1]}")
            
        elif choice == '2':
            name = input("Введите имя: ")
            phone = input("Введите номер: ")
            add_contact(name, phone)

        elif choice == '3':
            pattern = input("Введите часть имени или номера: ")
            results = search_contact(pattern)
            for r in results: print(f"🔍 Найдено: {r[0]} - {r[1]}")

        elif choice == '4':
            name = input("Имя контакта для обновления: ")
            new_phone = input("Новый номер: ")
            update_contact(name, new_phone)

        elif choice == '5':
            name = input("Имя контакта для удаления: ")
            delete_contact(name)

        elif choice == '6':
            filename = input("Введите имя CSV файла (напр. contacts.csv): ")
            upload_from_csv(filename)

        elif choice == '0':
            print("👋 До свидания!")
            break
        else:
            print("⚠️ Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main_menu()