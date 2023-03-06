from sqlite3 import Connection, Cursor


def delete_from_db(con: Connection, cur: Cursor, telegram_id: int, service: str):
    cur.execute("DELETE FROM passwords "
                f"WHERE telegram_id = {telegram_id} "
                f"AND service = '{service}'; ")
    con.commit()


def delete_all(con: Connection, cur: Cursor, telegram_id: int):
    cur.execute("DELETE FROM passwords "
                f"WHERE telegram_id = {telegram_id}; ")
    con.commit()
