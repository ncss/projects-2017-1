import sqlite3
import datetime

class UserExistsError(Exception):
    pass

class BucketNotFoundError(Exception):
    pass

conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class List:
    def __init__(self, title, uid, id=None, created=None):
        self.title = title
        self.uid = uid
        self.id = id
        self.created = created

    def __str__(self):
        return self.title

    def add(self):
        '''
        Add a bucket list to the given user,
        Throws an error if user doesn't exist
        or bucket object invalid
        '''
        self.created = datetime.datetime.now()
        cur.execute('INSERT INTO lists (userid, title, created) VALUES (?, ?, ?);', (self.uid, self.title, self.created))
        conn.commit()
        self.id = cur.lastrowid

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

    @staticmethod
    def search(**kwargs):

        search_key = ''
        search_value = ''

        search_options = ['id', 'userid', 'title']

        for key, value in kwargs:

            if value is not None and key in search_options:
                search_key = key
                search_value = value

        cur.execute('''

            SELECT title, userid, id
            FROM lists
            WHERE {} = ?
            '''.format(search_key), (search_value,)
        )

        rows = cur.fetchall()

        return [List(*row) for row in rows]

    @staticmethod
    def get(list_id):
        '''
        Get the bucket data of a given user
        '''
        cur.execute('''
                    SELECT title, userid, id, created
                    FROM lists
                    WHERE id = ?;
                    ''', (list_id,))
        row = cur.fetchone()
        if row is not None:
            title, uid, id, created = row
            return List(title, uid, id, created)
        return None

    @staticmethod
    def get_user_lists(user):
        '''
        Get the bucket lists of a given user
        '''
        cur.execute('''
                    SELECT title, userid, id, created
                    FROM lists
                    WHERE userid = ?;
                    ''', (user.id,))
        lists = []
        for row in cur:
            title, uid, id, created = row
            lists.append(List(title, uid, id, created))
        return lists

   def get_items(self):
       cur.execute('''SELECT listid, completed, text, image, id
                      FROM items
                      WHERE listid=?;''' (self.id,)
     items = []
     for row in cur:
         listid, completed, text, image, id = row
         items.append(Item(listid, completed, text, image, id))
     return items

class Item:
    def __init__(self, list_id, completed=False, text=None, image=None, id=None):
        self.completed = completed
        if text is None and image is None:
            raise ValueError('Either text or image must be declared!!!')
        self.text = text
        self.image = image
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
        cur.execute('''INSERT INTO items (listid, text, completed, image)
                    VALUES (?, ?, ?, ?);''',
                    (self.list_id, self.text, int(self.completed), self.image))

        conn.commit()
        self.id = cur.lastrowid

    @staticmethod
    def get(item_id):
        '''
        Get an item object given an item id.
        '''
        cur.execute('''
                    SELECT completed, text, image, listid
                    FROM items WHERE id = ?;
                    ''', (item_id,))
        row = cur.fetchone()
        if row is not None:
            completed, text, image, list_id = row
            return Item(list_id, completed, text, image, item_id)
        return None

    def search(self, id=None, list_id=None, text=None, rank=None, completed=None, image=None):

        search_key = ''
        search_value = ''

        for key, value in **kwargs.items():
            if value is not None:
                search_key = key
                search_value = value

        cur.execute('''

        SELECT id, list_id, text, rank, completed, image
        FROM items
        WHERE {} = ?
        '''.format(search_key), (search_value,))

        rows = cur.fetchall()

        return [List(*row) for row in rows]

    def update(self):
        '''
        Push item changes to the database.
        '''
        cur.execute('''
                    UPDATE items
                    SET listid = ?, text = ?, image = ?, completed = ?
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
    def __init__(self, name, passwd, id=None):
        self.name, self.password = (name, passwd)
        self.id = id

    def __str__(self):
        return "User(username={}, passwdHash={})".format(self.name, self.password)

    def add(self):
        '''
        Adds a user to the database,
        returns None if user already exists.
        '''
        cur.execute("SELECT * FROM users WHERE username = ?;", (self.name,))
        for row in cur:
            raise UserExistsError("User {} already Exists!!!".format(self.name))
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

    def search(self, username=None, id=None):

        search_key = ''
        search_value = ''
        # Does kwargs need to be defined?
        for key,value in **kwargs.items():
            if value is not None:
                search_key = key
                search_value = value

        cur.execute('''

        SELECT from username, password, id
        FROM users
        WHERE {} = ?
        '''.format(search_key), (search_value,))

        rows = cur.fetchall()

        return [List(*row) for row in rows]

    def delete(self):
        '''
        Deletes a user,
        !!!Check for authentication first!!!
        '''
        for i in List.get_user_lists(self):
            i.delete()

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
        if row is not None:
            name, password, id = row
            return User(name, password, id)
        return None

    @staticmethod
    def get_by_id(id):
        '''
        Get a User object with the details of the found user,
        returns None if no user found
        '''
        cur.execute('''SELECT username, password, id
                        FROM users u
                        WHERE u.id = ?;''', (id,))
        row = cur.fetchone()
        if row is not None:
            name, password, id = row
            return User(name, password, id)
        return None

        '''
        Get the bucket lists of a given user
        '''
        cur.execute('''
                    SELECT title, userid, id, created
                    FROM lists
                    WHERE userid = ?;
                    ''', (self.id,))
        lists = []
        for row in cur:
            title, userid, id, created = row
            lists.append(List(title, userid, id, created))
        return lists

    def get_newsfeed(self):
        '''
        Gets the items for newsfeed (lists other than active user)
        '''
        cur.execute('''SELECT title, userid, id, created
                    FROM lists
                    WHERE userid != ?
                    ''', (self.id,))
        lists = []
        for row in cur:
            title, uid, id, created = row
            lists.append(List(title, uid, id, created))
        return lists


if __name__ == "__main__":
    u2 = User('test1', 'testp')
    u2.add()
    u2.password = "windowsisBad123"
    u2.update()
    l = List("test list for user test1", u2.id)
    l.add()
    l.title += "HUZZAH"
    l.update()
    l2 = List.get(l.id)
    i = Item(l.id, text="Test goal for life")
    i.add()
    i2 = Item(l.id, image="test.png")
    i2.add()
    i2.set_completed()
    i2.update()
    item = Item.get(i2.id)
    print(l)
    print(l2)
    print(i)
    print(i2)
    print(item)
    item.delete()
    i.delete()
    l.delete()
    u2.delete()
