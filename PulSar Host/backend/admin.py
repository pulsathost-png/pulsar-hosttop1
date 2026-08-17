from flask import Blueprint, request, jsonify
from database import get_db
import secrets
from datetime import datetime, timedelta


admin = Blueprint("admin", __name__)


# Проверка администратора
def check_admin(token):

    db = get_db()

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE token=? AND role='admin'
        """,
        (token,)
    ).fetchone()

    db.close()

    return user



# Все пользователи
@admin.route("/admin/users", methods=["GET"])
def get_users():

    token = request.headers.get("token")

    if not check_admin(token):
        return jsonify({"error": "Нет доступа"}), 403


    db = get_db()

    users = db.execute(
        """
        SELECT id, username, balance, role
        FROM users
        """
    ).fetchall()


    return jsonify([
        dict(user)
        for user in users
    ])




# Выдать баланс
@admin.route("/admin/add_balance", methods=["POST"])
def add_balance():

    token = request.headers.get("token")

    if not check_admin(token):
        return jsonify({"error": "Нет доступа"}),403


    data = request.json

    user_id = data["user_id"]
    amount = data["amount"]


    db = get_db()

    db.execute(
        """
        UPDATE users
        SET balance = balance + ?
        WHERE id=?
        """,
        (amount,user_id)
    )


    db.commit()


    return jsonify({
        "message":"Баланс изменён"
    })





# Создание сервера пользователю
@admin.route("/admin/create_server", methods=["POST"])
def create_server():

    token = request.headers.get("token")

    if not check_admin(token):
        return jsonify({"error":"Нет доступа"}),403


    data = request.json


    user_id = data["user_id"]
    game = data["game"]
    ram = data.get("ram",2048)


    name = "PulSar-" + secrets.token_hex(3)


    db = get_db()


    db.execute(
        """
        INSERT INTO servers
        (user_id,name,game,ram,status,created)

        VALUES(?,?,?,?,?,?)
        """,
        (
            user_id,
            name,
            game,
            ram,
            "offline",
            datetime.now().isoformat()
        )
    )


    db.commit()


    return jsonify({
        "message":"Сервер создан",
        "server":name
    })





# Список серверов
@admin.route("/admin/servers", methods=["GET"])
def servers():

    token = request.headers.get("token")

    if not check_admin(token):
        return jsonify({"error":"Нет доступа"}),403


    db=get_db()

    servers=db.execute(
        """
        SELECT *
        FROM servers
        """
    ).fetchall()


    return jsonify([
        dict(server)
        for server in servers
    ])




# Продление сервера
@admin.route("/admin/extend_server", methods=["POST"])
def extend_server():

    token=request.headers.get("token")

    if not check_admin(token):
        return jsonify({"error":"Нет доступа"}),403


    data=request.json

    server_id=data["server_id"]


    db=get_db()


    db.execute(
        """
        UPDATE servers
        SET status='active'
        WHERE id=?
        """,
        (server_id,)
    )


    db.commit()


    return jsonify({
        "message":"Сервер продлён"
    })
