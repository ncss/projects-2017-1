import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

def auth_required(fn):
    def inner(user, *args):
        return fn()
    return inner


class Bucket:
    def __init__(self, title, *args):
        self.title = title
        self.items = [a for a in args]
        self.i = -1

    def __iter__(self):
        return iter(self.items)

    @staticmethod
    @auth_required
    def add_bucket(user):
        pass

    @staticmethod
    @auth_required
    def edit_bucket(user, **kwargs):
        pass

    @staticmethod
    def get(bucket):
        cur.execute()##Insert SQL Here
        cer.fetchone()
        for row in cur:
            title, *args = row
            return Bucket(title, args)


class Goal:
    def __init__(self, vals):
        self.completed = False
        self.text = ''
        for a in vals:
            if isinstance(a, int):
                self.completed = bool(a)
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

    @staticmethod
    def add_user(user):
        '''
        Adds a user to the database, gets passed a User object,
        returns None if user already exists.
        '''
        cur.execute("SELECT * FROM User WHERE username = ?", (user.name,))
        for row in cur:
            return None
        cur.execute('INSERT INTO User VALUES (NULL, ?, ?)', (user.name, user.passwd))
        conn.commit()

    @staticmethod
    @auth_required
    def delete_user(user):
        '''
        Deletes a user, gets passed a user object,
        Checks for authentication first.
        '''
        cur.execute('')

    @staticmethod
    @auth_required
    def edit_user(user, **kwargs):
        '''
        Edit the details of a user as passed in a dictionary
        '''
        pass

    @staticmethod
    def get(username):
        '''
        Get a User object with the details of the found user,
        returns None if no user found
        '''
        cur.execute('''SELECT u.username, u.password
                        FROM User u
                        WHERE u.username = ?;''', (username,))##Insert SQL Here
        cur.fetchone()
        for row in cur:
            print(row)
            return User(row)
        print("Error! User not found!")
        return None

#Setup the users table
#print(' '.join(open("UserSQL").read().split("\n")))
#cur.executescript(open("UserSQL").read())

g = Goal(('Complete the website to MVP standards. ', 0))
g1 = Goal(('Complete the website to MVP+1 standards. ', 0))
g2 = Goal(('Complete the website to MVP+2 standards. ', 0))
bucket = Bucket("Website Goals", g, g1, g2)
for a in bucket:
    print(a)
user = User(('mitchell', 'hello'))
print(User.add_user(user))
user = User.get('mitchell')
print(user)
cur.execute("SELECT * from User")
for row in cur:
    print(row)
