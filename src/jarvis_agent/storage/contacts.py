import sqlite3
from pathlib import Path

class Contacts:
    def __init__(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS contacts (user_id INTEGER, name TEXT, phone TEXT, PRIMARY KEY(user_id,name,phone))")
        self.db.commit()

    def add(self, user_id: int, name: str, phone: str):
        self.db.execute("INSERT OR IGNORE INTO contacts VALUES (?,?,?)", (user_id, name, phone))
        self.db.commit()

    def find(self, user_id: int, name: str):
        cur = self.db.execute("SELECT name,phone FROM contacts WHERE user_id=? AND lower(name)=lower(?)", (user_id, name))
        return cur.fetchone()
