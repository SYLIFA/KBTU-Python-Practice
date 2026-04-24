import sqlite3

def init_db():
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    # Таблица пользователей
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE)')
    # Таблица очков (связана через user_id)
    cursor.execute('CREATE TABLE IF NOT EXISTS scores (user_id INTEGER, score INTEGER, level INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))')
    conn.commit()
    conn.close()

def save_score(name, score, level):
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    # Добавляем юзера, если его нет
    cursor.execute('INSERT OR IGNORE INTO users (name) VALUES (?)', (name,))
    cursor.execute('SELECT id FROM users WHERE name = ?', (name,))
    user_id = cursor.fetchone()[0]
    # Сохраняем рекорд
    cursor.execute('INSERT INTO scores (user_id, score, level) VALUES (?, ?, ?)', (user_id, score, level))
    conn.commit()
    conn.close()

def get_top_10():
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    # ТОТ САМЫЙ JOIN ДЛЯ ЗАЩИТЫ
    query = """
    SELECT users.name, scores.score, scores.level 
    FROM users 
    JOIN scores ON users.id = scores.user_id 
    ORDER BY scores.score DESC LIMIT 10
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data