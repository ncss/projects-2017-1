import sqlite3
from api_errors import *
from classes import *

conn = sqlite3.connect('database.db')
cur = conn.cursor()

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
