import sqlite3
from user_info import UserInfo


class AddressConn:

    def __init__(self):
        self._conn = sqlite3.connect("user.db")
        self._c = self._conn.cursor()

    def insert_address(self, user_id, name, address1, address2, address3, address4):
        with self._conn:
            self._c.execute("INSERT INTO addresses (user_id, name, address1, address2, address3, address4) "
                            "VALUES (:user_id, :name, :address1, :address2, :address3, :address4)",
                            {"user_id": user_id, "name": name, "address1": address1, "address2": address2,
                             "address3": address3, "address4": address4})

    def get_addresses(self, user_id):
        with self._conn:
            self._c.execute("SELECT * FROM addresses WHERE user_id = :user_id", {"user_id": user_id})
            return self._c.fetchall()

    def update_addresses(self, address_id, user_id, name, address1, address2, address3, address4):
        with self._conn:
            self._c.execute("""UPDATE addresses SET address1 = :address1, address2 = :address2, address3 = :address3, 
                            address4 = :address4 
                            WHERE id = :address_id""",
                            {"user_id": user_id, "name": name, "address1": address1, "address2": address2,
                             "address3": address3, "address4": address4, "id": address_id})

    def remove_addresses(self, address_id):
        with self._conn:
            self._c.execute("DELETE from addresses WHERE id = :address_id", {"address_id": address_id})

