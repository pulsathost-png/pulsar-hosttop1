from flask import Blueprint, request, jsonify
from database import get_db
import hashlib
import secrets


auth = Blueprint("auth", __name__)


# Хеш пароля
def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



# Регистрация
@auth.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data["username"]
    password = data["password"]


    db = get_db()


    check = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()


    if check:
        return jsonify({
            "error":"Пользователь уже существует"
        }),400



    token = secrets.token_hex(32)


    db.execute(
        """
        INSERT INTO users
        (username,password,token)

        VALUES(?,?,?)
        """,
        (
            username,
            hash_password(password),
            token
        )
    )


    db.commit()


    return jsonify({

        "message":"Аккаунт создан",

        "token":token

    })





# Авторизация
@auth.route("/login", methods=["POST"])
def login():

    data=request.json


    username=data["username"]
    password=hash_password(
        data["password"]
    )


    db=get_db()


    user=db.execute(
        """
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """,
        (
            username,
            password
        )
    ).fetchone()



    if not user:

        return jsonify({
            "error":"Неверный логин или пароль"
        }),401



    token=secrets.token_hex(32)


    db.execute(
        """
        UPDATE users
        SET token=?
        WHERE id=?
        """,
        (
            token,
            user["id"]
        )
    )


    db.commit()



    return jsonify({

        "message":"Вход выполнен",

        "token":token,

        "role":user["role"]

    })





# Выход
@auth.route("/logout", methods=["POST"])
def logout():

    token=request.headers.get("token")


    db=get_db()


    db.execute(
        """
        UPDATE users
        SET token=NULL
        WHERE token=?
        """,
        (token,)
    )


    db.commit()


    return jsonify({
        "message":"Вы вышли"
    })
