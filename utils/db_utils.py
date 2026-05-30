# See chat for full code
import sqlite3


def get_database_schema(db_path):

   conn = sqlite3.connect(db_path)

   cursor = conn.cursor()

   cursor.execute("""
       SELECT sql
       FROM sqlite_master
       WHERE type='table'
       AND name NOT LIKE 'sqlite_%'
   """)

   schemas = cursor.fetchall()

   conn.close()

   return "\n\n".join(
       [schema[0] for schema in schemas]
   )
