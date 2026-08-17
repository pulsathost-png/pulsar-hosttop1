# =====================================
# 🌌 PulSar-Host v1.0
# Main Backend
# =====================================

from flask import Flask, jsonify, request
from flask_cors import CORS

from database import init_database, get_connection

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)

CORS(app)


# Запускаем базу
init_database()



# =====================================
# Главная
# =====================================

@app.route("/")
def home():

    return jsonify({
        "project": "PulSar-Host",
        "version": "1.0.0",
        "status": "online"
    })





# =====================================
# Статус
# =====================================

@app.route("/api/status")
def status():

    db = get_connection()

    users = db.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]


    servers = db.execute(
        "SELECT COUNT(*) FROM servers"
    ).fetchone()[0]


    db.close()


    return jsonify({

        "online": True,

        "users": users,

        "servers": servers

    })






# =====================================
# Регистрация
# =====================================

@app.route("/api/register", methods=["POST"])
def register():

    data = request.json


    username = data.get("username")
    password = data.get("password")


    if not username or not password:

        return jsonify({
            "error":"Заполни поля"
        }),400



    db = get_connection()


    try:

        db.execute(

            """
            INSERT INTO users
            (
            username,
            password
            )

            VALUES (?,?)

            """,

            (
                username,
                generate_password_hash(password)
            )

        )


        db.commit()



    except Exception:

        return jsonify({

            "error":
            "Пользователь уже существует"

        }),400



    db.close()


    return jsonify({

        "success":True

    })






# =====================================
# Вход
# =====================================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.json


    username = data.get("username")
    password = data.get("password")



    db = get_connection()



    user = db.execute(

        """
        SELECT *
        FROM users
        WHERE username=?

        """,

        (username,)

    ).fetchone()



    db.close()



    if user and check_password_hash(
        user["password"],
        password
    ):


        return jsonify({

            "success":True,

            "user":{

                "id":user["id"],

                "username":
                user["username"],

                "role":
                user["role"]

            }

        })



    return jsonify({

        "success":False

    })






# =====================================
# Пользователи
# =====================================

@app.route("/api/users")
def users():

    db = get_connection()


    result = db.execute(

        """
        SELECT id,username,role
        FROM users

        """

    ).fetchall()


    db.close()


    return jsonify(
        [
            dict(x)
            for x in result
        ]
    )







# =====================================
# Серверы
# =====================================

@app.route("/api/servers")
def get_servers():

    db = get_connection()


    result = db.execute(

        """
        SELECT *
        FROM servers

        """

    ).fetchall()


    db.close()



    return jsonify(
        [
            dict(x)
            for x in result
        ]
    )







@app.route("/api/servers",
methods=["POST"])
def create_server():

    data = request.json


    db = get_connection()


    db.execute(

        """
        INSERT INTO servers
        (
        user_id,
        name,
        game
        )

        VALUES (?,?,?)

        """,

        (
            data.get("user_id",1),

            data.get("name"),

            data.get("game")
        )

    )


    db.commit()

    db.close()



    return jsonify({

        "success":True

    })








@app.route(
"/api/servers/<int:id>/start",
methods=["POST"]
)
def start_server(id):


    db=get_connection()


    db.execute(

        """
        UPDATE servers
        SET status='online'
        WHERE id=?

        """,

        (id,)

    )


    db.commit()

    db.close()



    return jsonify({

        "success":True

    })







@app.route(
"/api/servers/<int:id>/stop",
methods=["POST"]
)
def stop_server(id):


    db=get_connection()


    db.execute(

        """
        UPDATE servers
        SET status='offline'
        WHERE id=?

        """,

        (id,)

    )


    db.commit()

    db.close()



    return jsonify({

        "success":True

    })








# =====================================
# Промокоды
# =====================================

@app.route(
"/api/promo/check",
methods=["POST"]
)
def promo_check():

    data=request.json


    code=data.get("code")



    db=get_connection()



    promo=db.execute(

        """
        SELECT *
        FROM promo_codes
        WHERE code=?
        AND active=1

        """,

        (code,)

    ).fetchone()



    db.close()



    if promo:

        return jsonify({

            "valid":True,

            "discount":
            promo["discount"]

        })



    return jsonify({

        "valid":False

    })






# =====================================
# Запуск
# =====================================

if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
