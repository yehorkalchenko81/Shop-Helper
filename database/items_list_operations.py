import sqlite3 as sq
import pickle


def create_item_list(user_id, message_id, items_list, keyboard):
    seralized_item_list = pickle.dumps(items_list)
    seralized_keyboard = pickle.dumps(keyboard)
    with sq.connect('../database.db') as con:
        cur = con.cursor()

        cur.execute('''
            INSERT INTO items_list_table
            VALUES (?, ?, ?, ?)
        ''', (user_id, message_id, seralized_item_list, seralized_keyboard))

        con.commit()


def read_item_list(user_id, message_id):
    with sq.connect('../database.db') as con:
        cur = con.cursor()

        cur.execute('''
            SELECT items_list, keyboard FROM items_list_table
            WHERE user_id = ? AND message_id = ?
        ''', (user_id, message_id))

        raw_item_list, raw_keyboard = cur.fetchone()
        items_list = pickle.loads(raw_item_list)
        keyboard = pickle.loads(raw_keyboard)

        return items_list, keyboard


def edit_item_list(user_id, message_id, items_list, keyboard):
    seralized_item_list = pickle.dumps(items_list)
    seralized_keyboard = pickle.dumps(keyboard)
    with sq.connect('../database.db') as con:
        cur = con.cursor()

        cur.execute('''
            UPDATE items_list_table
            SET items_list = ?, keyboard = ?
            WHERE user_id = ? AND message_id = ?
        ''', (seralized_item_list, seralized_keyboard, user_id, message_id))

        con.commit()


def remove_item_list(user_id, message_id):
    with sq.connect('../database.db') as con:
        cur = con.cursor()

        cur.execute('''
            DELETE FROM items_list_table
            WHERE user_id = ? AND message_id = ?
        ''', (user_id, message_id))

        con.commit()
