from sqlite3 import Connection, Cursor
import zlib


def put_user_in_db(con: Connection, cur: Cursor,
                   telegram_id: int, password: str) -> None:
    """Creates user in database"""
    password_hash = get_password_hash(password)
    cur.execute("INSERT INTO users(telegram_id, password_hash) "
                f"VALUES ({telegram_id}, {password_hash}); ")
    con.commit()


def put_service_pass_in_db(con: Connection, cur: Cursor, telegram_id: int,
                           service: str, password: str) -> None:
    """Creates service with password in database"""
    if len(service) > 80:
        raise Exception("Service length too long!")

    cur.execute("INSERT INTO passwords(telegram_id, service, password) "
                f"VALUES ({telegram_id}, '{service}', '{password}'); ")
    con.commit()


def get_password_hash(password: str) -> int:
    """Returns password hash from password"""
    return zlib.crc32(bytes(password, encoding="utf8"))
