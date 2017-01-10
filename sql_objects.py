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
                    WHERE id = self.id;
                    ''', (self.title, self.uid))
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
    def __init__(self, vals):
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

    def __str__(self):
        return "{} : {}".format(self.text, "Yes" if self.completed else "No")

    def set_completed(self):
        self.completed = not self.completed

class User:
    def __init__(self, args):
        self.name, self.passwd, self.id = args
        #self.bucket = None

    def __str__(self):
        return "User(username={}, passwdHash={})".format(self.name, self.passwd)

    #def link_bucket(self, bucket):
        '''
        Links the bucket to the User instance.
        '''
        #self.bucket = bucket

    def add(self):
        '''
        Adds a user to the database,
        returns None if user already exists.
        '''
        #cur.execute("SELECT * FROM users WHERE username = ?;", (self.name,))
        #for row in cur:
        #    raise UserExistsError("User {} already Exists!!!".format(self.name))
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?);', (self.name, self.passwd))
        conn.commit()

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

        return User(*row)

#Setup the users table
#Insert sql here?


g = Item(('Complete the website to MVP standards. ', 0))
g1 = Item(('Complete the website to MVP+1 standards. ', 0))
g2 = Item(('Complete the website to MVP+2 standards. ', 0))
bucket = List("Website Goals", g, g1, g2)
for a in bucket:
    print(a)
user = User(('mitchell', 'hello'))
print(User.add_user(user))
user = User.get('mitchell')
print(user)
cur.execute("SELECT * from users")
for row in cur:
    print(row)
