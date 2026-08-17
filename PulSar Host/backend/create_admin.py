from database import get_db, init_db
import hashlib
import secrets


# Создание админа

def create_admin():

    init_db()

    db = get_db()


    username = "admin"
    password = "admin123"


    # Проверяем есть ли админ
    check = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()


    if check:
        print("Администратор уже существует")
        return



    token = secrets.token_hex(32)


    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()



    db.execute(
        """
        INSERT INTO users
        (
        username,
        password,
        token,
        balance,
        role
        )

        VALUES(?,?,?,?,?)
        """,
        (
            username,
            password_hash,
            token,
            0,
            "admin"
        )
    )


    db.commit()

    db.close()


    print("Администратор создан!")
    print("Логин:", username)
    print("Пароль:", password)
    print("Token:", token)




if __name__ == "__main__":

    create_admin()
