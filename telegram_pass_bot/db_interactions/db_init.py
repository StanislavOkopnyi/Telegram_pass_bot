import sqlite3
from sqlite3 import Connection, Cursor, OperationalError


PATH_TO_DB = "pass.db"


def create_tables(con: Connection, cur: Cursor) -> None:

    # Creates table to keep telegram_ids and hashed passwords
    cur.execute("CREATE TABLE [IF NOT EXISTS] users( "
                "telegram_id BIGINT NOT NULL UNIQUE, "
                "password_hash BIGINT NOT NULL "
                "); ")
    # Creates table to keep telegram_ids, services and passwords for them
    cur.execute("CREATE TABLE [IF NOT EXISTS] passwords( "
                "telegram_id BIGINT NOT NULL, "
                "service VARCHAR(80) NOT NULL, "
                "password VARCHAR(80) NOT NULL "
                "); ")

    con.commit()


def check_tables(cur: Cursor) -> bool:
    try:
        cur.execute("SELECT * FROM users; ")
    except OperationalError:
        return False
    try:
        cur.execute("SELECT * FROM passwords; ")
    except OperationalError:
        return False
    return True


def init() -> tuple[Connection, Cursor]:

    with open(PATH_TO_DB, "a") as _:
        pass

    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()

    if not check_tables(cur):
        create_tables(con, cur)

    return con, cur
