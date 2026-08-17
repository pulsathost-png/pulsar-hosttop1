import sqlite3
import os


DB_NAME = "pulsar.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn



def init_db():

    db = get_db()


    # Пользователи
    db.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        token TEXT,
        balance INTEGER DEFAULT 0,
        role TEXT DEFAULT 'user'
    )
    """)



    # Игровые серверы
    db.execute("""
    CREATE TABLE IF NOT EXISTS servers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        game TEXT,
        status TEXT DEFAULT 'offline',
        ram INTEGER DEFAULT 1024,
        cpu INTEGER DEFAULT 1,
        created TEXT
    )
    """)



    # Промокоды
    db.execute("""
    CREATE TABLE IF NOT EXISTS promo_codes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        bonus INTEGER DEFAULT 0,
        used INTEGER DEFAULT 0
    )
    """)



    # Платежи
    db.execute("""
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        status TEXT DEFAULT 'pending'
    )
    """)



    db.commit()

    db.close()
