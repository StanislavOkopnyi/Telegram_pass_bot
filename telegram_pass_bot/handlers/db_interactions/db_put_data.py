from sqlite3 import Connection, Cursor


def put_user_in_db(con: Connection, cur: Cursor, telegram_id: int, password_hash: int) -> None:
    cur.execute("INSERT INTO users(telegram_id, password_hash) "
                f"VALUES ({telegram_id}, {password_hash}); ")
    con.commit()


def put_service_pass_in_db(con: Connection, cur: Cursor, telegram_id: int, service: str, password: str) -> None:

    if len(service) > 80:
        raise Exception("Service length too long!")

    cur.execute("INSERT INTO passwords(telegram_id, service, password) "
                f"VALUES ({telegram_id}, '{service}', '{password}'); ")
    con.commit()
