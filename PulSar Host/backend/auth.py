# =====================================
# 🌌 PulSar-Host v1.0
# Advanced Authentication System
# =====================================

from functools import wraps
from flask import request, jsonify
from database import get_connection
import secrets
from datetime import datetime, timedelta



# Временное хранилище токенов
# Позже можно перенести в таблицу sessions

sessions = {}



# =====================================
# Создание токена
# =====================================

def create_token(user_id):

    token = secrets.token_hex(32)


    sessions[token] = {

        "user_id": user_id,

        "created": datetime.now(),

        "expires":
        datetime.now() + timedelta(hours=24)

    }


    return token





# =====================================
# Получение пользователя
# =====================================

def get_current_user():


    token = request.headers.get(
        "Authorization"
    )


    if not token:

        return None



    session = sessions.get(
        token
    )


    if not session:

        return None




    if datetime.now() > session["expires"]:

        del sessions[token]

        return None





    db = get_connection()



    user = db.execute(

        """
        SELECT id,username,role,balance
        FROM users
        WHERE id=?

        """,

        (
            session["user_id"],
        )

    ).fetchone()



    db.close()



    return user





# =====================================
# Требуется авторизация
# =====================================

def login_required(function):


    @wraps(function)

    def wrapper(*args, **kwargs):


        user = get_current_user()



        if not user:


            return jsonify({

                "success":False,

                "error":
                "Требуется вход"

            }),401




        return function(
            *args,
            **kwargs
        )


    return wrapper






# =====================================
# Только администратор
# =====================================

def admin_required(function):


    @wraps(function)

    def wrapper(*args, **kwargs):


        user = get_current_user()



        if not user:


            return jsonify({

                "success":False,

                "error":
                "Нет авторизации"

            }),401





        if user["role"] != "admin":


            return jsonify({

                "success":False,

                "error":
                "Недостаточно прав"

            }),403





        return function(
            *args,
            **kwargs
        )


    return wrapper






# =====================================
# Проверка владельца сервера
# =====================================

def owner_required(function):


    @wraps(function)

    def wrapper(*args, **kwargs):


        user = get_current_user()



        if not user:


            return jsonify({

                "error":
                "Не авторизован"

            }),401





        return function(
            user,
            *args,
            **kwargs
        )


    return wrapper
