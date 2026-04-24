import psycopg2
import csv
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS

# Подключение к базе данных
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# 1. Design and create PhoneBook table
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    # Создаем таблицу, если ее еще нет. 
    # id (SERIAL) - автонумерация, name и phone - текст.
    cur.execute('''
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
    ''')
    conn.commit() # Обязательно подтверждаем изменения!
    cur.close()
    conn.close()
    print("Таблица PhoneBook готова.")

# 2. Implement CSV-based data import
def import_csv(filename="contacts.csv"):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2: # Проверяем, что в строке ровно 2 элемента (имя и телефон)
                cur.execute("INSERT INTO PhoneBook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Данные из {filename} успешно импортированы!")

# 3. Implement console-based data entry
def add_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO PhoneBook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Контакт {name} добавлен!")

# 4. Implement updating contacts (name or phone)
# --- ВОТ ЗДЕСЬ ИСПРАВЛЕНА ПРОБЛЕМА ---
def update_contact(old_name, new_name, new_phone):
    conn = get_connection()
    cur = conn.cursor()
    
    # Сначала находим старые данные контакта в базе
    cur.execute("SELECT name, phone FROM PhoneBook WHERE name = %s", (old_name,))
    record = cur.fetchone()
    
    if record:
        # Если новое имя или телефон не ввели  оставляем старые данные
        final_name = new_name if new_name != "" else record[0]
        final_phone = new_phone if new_phone != "" else record[1]
        
        cur.execute("UPDATE PhoneBook SET name = %s, phone = %s WHERE name = %s", (final_name, final_phone, old_name))
        conn.commit()
        print(f"Контакт {old_name} успешно обновлен!")
    else:
        print(f"Контакт с именем {old_name} не найден!")
        
    cur.close()
    conn.close()

# 5. Implement querying with different filters
def search_contact(filter_text):
    conn = get_connection()
    cur = conn.cursor()
    # ILIKE ищет совпадения без учета регистра, знаки % означают "любые символы до и после"
    search_pattern = f"%{filter_text}%"
    cur.execute("SELECT * FROM PhoneBook WHERE name ILIKE %s OR phone ILIKE %s", (search_pattern, search_pattern))
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    print("\n--- Результаты поиска ---")
    for row in results:
        print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    print("-------------------------\n")

# 6. Implement deleting contacts by username or phone
def delete_contact(identifier):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM PhoneBook WHERE name = %s OR phone = %s", (identifier, identifier))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Контакт '{identifier}' удален (если он существовал).")

# Интерактивное меню для терминала
if __name__ == '__main__':
    create_table() # Сразу создаем таблицу при запуске
    
    while True:
        print("\n--- ТЕЛЕФОННАЯ КНИГА ---")
        print("1. Загрузить из CSV")
        print("2. Добавить контакт вручную")
        print("3. Найти контакт")
        print("4. Обновить контакт")
        print("5. Удалить контакт")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            import_csv()
        elif choice == '2':
            name = input("Введите имя: ")
            phone = input("Введите телефон: ")
            add_contact(name, phone)
        elif choice == '3':
            text = input("Введите имя или телефон для поиска: ")
            search_contact(text)
        elif choice == '4':
            old = input("Введите старое имя контакта: ")
            # --- ЗДЕСЬ ИЗМЕНИЛИСЬ ПОДСКАЗКИ ДЛЯ УДОБСТВА ---
            new_n = input("Введите новое имя (или посто нажмите Enter, чтобы оставить старое): ")
            new_p = input("Введите новый телефон (или посто нажмите Enter, чтобы оставить старый): ")
            update_contact(old, new_n, new_p)
        elif choice == '5':
            ident = input("Введите точное имя или телефон для удаления: ")
            delete_contact(ident)
        elif choice == '0':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте еще раз.")