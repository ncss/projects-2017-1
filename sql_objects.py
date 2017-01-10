import sqlite3
from api_errors import *
from classes import *

conn = sqlite3.connect('database.db')
cur = conn.cursor()

class List:
    def __init__(self, title, *args):
        self.title = title
        self.items = [a for a in args]
        self.i = -1

    def __iter__(self):
        return iter(self.items)

    def add(self, user):
        '''
        Add a bucket list to the given user,
        Throws an error if user doesn't exist
        or bucket object invalid
        '''
        pass

    def update(self, user, **kwargs):
        '''
        Edit the bucket of a given user,
        changes are passed in through a
        dictionary.
        //TODO fix how data is passed in
        '''
        pass

    def delete(self):
        cur.execute('''

                    ''')
        pass

    def search(self):
        pass

    @staticmethod
    def get(user):
        '''
        Get the bucket data of a given user
        '''
        cur.execute()##Insert SQL Here
        cer.fetchone()
        for row in cur:
            title, *args = row
            return List(title, args)
        raise BucketNotFoundError("Bucket List of {} not found".format(user.name))


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
        self.name, self.passwd = args
        self.bucket = None

    def __str__(self):
        return "User(username={}, passwdHash={})".format(self.name, self.passwd)

    def link_bucket(self, bucket):
        '''
        Links the bucket to the User instance.
        '''
        self.bucket = bucket

    def add(self):
        '''
        Adds a user to the database,
        returns None if user already exists.
        '''
        cur.execute("SELECT * FROM users WHERE username = ?", (self.name,))
        for row in cur:
            raise UserExistsError("User {} already Exists!!!".format(self.name))
        cur.execute('INSERT INTO users VALUES (NULL, ?, ?)', (self.name, self.passwd))
        conn.commit()

    def update(self):
        ##TODO fix this SQL
        cur.execute('''
                    UPDATE users
                    SET
                    ''')

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
                    WHERE username = ?
                    ''', (self.name,))
        conn.commit()

    @staticmethod
    def get(username):
        '''
        Get a User object with the details of the found user,
        returns None if no user found
        '''
        cur.execute('''SELECT u.username, u.password
                        FROM users u
                        WHERE u.username = ?;''', (username,))
        cur.fetchone()
        for row in cur:
            return User(row)
        print("Error! User not found!")
        return None

#Setup the users table


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
