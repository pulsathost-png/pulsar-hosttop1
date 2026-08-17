# =====================================
# 🌌 PulSar-Host v1.0
# Admin Creator System
# =====================================

from database import init_database, get_connection
from werkzeug.security import generate_password_hash
from datetime import datetime
import getpass



# Инициализация базы

init_database()



print("""
=================================
🌌 PulSar-Host Admin Creator
=================================
""")



# Получаем данные

username = input(
    "Введите логин администратора: "
).strip()



password = getpass.getpass(
    "Введите пароль администратора: "
)



if not username or not password:

    print(
        "❌ Логин и пароль обязательны"
    )

    exit()





db = get_connection()



try:


    # Проверяем пользователя

    existing = db.execute(

        """
        SELECT *
        FROM users
        WHERE username=?

        """,

        (username,)

    ).fetchone()





    if existing:


        print(
            "⚠️ Такой пользователь уже существует"
        )


        # Обновляем роль

        db.execute(

            """
            UPDATE users
            SET role='admin'

            WHERE username=?

            """,

            (username,)

        )


        db.commit()



        print(
            "👑 Пользователь назначен администратором"
        )



    else:


        # Создание нового админа

        db.execute(

            """
            INSERT INTO users
            (
            username,
            password,
            role
            )

            VALUES (?,?,?)

            """,

            (

                username,

                generate_password_hash(
                    password
                ),

                "admin"

            )

        )


        db.commit()



        print(
            "✅ Администратор успешно создан"
        )





    # Запись в логи

    db.execute(

        """
        INSERT INTO logs
        (
        action
        )

        VALUES (?)

        """,

        (

        f"Создан администратор {username}"

        )

    )


    db.commit()





except Exception as error:


    print(
        "❌ Ошибка:",
        error
    )



finally:


    db.close()





print("""
=================================
🚀 PulSar-Host Admin Ready
=================================
""")
