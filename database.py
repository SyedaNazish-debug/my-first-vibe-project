"""
database.py - Database Layer for Student Opportunity Board

Handles database connections and table initialization using Python's
built-in sqlite3 module.
"""

import sqlite3

DB_NAME = "opportunities.db"


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    Configures sqlite3.Row as the row factory so query results can be
    accessed by column name (like dictionaries) as well as index.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the database by creating the 'opportunities' table
    if it does not already exist. Safely closes the connection when done.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        organization TEXT NOT NULL,
        category TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        deadline TEXT,
        link TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = get_connection()
    try:
        with conn:
            conn.execute(create_table_sql)
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
