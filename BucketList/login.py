import sqlite3

class User:

    @staticmethod
    def login(username, password):
        cur = conn.execute('''
          SELECT id
          FROM User
          WHERE username?
          AND password=?
        ''', (username, password))
        row = cur.fetchone()
        user_id = None if row is None else row['id']
        conn.commit()
        return user_id

    @staticmethod
    def find(username):
        cur = conn.execute('''
            SELECT *
            FROM User
            Where username=?''', (username,))
        row = cur.fetchone()
        if row is None:
            raise UserNotFound('{} does not exist'.format(username))
        return User(row[0]

    @staticmethod
    def create(username, password):
        cur = conn.execute('''
            INSERT INTO User
            VALUES (?, ?)''', (username, password))
        return User(username, password)

    @staticmethod
    def delete(username):
        cur = conn.execute('''
            DELETE FROM User
            WHERE username = ?''', (username,))
