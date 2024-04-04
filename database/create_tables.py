import sqlite3 as sq


def create_tables():
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER NOT NULL PRIMARY KEY,
            user_name TEXT NOT NULL
        )''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS items_list_table (
            user_id TEXT NOT NULL,
            message_id TEXT NOT NULL,
            items_list BLOB NOT NULL,
            cancel_fsm_button BLOB NOT NULL
        )''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS shop_cards (
            user_id INTEGER NOT NULL,
            shop_name TEXT NOT NULL,
            shop_card INTEGER NOT NULL
        )''')

        con.commit()
