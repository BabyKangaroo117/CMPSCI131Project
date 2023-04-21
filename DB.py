import sqlite3
from user_conn import UserConn
from user_info import UserInfo
conn = sqlite3.connect("user.db")

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER PRIMARY KEY,
            username VARCHAR (30) NOT NULL,
            password VARCHAR (30) NOT NULL

        )""")

c.execute("""CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name VARCHAR (10) NOT NULL,
            address1 VARCHAR (40),
            address2 VARCHAR (40),
            address3 VARCHAR (40),
            address4 VARCHAR (40),
            FOREIGN KEY (user_id) REFERENCES userdata(id)
        )""")

c.execute("INSERT INTO addresses (user_id, name, address1, address2, address3, address4) VALUES (?, ?, ?, ?, ?, ?)", ("1", "Friends", "506 Starflower St, Warrington, Pa 18976", "550 valley view rd, langhorne, pa 19047", "563 Woodview ln, Harleysville, Pa 19438", ""))
#c.execute("DELETE FROM userdata")
c.execute("SELECT * FROM addresses")
print(c.fetchall())


conn.commit()
conn.close()

# user_connection = UserConn()
# user = UserInfo("smith", "1234")
# user_connection.insert_user("smith", "1234")
# user_data = user_connection.get_user("smith")
# user_connection.update_username("smith", "joe")
# user_data = user_connection.get_user("joe")


