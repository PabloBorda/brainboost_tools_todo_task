#!/usr/bin/env python3
import sqlite3
from datetime import datetime

DB_PATH = "/home/golden/todos.db"  # update with your actual database path

def column_exists(conn, table, column):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]  # row[1] is the column name
    return column in columns

def alter_tasks_table(conn):
    cursor = conn.cursor()
    # Add the "timestamp" column without a default value.
    if not column_exists(conn, "tasks", "timestamp"):
        print("Adding 'timestamp' column to tasks table...")
        cursor.execute("ALTER TABLE tasks ADD COLUMN timestamp TEXT")
        conn.commit()
        print("Column added.")
    else:
        print("Column 'timestamp' already exists.")

def update_existing_timestamps(conn):
    cursor = conn.cursor()
    # Set a mock timestamp for rows where timestamp is NULL or empty.
    current_ts = datetime.now().isoformat()
    print("Updating existing tasks with a mock timestamp if needed...")
    cursor.execute("UPDATE tasks SET timestamp = ? WHERE timestamp IS NULL OR timestamp = ''", (current_ts,))
    conn.commit()
    print(f"Updated {cursor.rowcount} records.")

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        alter_tasks_table(conn)
        update_existing_timestamps(conn)
    except Exception as e:
        print("Error during update:", e)
    finally:
        conn.close()
        print("Database update complete.")

if __name__ == "__main__":
    main()
