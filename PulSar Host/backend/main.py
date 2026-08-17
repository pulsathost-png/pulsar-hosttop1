from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from database import init_db, get_db
from auth import auth
from admin import admin


load_dotenv()


app = Flask(__name__)

CORS(app)


# Запуск базы данных
init_db()


# Подключение маршрутов
app.register_blueprint(auth)
app.register_blueprint(admin)



@app.route("/")
def home():
    return jsonify({
        "name": "PulSar-Host",
        "version": "1.0",
        "status": "online"
    })



@app.route("/api/status")
def status():
    return jsonify({
        "service": "PulSar-Host API",
        "online": True
    })



# Профиль пользователя
@app.route("/api/profile", methods=["GET"])
def profile():

    token = request.headers.get("token")

    if not token:
        return jsonify({
            "error": "Token отсутствует"
        }), 401


    db = get_db()

    user = db.execute(
        """
        SELECT id, username, balance, role
        FROM users
        WHERE token=?
        """,
        (token,)
    ).fetchone()


    if not user:
        return jsonify({
            "error": "Пользователь не найден"
        }), 404


    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "balance": user["balance"],
        "role": user["role"]
    })



# Тест API
@app.route("/api/test")
def test():

    return jsonify({
        "message": "PulSar-Host API работает!"
    })



# Ошибка 404
@app.errorhandler(404)
def error_404(error):

    return jsonify({
        "error": "Маршрут не найден"
    }), 404



if __name__ == "__main__":

    port = int(os.getenv("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
