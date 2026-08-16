import sqlite3 from "sqlite3";
import { open } from "sqlite";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


const database = await open({

    filename: path.join(__dirname, "pulsar.db"),

    driver: sqlite3.Database

});


// ==========================
// Создание структуры базы
// ==========================

await database.exec(`


PRAGMA journal_mode = WAL;

PRAGMA foreign_keys = ON;



CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    email TEXT UNIQUE,

    password TEXT NOT NULL,

    role TEXT DEFAULT 'user',

    balance INTEGER DEFAULT 0,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);



CREATE TABLE IF NOT EXISTS servers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    name TEXT NOT NULL,

    game TEXT NOT NULL,

    status TEXT DEFAULT 'offline',

    cpu INTEGER DEFAULT 0,

    ram INTEGER DEFAULT 0,

    storage INTEGER DEFAULT 0,

    players INTEGER DEFAULT 0,

    ip TEXT,

    port INTEGER,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY(user_id)

    REFERENCES users(id)

    ON DELETE CASCADE

);



CREATE TABLE IF NOT EXISTS plans (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    cpu INTEGER,

    ram INTEGER,

    storage INTEGER,

    price INTEGER

);



CREATE TABLE IF NOT EXISTS promo_codes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    code TEXT UNIQUE NOT NULL,

    discount INTEGER NOT NULL,

    max_uses INTEGER DEFAULT 100,

    used INTEGER DEFAULT 0,

    active INTEGER DEFAULT 1,

    expires DATETIME

);



CREATE TABLE IF NOT EXISTS backups (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    server_id INTEGER,

    file TEXT,

    size INTEGER,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY(server_id)

    REFERENCES servers(id)

);



CREATE TABLE IF NOT EXISTS logs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    action TEXT,

    ip TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);



CREATE TABLE IF NOT EXISTS api_keys (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    key TEXT UNIQUE,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);



CREATE TABLE IF NOT EXISTS settings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT UNIQUE,

    value TEXT

);



CREATE INDEX IF NOT EXISTS idx_servers_user

ON servers(user_id);



CREATE INDEX IF NOT EXISTS idx_logs_user

ON logs(user_id);



`);



// ==========================
// Начальные данные
// ==========================


// Тарифы

const plans = await database.get(
    "SELECT COUNT(*) as count FROM plans"
);


if(plans.count === 0){

    await database.run(`

    INSERT INTO plans
    (name,cpu,ram,storage,price)

    VALUES

    ('START',1,1024,10,99),

    ('PRO',2,4096,30,299),

    ('ULTRA',4,8192,60,599)

    `);

}



// Промокод открытия

const promo = await database.get(

    "SELECT * FROM promo_codes WHERE code=?",

    ["PULSAR35"]

);



if(!promo){

    await database.run(`

    INSERT INTO promo_codes

    (code,discount,max_uses)

    VALUES

    ('PULSAR35',35,100)

    `);

}



// Настройки

const settings = await database.get(

    "SELECT * FROM settings WHERE name=?",

    ["hosting_name"]

);


if(!settings){

    await database.run(`

    INSERT INTO settings

    (name,value)

    VALUES

    ('hosting_name','PulSar-Host')

    `);

}



console.log("🌌 PulSar-Host Database v1.0 запущена");


export default database;
