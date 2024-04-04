import sqlite3 as sq


def add_shop_card(user_id, shop_name, shop_card):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''
            INSERT INTO shop_cards
            VALUES (?, ?, ?)
        ''', (user_id, shop_name, shop_card))

        con.commit()


def read_shop_cards(user_id):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''
            SELECT shop_name, shop_card FROM shop_cards
            WHERE user_id = ?
        ''', (user_id,))

        rows = cur.fetchall()

        return rows


def remove_shop_cards(user_id, shop_nmae):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''
            DELETE FROM shop_cards
            WHERE user_id = ? AND shop_name = ?
        ''', (user_id, shop_nmae))

        con.commit()
