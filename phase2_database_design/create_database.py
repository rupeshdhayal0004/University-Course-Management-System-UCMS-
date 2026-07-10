import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "database", "university.db")

schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

conn = sqlite3.connect(db_path)

with open(schema_path, "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database created successfully")
