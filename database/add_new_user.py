import sqlite3 as sq


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
