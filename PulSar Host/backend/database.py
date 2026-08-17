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





# Создание базы

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

        balance INTEGER DEFAULT 0,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP

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

        cpu INTEGER DEFAULT 0,

        ram INTEGER DEFAULT 0,

        storage INTEGER DEFAULT 0,

        players INTEGER DEFAULT 0,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,


        FOREIGN KEY(user_id)

        REFERENCES users(id)

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

        active INTEGER DEFAULT 1,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP

    )
    """)





    # Логи действий

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        action TEXT,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP

    )
    """)





    # Настройки хостинга

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT UNIQUE,

        value TEXT

    )
    """)





    # Создаем стартовый промокод

    cursor.execute("""
    INSERT OR IGNORE INTO promo_codes
    (
        code,
        discount,
        max_uses
    )

    VALUES
    (
        'PULSAR35',
        35,
        100
    )
    """)






    # Основные настройки

    cursor.execute("""
    INSERT OR IGNORE INTO settings
    (
        name,
        value
    )

    VALUES
    (
        'hosting_name',
        'PulSar-Host'
    )
    """)



    cursor.execute("""
    INSERT OR IGNORE INTO settings
    (
        name,
        value
    )

    VALUES
    (
        'version',
        '1.0.0'
    )
    """)





    db.commit()

    db.close()



    print(
        "💾 PulSar-Host Database готова"
    )






# Проверка запуска

if __name__ == "__main__":

    init_database()
