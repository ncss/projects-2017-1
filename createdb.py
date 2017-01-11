import sqlite3
import datetime

open('database.db', 'w').close()

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
    created TIMESTAMP NOT NULL,
  	PRIMARY KEY (id),
  	FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
);
'''
)

cur.execute('''
  CREATE TABLE items (
  	id INTEGER NOT NULL,
  	listid INTEGER NOT NULL,
  	text TEXT,
    image TEXT,
  	completed  INTEGER NOT NULL,
  	PRIMARY KEY (id),
  	FOREIGN KEY (listid) REFERENCES lists(id) ON DELETE CASCADE
);
'''
)

cur.execute('''
  CREATE TABLE comments (
    id INTEGER NOT NULL,
    listid INTEGER NOT NULL,
    author INTEGER NOT NULL,
    comment TEXT NOT NULL,
    created TIMESTAMP NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (listid) REFERENCES lists(id) ON DELETE CASCADE,
    FOREIGN KEY (author) REFERENCES users(id) ON DELETE CASCADE
);
'''
)

cur.execute("INSERT INTO users VALUES (0, 'Isaac', 'password');")
cur.execute("INSERT INTO users VALUES (1, 'mitchell', 'hello');")
cur.execute("INSERT INTO users VALUES (2, 'Name2', 'word2');")
cur.execute("INSERT INTO users VALUES (3, 'Name3', 'word3');")

now = datetime.datetime.now()
cur.execute("INSERT INTO lists VALUES (0, 0, 'listtittle', ?);", (now,))
cur.execute("INSERT INTO lists VALUES (1, 1, 'listtittle1', ?);", (now,))
cur.execute("INSERT INTO lists VALUES (2, 2, 'listtitle2', ?);", (now,))
cur.execute("INSERT INTO lists VALUES (3, 3, 'listtitle3', ?);", (now,))

cur.execute("INSERT INTO items VALUES (0, 0, 'Word1', NULL, 0 );")
cur.execute("INSERT INTO items VALUES (1, 1, 'Word2', NULL, 1 );")
cur.execute("INSERT INTO items VALUES (2, 2, 'Word3', NULL, 0 );")
cur.execute("INSERT INTO items VALUES (3, 3, 'Word4', NULL, 1 );")


cur.execute("INSERT INTO comments VALUES (0, 0, 0, 'Comment', ?)" (now,))
cur.execute("INSERT INTO comments VALUES (1, 1, 1, 'Comment1', ?)" (now,))
cur.execute("INSERT INTO comments VALUES (2, 2, 2, 'Comment2', ?)" (now,))
cur.execute("INSERT INTO comments VALUES (3, 3, 3, 'Comment3', ?)" (now,))

conn.commit()
