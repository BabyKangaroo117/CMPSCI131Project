import sqlite3
import user_conn
conn = sqlite3.connect("user.db")

c = conn.cursor()

# create tables
c.execute("""CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER PRIMARY KEY,
            username VARCHAR (30) NOT NULL,
            password VARCHAR (30) NOT NULL

        )""")

c.execute("""CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name VARCHAR (20) NOT NULL,
            address1 VARCHAR (80),
            address2 VARCHAR (80),
            address3 VARCHAR (80),
            address4 VARCHAR (80),
            FOREIGN KEY (user_id) REFERENCES userdata(id)
        )""")

conn.commit()
conn.close()
