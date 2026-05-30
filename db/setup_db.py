import sqlite3
import os

os.makedirs("db", exist_ok=True)

conn = sqlite3.connect("db/company.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
   id INTEGER PRIMARY KEY,
   name TEXT,
   department TEXT,
   salary INTEGER
)
""")

# cursor.execute("DELETE FROM employees")

employees = [
   ("John", "Engineering", 75000),
   ("Sarah", "HR", 65000),
   ("Mike", "Finance", 70000),
   ("Priya", "Marketing", 68000)
]

cursor.executemany(
   """
   INSERT INTO employees(name,department,salary)
   VALUES(?,?,?)
   """,
   employees
)

conn.commit()
conn.close()

print("Database created.")

