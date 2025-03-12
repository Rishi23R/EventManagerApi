from database import engine, Base
import models
import sqlite3


Base.metadata.create_all(bind=engine)
print("Tables should now be created.")

conn = sqlite3.connect("event_management.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
conn.close()

print("Existing Tables in SQLite:", tables)  # This should show tables
