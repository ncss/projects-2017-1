import sqlite3
from api_errors import *

conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class List:
    def __init__(self, title, uid, id):
        self.title = title
        self.uid = uid
        self.id = id

    def add(self):
        '''
        Add a bucket list to the given user,
        Throws an error if user doesn't exist
        or bucket object invalid
        '''
        cur.execute('INSERT INTO lists (uid, title) VALUES (?, ?);', (self.uid, self.title))
        conn.commit()

    def update(self):
        '''
        Edit the bucket list of a given user.
        '''
        cur.execute('''
                    UPDATE lists
                    SET title = ?, userid = ?
                    WHERE id = ?;
                    ''', (self.title, self.uid, self.id))
        conn.commit()

    def delete(self):
        cur.execute('''
                    DELETE FROM lists
                    WHERE id = ?;
                    ''', (self.id,)
                   )
        conn.commit()

    def search(self):
        pass

    @staticmethod
    def get(list_id):
        '''
        Get the bucket data of a given user
        '''
        cur.execute('''
                    SELECT title, userid, id
                    FROM lists
                    WHERE id = ?;
                    ''', (list_id,))
        row = cur.fetchone()
        #title, uid, id = row
        return List(*row)
        #raise BucketNotFoundError("Bucket List of {} not found".format(user.name))


class Item:
    def __init__(self, vals, id, list_id):
        self.completed = False
        self.text = ''
        self.image = ''
        for a in vals:
            if isinstance(a, int):
                self.completed = bool(a)
            elif a.startswith('static/'):
                self.image = a.strip()
            else:
                self.text = a.strip()
        self.id  = id
        self.list_id = list_id

    def __str__(self):
        return "{} : {}".format(self.text, "Yes" if self.completed else "No")

    def set_completed(self):
        self.completed = not self.completed

    def add(self):
        '''
        Add a bucket list item to the database.
        '''
        cur.execute('INSERT INTO items (listid, text, completed, image) VALUES (?, ?, ?, ?);', (self.list_id, self.text, int(self.completed), self.image))
        conn.commit()

    @staticmethod
    def get(item_id):
        '''
        Get an item object given an item id.
        '''
        cur.execute('''
                    SELECT completed, text, image, list_id
                    FROM items WHERE id = ?;
                    ''', (item_id))
        row = cur.fetchone()
        *val, list_id = row
        return Item(val, item_id, list_id)

    def search(self):
        pass

    def update(self):
        '''
        Push item changes to the database.
        '''
        cur.execute('''
                    UPDATE items
                    SET list_id = ?, text = ?, image = ?, completed = ?
                    WHERE id = ?
                    ''', (self.list_id, self.text, self.image, int(self.completed), self.id))
        conn.commit()

    def delete(self):
        '''
        Delete the item from the list.
        '''
        cur.execute('''
                    DELETE FROM items WHERE id = ?
                    ''', (self.id,))
        conn.commit()

class User:
    def __init__(self, name, passwd):
        self.name, self.password = (name, passwd)
        self.id = -1

    def __str__(self):
        return "User(username={}, passwdHash={})".format(self.name, self.password)

    def add(self):
        '''
        Adds a user to the database,
        returns None if user already exists.
        '''
        #cur.execute("SELECT * FROM users WHERE username = ?;", (self.name,))
        #for row in cur:
        #    raise UserExistsError("User {} already Exists!!!".format(self.name))
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?);', (self.name, self.password))
        conn.commit()
        self.id = cur.lastrowid

    def update(self):
        '''
            Does this update the user's password?
        '''
        cur.execute('''
                    UPDATE users
                    SET password = ?
                    WHERE id = ?
                    ''', (self.password, self.id))
        conn.commit()

    def search(self):
        ##TODO fill this out
        pass

    def delete(self):
        '''
        Deletes a user,
        !!!Check for authentication first!!!
        '''
        cur.execute('''
                    DELETE FROM users
                    WHERE username = ?;
                    ''', (self.name,))
        conn.commit()

    @staticmethod
    def get(username):
        '''
        Get a User object with the details of the found user,
        returns None if no user found
        '''
        cur.execute('''SELECT username, password, id
                        FROM users u
                        WHERE u.username = ?;''', (username,))
        row = cur.fetchone()
        name, password, id = row
        try:
            return User(name, password, id)
        except:
            return None
