import sqlite3

conn = sqlite3.connect('data/warehouse.db')

with open('db/schema.sql', encoding='utf-8') as f:
    conn.executescript(f.read())

with open('db/seed_dummy.sql', encoding='utf-8') as f:
    conn.executescript(f.read())

conn.commit()
conn.close()