"""
database.py - Database Layer for Student Opportunity Board

Handles database connections, table initialization, and CRUD operations
using Python's built-in sqlite3 module.
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


def add_opportunity(title, organization, category, status, priority, deadline=None, link=None, notes=None):
    """
    Inserts a new opportunity into the opportunities table.
    Returns the id of the newly created record.
    """
    sql = """
    INSERT INTO opportunities (title, organization, category, status, priority, deadline, link, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(sql, (title, organization, category, status, priority, deadline, link, notes))
            return cursor.lastrowid
    finally:
        conn.close()


def get_all_opportunities(search_query=None, category_filter=None, status_filter=None, priority_filter=None):
    """
    Retrieves opportunities from the database with optional search and filtering:
    - search_query: matches keyword against title or organization
    - category_filter: filters by category (ignores if None or 'All')
    - status_filter: filters by status (ignores if None or 'All')
    - priority_filter: filters by priority (ignores if None or 'All')
    Returns a list of sqlite3.Row objects ordered by newest first.
    """
    sql = "SELECT * FROM opportunities WHERE 1=1"
    params = []

    if search_query and search_query.strip():
        sql += " AND (title LIKE ? OR organization LIKE ?)"
        wildcard = f"%{search_query.strip()}%"
        params.extend([wildcard, wildcard])

    if category_filter and category_filter != "All":
        sql += " AND category = ?"
        params.append(category_filter)

    if status_filter and status_filter != "All":
        sql += " AND status = ?"
        params.append(status_filter)

    if priority_filter and priority_filter != "All":
        sql += " AND priority = ?"
        params.append(priority_filter)

    sql += " ORDER BY id DESC"

    conn = get_connection()
    try:
        cursor = conn.execute(sql, params)
        return cursor.fetchall()
    finally:
        conn.close()


def get_opportunity_by_id(opportunity_id):
    """
    Fetches a single opportunity by its ID.
    Returns an sqlite3.Row object, or None if not found.
    """
    sql = "SELECT * FROM opportunities WHERE id = ?"
    conn = get_connection()
    try:
        cursor = conn.execute(sql, (opportunity_id,))
        return cursor.fetchone()
    finally:
        conn.close()


def update_opportunity(opportunity_id, title, organization, category, status, priority, deadline=None, link=None, notes=None):
    """
    Updates an existing opportunity by its ID.
    Returns True if a row was updated, False otherwise.
    """
    sql = """
    UPDATE opportunities
    SET title = ?, organization = ?, category = ?, status = ?, priority = ?, deadline = ?, link = ?, notes = ?
    WHERE id = ?
    """
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(
                sql,
                (title, organization, category, status, priority, deadline, link, notes, opportunity_id)
            )
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_opportunity(opportunity_id):
    """
    Deletes an opportunity by its ID.
    Returns True if a row was deleted, False otherwise.
    """
    sql = "DELETE FROM opportunities WHERE id = ?"
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(sql, (opportunity_id,))
            return cursor.rowcount > 0
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
