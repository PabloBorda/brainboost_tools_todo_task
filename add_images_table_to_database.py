#!/usr/bin/env python3
import sqlite3
from datetime import datetime

# Update the path to your database as needed.
DB_PATH = "/home/golden/todos.db"

def table_exists(conn, table_name):
    """
    Check if a table with the given name exists in the database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

def create_documents_table(conn):
    """
    Creates the 'documents' table if it does not already exist.
    The table includes:
      - id: Auto-incrementing primary key.
      - name: The name of the document.
      - binary_content: BLOB field to store the document's binary data.
      - mime_type: TEXT field for the MIME type (e.g., "png", "jpg", "pdf").
      - text_caption: TEXT field for any OCR text extracted from the document.
    """
    cursor = conn.cursor()
    if not table_exists(conn, "documents"):
        print("Creating 'documents' table...")
        cursor.execute("""
            CREATE TABLE documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                binary_content BLOB,
                mime_type TEXT,
                text_caption TEXT
            )
        """)
        conn.commit()
        print("Table 'documents' created.")
    else:
        print("Table 'documents' already exists.")

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        create_documents_table(conn)
    except Exception as e:
        print("Error during table creation:", e)
    finally:
        conn.close()
        print("Database update complete.")

if __name__ == "__main__":
    main()
