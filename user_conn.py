import sqlite3
from user_info import UserInfo

class UserConn:

    def __init__(self):
        self._conn = sqlite3.connect("user.db")
        self._c = self._conn.cursor()

    def insert_user(self, username, password):
        with self._conn:
            self._c.execute("INSERT INTO userdata (username, password) VALUES (:username, :password)",
                            {"username": username, "password": password})

    def get_user(self, username):
        with self._conn:
            self._c.execute("SELECT * FROM userdata WHERE username = :username", {"username": username})
            return self._c.fetchone()

    def update_username(self, old_username, new_username):
        with self._conn:
            self._c.execute("""UPDATE userdata SET username = :new_username WHERE username = :old_username""",
                            {"new_username": new_username, "old_username": old_username})

    def update_password(self, username, new_password):
        with self._conn:
            self._c.execute("""UPDATE userdata SET password = :new_password WHERE username = :username""",
                            {"new_password": new_password, "username": username})

    def remove_user(self, username):
        with self._conn:
            self._c.execute("DELETE from userdata WHERE username = :username", {"username": username})

