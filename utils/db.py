import sqlite3, secrets, hashlib
from flask import current_app

class Db():
    def _init_(self):
        # Initialize pos.db database or create if it does not exist.
        self.conn = sqlite3.connect('pos.db')
        self.cursor = self.conn.cursor()
        
        # Creates new tables in the pos.db database if they do not already exist.
        with current_app.open_resource("pos.sql") as f:
            self.cursor.executescript(f.read().decode("utf8"))
        self.conn.commit()
        
    def create_tables(self):
        # Creates new tables in the pos.db database if they do not already exist.
        with current_app.open_resource("pos.sql") as f:
            self.cursor.executescript(f.read().decode("utf8"))
        self.conn.commit()
        self.conn.close()