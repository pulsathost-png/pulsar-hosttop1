// =======================================
// 🌌 PulSar-Host v1.0
// Database System
// =======================================

import sqlite3 from "sqlite3";
import { open } from "sqlite";
import path from "path";
import { fileURLToPath } from "url";


// Получаем путь к папке

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


// Подключение базы

const database = await open({

    filename: path.join(
        __dirname,
        "pulsar.db"
    ),

    driver: sqlite3.Database

});



// Включаем защиту базы

await database.exec(`

PRAGMA journal_mode = WAL;

PRAGMA foreign_keys = ON;

`);





// Создание таблиц

await database.exec(`


CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    email TEXT,

    password TEXT NOT NULL,

    role TEXT DEFAULT 'user',

    balance INTEGER DEFAULT 0,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);



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

    ON DELETE CASCADE

);



CREATE TABLE IF NOT EXISTS promo_codes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    code TEXT UNIQUE NOT NULL,

    discount INTEGER NOT NULL,

    max_uses INTEGER DEFAULT 100,

    used INTEGER DEFAULT 0,

    active INTEGER DEFAULT 1,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);



CREATE TABLE IF NOT EXISTS logs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    action TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);



CREATE TABLE IF NOT EXISTS settings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT UNIQUE,

    value TEXT

);



`);






// Создание первого промокода

const promo = await database.get(

    "SELECT * FROM promo_codes WHERE code=?",

    [
        "PULSAR35"
    ]

);



if(!promo){


    await database.run(

        `

        INSERT INTO promo_codes

        (code,discount,max_uses)

        VALUES(?,?,?)

        `,

        [
            "PULSAR35",
            35,
            100
        ]

    );


}







// Настройки хостинга

const setting = await database.get(

    "SELECT * FROM settings WHERE name=?",

    [
        "hosting_name"
    ]

);



if(!setting){


    await database.run(

        `

        INSERT INTO settings

        (name,value)

        VALUES(?,?)

        `,

        [
            "hosting_name",
            "PulSar-Host"
        ]

    );


}





console.log(
    "💾 PulSar-Host Database запущена"
);



export default database;
