import sqlite3
import datetime
import hashlib

class UserExistsError(Exception):
    pass

class BucketNotFoundError(Exception):
    pass

conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class List:
    def __init__(self, title, userid, id=None, created=None):
        if title == "":
            title = User.get_by_id(userid).name+"'s Bucket List"
        self.title = title
        self.userid = userid
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
        cur.execute('INSERT INTO lists (userid, title, created) VALUES (?, ?, ?);', (self.userid, self.title, self.created))
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
                    ''', (self.title, self.userid, self.id))
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

        search_keys = []
        search_values = []

        search_options = ['title', 'userid', 'id', 'created']

        for key, value in kwargs.items():
            if value is not None and key in search_options:
                search_keys.append(key + '=?')
                search_values.append(value)

        if search_keys == [] or search_values == []:
            return "Invalid search"

        cur.execute('''
            SELECT title, userid, id, created
            FROM lists
            WHERE {}
            '''.format(' AND '.join(search_keys)), tuple(search_values)
        )

        rows = cur.fetchall()

        return [List(*row) for row in rows]

    @staticmethod
    def get(listid):
        '''
        Get the bucket data of a given user
        '''
        cur.execute('''
                    SELECT title, userid, id, created
                    FROM lists
                    WHERE id = ?;
                    ''', (listid,))
        row = cur.fetchone()
        if row is not None:
            title, userid, id, created = row
            return List(title, userid, id, created)
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
            title, userid, id, created = row
            lists.append(List(title, userid, id, created))
        return lists

    def get_items(self):
        cur.execute('''SELECT listid, completed, text, image, id
                       FROM items
                       WHERE listid=?;''', (self.id,))
        items = []
        for row in cur:
            listid, completed, text, image, id = row
            items.append(Item(listid, completed, text, image, id))
        return items


    @staticmethod
    def get_newest():
        '''
        Get bucket lists by creation date
        '''
        cur.execute('''
                    SELECT created, title, userid, id
                    FROM lists
                    ORDER BY created DESC
                    ''')
        create = []
        for row in cur:
            created, title, userid, id = row
            create.append(List(title, userid, id, created))
        return create

    def new_item(self, text=None, image=None):
        '''
        Add a new item.
        '''
        i = Item(self.id, False, text, image)
        i.add()
        return i

class Item:
    def __init__(self, list_id, completed=False, text=None, image="", id=None):
        self.completed = completed
        if text is None and image == "":
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

    @staticmethod
    def search(**kwargs):

        search_keys = []
        search_values = []

        search_options = ['id', 'listid', 'text', 'completed', 'image']

        for key, value in kwargs.items():
            if value is not None and key in search_options:
                search_keys.append(key + ' = ?')
                search_values.append(value)

        if search_keys == [] or search_values == []:
            return "Invalid search"

        cur.execute('''
            SELECT listid, completed, text, image, id
            FROM items
            WHERE {}
            '''.format(' AND '.join(search_keys)), tuple(search_values)
        )

        rows = cur.fetchall()

        return [Item(*row) for row in rows]

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
    def __init__(self, name, passwd, email="", image='/static/img/user_def.png', rname='', id=None, shouldHash=True):
        if not rname:
            rname = name
        if shouldHash:
            m = hashlib.sha256()
            m.update(passwd.encode())
            self.password = m.hexdigest()
        else:
            self.password = passwd
        self.image = image
        self.email = email
        self.real_name = rname
        self.name = name
        self.id = id

    def __str__(self):
        return "User(username={}, passwdHash={})".format(self.name, self.password)

    def add(self):
        '''
        Adds a user to the database,
        returns None if user already exists.
        '''
        cur.execute("SELECT * FROM users WHERE username = ?", (self.name,))
        for row in cur:
            raise UserExistsError("User {} already Exists!!!".format(self.name))
        cur.execute('INSERT INTO users (username, password, image, email, name) VALUES (?, ?, ?, ?, ?);', (self.name, self.password, self.image, self.email, self.real_name))
        conn.commit()
        self.id = cur.lastrowid

    def update(self):
        '''
        Does this update the user's password?
        '''
        cur.execute('''
                    UPDATE users
                    SET password = ?, image = ?, email = ?, name = ?
                    WHERE id = ?
                    ''', (self.password, self.image, self.email, self.real_name, self.id))
        conn.commit()

    @staticmethod
    def search(**kwargs):

        '''
        Runs search and returns "Invalid search" if username not found
        '''

        search_keys = []
        search_values = []

        search_options = ['username', 'password', 'id']
        for key, value in kwargs.items():
            if value is not None and key in search_options:
                search_keys.append(key + '=?')
                search_values.append(value)

        if search_keys == [] or search_values == []:
            return "Invalid search"

        cur.execute('''
            SELECT username, password, id
            FROM users
            WHERE {}
            '''.format(' AND '.join(search_keys)), tuple(search_values))

        rows = cur.fetchall()

        return [User(*row) for row in rows]

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
        cur.execute('''SELECT username, password, id, image, name, email
                        FROM users u
                        WHERE u.username = ?;''', (username,))
        row = cur.fetchone()
        if row is not None:
            name, password, id, im, rname, email = row
            return User(name, password, email, im, rname, id, False)
        return None

    @staticmethod
    def get_by_id(id):
        '''
        Get a User object with the details of the found user,
        returns None if no user found
        '''
        cur.execute('''SELECT username, password, id, image, name, email
                        FROM users u
                        WHERE u.id = ?;''', (id,))
        row = cur.fetchone()
        if row is not None:
            name, password, id, im, rname, email = row
            return User(name, password, email, im, rname, id, False)
        return None

    def get_lists(self):
        '''
        Get the bucket lists of a given user
        '''
        cur.execute('''
                    SELECT title, userid, id, created
                    FROM lists
                    WHERE userid = ?
                    ORDER BY created DESC;
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
                    ORDER BY created DESC;
                    ''')
        lists = []
        for row in cur:
            title, uid, id, created = row
            lists.append(List(title, uid, id, created))
        return lists

    def new_list(self, title):
        '''
        Add a new bucket list to the given user.
        '''
        l = List(title, self.id)
        l.add()
        return l

class Comment:
    def __init__(self, author, text, list_id, date=None, id=None):
        self.author = author
        self.list_id = list_id
        self.date = date
        self.id = id
        self.text = text

    def add(self):
        '''
        Add the comment to the database.
        '''
        self.date = datetime.datetime.now()
        cur.execute('''INSERT INTO comments (author, comment, created, listid) VALUES (?,?,?, ?)''', (self.author, self.text, self.date, self.list_id))
        conn.commit()
        self.id = cur.lastrowid

    def get_name(self):
        return User.get_by_id(self.author).name

    def fix_date(self, date):
        if date is not None:
            print(date)
            d = date.split()
            d2 = d[0].split('-')
            d2.reverse()
            d2 = '-'.join(d2)
            d1 = d[1].split(":")
            d3 = int(d1[0])
            t = 'PM' if d3 > 12 else 'AM'
            d3 -= 12 if d3 > 12 else 0
            return d2 + " " + str(d3)+":"+d1[1]+" "+t

    def update(self):
        '''
        Update any changes to the comment.
        '''
        cur.execute('''
                    UPDATE comments
                    SET text = ?, created = ?
                    WHERE id = ?
                    ''', (self.text, self.date, self.id))
        conn.commit()

    def delete(self):
        '''
        Delete a comment by its id
        '''
        
        cur.execute('''DELETE FROM comments
                    WHERE id = ?''',
                    (self.id,))
        conn.commit()

    @staticmethod
    def get(id):
        '''
        Get a comment by id.
        '''
        
        cur.execute('SELECT * FROM comments WHERE id = ?', (id,))
        row = cur.fetchone()
        if row is not None:
            return Comment(c[2], c[3], c[1], c[4], id)
        return None
        

    @staticmethod
    def get_comments_for_list(list_id):
        '''
        Get a list of comment objects by list_id.
        '''
        cur.execute('SELECT * FROM comments WHERE listid = ? ORDER BY created DESC', (list_id,))
        cs = [a for a in cur]
        comments = []
        for c in cs:
            comment = Comment(c[2], c[3], list_id, c[4], c[0])
            comments.append(comment)
        return comments

class Empty:
    def __init__(self):
        self.image = ''

if __name__ == "__main__":
    '''u2 = User('test1', 'testp')
    u2.add()
    u2.password = "windowsisBad123"
    u2.update()
    #l = List("test list for user test1", u2.id)
    l = u2.new_list("test list for user test1")
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
    u2.delete()'''

    # Testing search methods
    #u = User('test', 'test')
    #u.add()
    l = List('test', 'test')
    l.add()
    #i = Item(l.id, text='test')
    #i.add()
    print(User.search(username='test', password='test'))
    print(List.search(title='test', userid='test'))
    print(Item.search(listid=4, text='test'))
