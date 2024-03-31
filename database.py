import sqlite3 as sq
import pickle


def create_table():
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
            user_id TEXT NOT NULL PRIMARY KEY,
            user_name TEXT NOT NULL
        )''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS items_list_table (
            user_id TEXT NOT NULL,
            message_id TEXT NOT NULL,
            items_list BLOB NOT NULL
        )''')

        con.commit()


def add_new_user(user_id, user_name):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        try:
            cur.execute('''
                INSERT INTO users
                VALUES (?, ?)
            ''', (user_id, user_name))
        except sq.IntegrityError:
            pass

        con.commit()


def create_item_list(user_id, message_id, items_list):
    seralized_data = pickle.dumps(items_list)
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''
            INSERT INTO items_list_table
            VALUES (?,?,?)
        ''', (user_id, message_id, seralized_data))

        con.commit()


def read_item_list(user_id, message_id):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''
            SELECT items_list FROM items_list_table
            WHERE user_id = ? AND message_id = ?
        ''', (user_id, message_id))

        raw_data = cur.fetchone()[0]
        items_list = pickle.loads(raw_data)

        return items_list


def edit_item_list(user_id, message_id, items_list):
    seralized_data = pickle.dumps(items_list)
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''
            UPDATE items_list_table
            SET items_list = ?
            WHERE user_id = ? AND message_id = ?
        ''', (seralized_data, user_id, message_id))

        con.commit()


def remove_item_list(user_id, message_id):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''
            DELETE FROM items_list_table
            WHERE user_id = ? AND message_id = ?
        ''', (user_id, message_id))

        con.commit()
