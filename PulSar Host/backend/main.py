# =====================================
# 🌌 PulSar-Host v1.0
# Python Backend
# =====================================

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import uuid


app = Flask(__name__)

# Разрешаем подключение frontend
CORS(app)



# =====================================
# Временное хранилище
# Потом подключим database.py
# =====================================

users = []

servers = []

promo_codes = [
    {
        "code": "PULSAR35",
        "discount": 35,
        "active": True
    }
]



# =====================================
# Главная
# =====================================

@app.route("/")
def home():

    return jsonify({

        "project": "PulSar-Host",

        "version": "1.0.0",

        "status": "online",

        "time": datetime.now()

    })





# =====================================
# Статус системы
# =====================================

@app.route("/api/status")
def status():

    return jsonify({

        "hosting": "PulSar-Host",

        "online": True,

        "servers": len(servers),

        "users": len(users)

    })






# =====================================
# Пользователи
# =====================================

@app.route("/api/register", methods=["POST"])
def register():

    data = request.json


    user = {

        "id": str(uuid.uuid4()),

        "username": data.get("username"),

        "password": data.get("password"),

        "role": "user",

        "created":
        str(datetime.now())

    }


    users.append(user)


    return jsonify({

        "success": True,

        "user": user

    })






@app.route("/api/users")
def get_users():

    return jsonify(users)






# =====================================
# Серверы
# =====================================


@app.route("/api/servers", methods=["GET"])
def get_servers():

    return jsonify(servers)






@app.route("/api/servers", methods=["POST"])
def create_server():

    data = request.json


    server = {

        "id": str(uuid.uuid4()),

        "name": data.get("name"),

        "game": data.get("game"),

        "status": "offline",

        "created":
        str(datetime.now())

    }


    servers.append(server)


    return jsonify({

        "success": True,

        "server": server

    })






@app.route("/api/servers/<server_id>/start",
methods=["POST"])
def start_server(server_id):


    for server in servers:

        if server["id"] == server_id:

            server["status"] = "online"


            return jsonify({

                "success": True,

                "message":
                "Сервер запущен"

            })


    return jsonify({

        "error":
        "Сервер не найден"

    }),404







@app.route("/api/servers/<server_id>/stop",
methods=["POST"])
def stop_server(server_id):


    for server in servers:

        if server["id"] == server_id:

            server["status"] = "offline"


            return jsonify({

                "success": True,

                "message":
                "Сервер остановлен"

            })


    return jsonify({

        "error":
        "Сервер не найден"

    }),404







# =====================================
# Промокоды
# =====================================


@app.route("/api/promo/check",
methods=["POST"])
def check_promo():


    data = request.json


    code = data.get("code")



    for promo in promo_codes:


        if promo["code"] == code and promo["active"]:


            return jsonify({

                "valid": True,

                "discount":
                promo["discount"]

            })



    return jsonify({

        "valid": False

    })






# =====================================
# Ошибки
# =====================================

@app.errorhandler(500)
def error(error):

    return jsonify({

        "error":
        "Внутренняя ошибка сервера"

    }),500





# =====================================
# Запуск
# =====================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
