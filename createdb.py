import sqlite3
conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
  CREATE TABLE users (
  	id INTEGER NOT NULL,
  	username TEXT NOT NULL,
  	password TEXT NOT NULL,
  	PRIMARY KEY (id)
);
'''
)

cur.execute('''
  CREATE TABLE lists (
  	id INTEGER NOT NULL,
  	userid INTEGER NOT NULL,
  	title TEXT NOT NULL,
  	PRIMARY KEY (id),
  	FOREIGN KEY (userid) REFERENCES users(id)
);
'''
)

cur.execute('''
  CREATE TABLE items (
  	id INTEGER NOT NULL,
  	listid INTEGER NOT NULL,
  	text TEXT NOT NULL,
    image TEXT NOT NULL,
  	completed  INTEGER NOT NULL,
  	PRIMARY KEY (id),
  	FOREIGN KEY (listid) REFERENCES lists(id)
);
'''
)

cur.execute("INSERT INTO users VALUES (0, 'Isaac', 'password');")
cur.execute("INSERT INTO users VALUES ( 1, 'Name1', 'word1');")
cur.execute("INSERT INTO users VALUES ( 2, 'Name2', 'word2');")
cur.execute("INSERT INTO users VALUES ( 3, 'Name3', 'word3');")

cur.execute("INSERT INTO lists VALUES (0, 0,'listtittle');")
cur.execute("INSERT INTO lists VALUES (1, 1,'listtittle1');")
cur.execute("INSERT INTO lists VALUES (2, 2,'listtitle2');")
cur.execute("INSERT INTO lists VALUES (3, 3, 'listtitle3');")

cur.execute("INSERT INTO items VALUES (0, 0,'Word1', 0 );")
cur.execute("INSERT INTO items VALUES (1, 1,'Word2', 1 );")
cur.execute("INSERT INTO items VALUES (2, 2,'Word3', 0 );")
cur.execute("INSERT INTO items VALUES (3, 3, 'Word4', 1 );")
