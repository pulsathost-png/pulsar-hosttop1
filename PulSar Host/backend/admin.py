from flask import Blueprint, request, jsonify
from database import get_db
from auth import verify_token

admin = Blueprint("admin", __name__)


def admin_required():
    token = request.headers.get("Authorization")

    if not token:
        return None, jsonify({"error": "Token required"}), 401

    user = verify_token(token)

    if not user:
        return None, jsonify({"error": "Invalid token"}), 401

    if user["role"] != "admin":
        return None, jsonify({"error": "Admin access required"}), 403

    return user, None, None


# Получить всех пользователей
@admin.route("/admin/users", methods=["GET"])
def get_users():
    user, error, code = admin_required()

    if error:
        return error, code

    db = get_db()
    users = db.execute(
        "SELECT id, username, email, role FROM users"
    ).fetchall()

    return jsonify([
        dict(u) for u in users
    ])


# Получить все игровые серверы
@admin.route("/admin/servers", methods=["GET"])
def get_servers():
    user, error, code = admin_required()

    if error:
        return error, code

    db = get_db()
    servers = db.execute(
        "SELECT * FROM servers"
    ).fetchall()

    return jsonify([
        dict(s) for s in servers
    ])


# Создать сервер
@admin.route("/admin/server/create", methods=["POST"])
def create_server():
    user, error, code = admin_required()

    if error:
        return error, code

    data = request.json

    name = data.get("name")
    game = data.get("game")
    ram = data.get("ram")

    db = get_db()

    db.execute(
        """
        INSERT INTO servers
        (name, game, ram, status)
        VALUES (?, ?, ?, ?)
        """,
        (name, game, ram, "offline")
    )

    db.commit()

    return jsonify({
        "message": "Server created"
    })


# Удалить сервер
@admin.route("/admin/server/delete/<int:id>", methods=["DELETE"])
def delete_server(id):
    user, error, code = admin_required()

    if error:
        return error, code

    db = get_db()

    db.execute(
        "DELETE FROM servers WHERE id=?",
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Server deleted"
    })
