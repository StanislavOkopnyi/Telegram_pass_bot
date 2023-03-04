from sqlite3 import Cursor
from typing import Any


def get_hash_pass(cur: Cursor, telegram_id: int) -> int | None:
    user = cur.execute("SELECT telegram_id, password_hash FROM users "
                       f"WHERE telegram_id = {telegram_id}; ")
    user = user.fetchone()
    if user:
        return user[1]


def get_all_passwords(cur: Cursor, telegram_id: int) -> list[tuple]:
    passwords = cur.execute("SELECT telegram_id, service, password "
                            "FROM passwords "
                            f"WHERE telegram_id = {telegram_id}; ")
    passwords = passwords.fetchall()
    if passwords:
        passwords = list(map(lambda x: (x[1], x[2]), passwords))
    return passwords


def get_service_passwords(cur: Cursor, telegram_id: int, service: str) -> list[Any]:
    passwords = cur.execute("SELECT telegram_id, service, password "
                            "FROM passwords "
                            f"WHERE telegram_id = {telegram_id} AND "
                            f"service = '{service}'; ")
    return passwords.fetchall()
