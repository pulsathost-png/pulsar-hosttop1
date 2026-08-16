# =====================================
# 🌌 PulSar-Host v1.0
# Database System
# =====================================

import sqlite3
import os


# Путь к базе

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "pulsar.db"
)



# Подключение к базе

def get_connection():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection




# Создание таблиц

def init_database():

    db = get_connection()

    cursor = db.cursor()



    # Пользователи

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT DEFAULT 'user',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # Игровые серверы

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servers (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        name TEXT NOT NULL,

        game TEXT NOT NULL,

        status TEXT DEFAULT 'offline',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # Промокоды

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS promo_codes (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT UNIQUE NOT NULL,

        discount INTEGER NOT NULL,

        max_uses INTEGER DEFAULT 100,

        used INTEGER DEFAULT 0,

        active INTEGER DEFAULT 1

    )
    """)



    # Логи

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        action TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)




    # Первый промокод

    cursor.execute("""
    INSERT OR IGNORE INTO promo_codes
    (code, discount, max_uses)
    VALUES
    ('PULSAR35',35,100)
    """)



    db.commit()

    db.close()



    print(
        "💾 База PulSar-Host создана"
    )



# Запуск создания базы

if __name__ == "__main__":

    init_database()
