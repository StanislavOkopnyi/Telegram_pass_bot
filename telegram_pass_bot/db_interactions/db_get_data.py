from sqlite3 import Cursor
from types import NoneType
from typing import Any


def get_hash_pass(cur: Cursor, telegram_id: int) -> int | None:
    user = cur.execute("SELECT telegram_id, password_hash FROM users "
                       f"WHERE telegram_id = {telegram_id}; ")
    return tuple(user.fetchone())[1]


def get_all_passwords(cur: Cursor, telegram_id: int) -> list[Any]:
    passwords = cur.execute("SELECT telegram_id, service, password "
                            "FROM passwords "
                            f"WHERE telegram_id = {telegram_id}; ")
    return passwords.fetchall()


def get_service_passwords(cur: Cursor, telegram_id: int, service: str) -> list[Any]:
    passwords = cur.execute("SELECT telegram_id, service, password "
                            "FROM passwords "
                            f"WHERE telegram_id = {telegram_id} AND "
                            f"service = '{service}'; ")
    return passwords.fetchall()
