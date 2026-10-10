"""
seed_demo_data.py — Phase 0 Demo Seed Script
Student Opportunity Board

PURPOSE
-------
Inserts five clearly-labeled, fictional demo records into a specified
SQLite database that already has the 'opportunities' schema initialized.

PHASE 0 RESTRICTION
-------------------
THIS SCRIPT MUST NOT BE EXECUTED DURING PHASE 0.

Phase 0 covers only the creation and review of this file.
Running the script against any database is a Phase 1 action and
requires separate, explicit approval.

Do NOT run this script against:
  - opportunities.db                              (live project database)
  - opportunities-backup-20261010-164531.db       (verified backup)

This script cannot independently identify whether the path supplied via
--db-path points to the live database, the verified backup, or any other
file. The developer is solely responsible for verifying the target path
before running.

Any future testing of this script must use a separate, disposable SQLite
database that is not the original opportunities.db and not the verified
backup. The test database should be created solely for that purpose and
discarded afterwards.

USAGE (Phase 1 and later only, after explicit approval)
-------------------------------------------------------
    python seed_demo_data.py --db-path /path/to/target.db

The --db-path argument is REQUIRED. There is no default path and no
environment-variable fallback. The script will refuse to run without it
and will refuse to run if the specified file does not exist.

IDEMPOTENCY
-----------
Before each insert the script performs a SELECT to check whether a row
with the same (title, organization) pair already exists. If it does,
the insert is skipped. This prevents ordinary repeated runs from creating
duplicates.

IMPORTANT LIMITATION: this is an application-level check only. There is
NO unique constraint on (title, organization) in the database schema.
If two concurrent processes ran this script simultaneously, or if a row
with a matching (title, organization) was inserted by another path between
the check and the insert, a duplicate could still be created. For this
single-user, local-development context that risk is acceptable, but it
must not be described or understood as a database-enforced guarantee.

TRANSACTION HANDLING
--------------------
All inserts are performed inside a single explicit transaction:

  - conn.commit() is called only when all inserts have completed without
    error. The entire batch is committed together.
  - conn.rollback() is called if any exception occurs. The entire batch
    is rolled back together; no partial state is written.
  - conn.close() is called in a finally block and runs unconditionally,
    whether the transaction committed, rolled back, or raised an unhandled
    exception.

PHASE 2 NOTE
------------
This script targets the existing SQLite schema. In Phase 2 the schema
migrates to PostgreSQL and gains user_id and is_demo columns. At that
point this script will be superseded by a PostgreSQL seed migration and
should not be used.
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Demo records
# All organizations are fictional. No deadlines. No links.
# The "(Demo)" suffix makes these records identifiable in the UI list view
# before the Phase 2 is_demo column exists.
# ---------------------------------------------------------------------------
DEMO_RECORDS = [
    {
        "title":        "Software Engineering Internship (Demo)",
        "organization": "Example Corp",
        "category":     "Internship",
        "status":       "Applied",
        "priority":     "High",
        "deadline":     None,
        "link":         None,
        "notes":        "Demo record — illustrates an active internship application.",
    },
    {
        "title":        "AI Builders Hackathon (Demo)",
        "organization": "Demo Hacks Foundation",
        "category":     "Hackathon",
        "status":       "Saved",
        "priority":     "High",
        "deadline":     None,
        "link":         None,
        "notes":        "Demo record — illustrates a saved hackathon entry.",
    },
    {
        "title":        "Open Source Workshop (Demo)",
        "organization": "Community Learning Lab",
        "category":     "Workshop",
        "status":       "Saved",
        "priority":     "Medium",
        "deadline":     None,
        "link":         None,
        "notes":        "Demo record — illustrates a workshop opportunity.",
    },
    {
        "title":        "Merit Scholarship (Demo)",
        "organization": "Sample Scholarship Fund",
        "category":     "Scholarship",
        "status":       "In Review",
        "priority":     "Medium",
        "deadline":     None,
        "link":         None,
        "notes":        "Demo record — illustrates a scholarship under review.",
    },
    {
        "title":        "Python for Data Science (Demo)",
        "organization": "Online Learning Platform",
        "category":     "Course",
        "status":       "Saved",
        "priority":     "Low",
        "deadline":     None,
        "link":         None,
        "notes":        "Demo record — illustrates a tracked course.",
    },
]


# ---------------------------------------------------------------------------
# SQL statements
# ---------------------------------------------------------------------------
CHECK_SQL = """
    SELECT COUNT(*) FROM opportunities
    WHERE title = ? AND organization = ?
"""

INSERT_SQL = """
    INSERT INTO opportunities
        (title, organization, category, status, priority, deadline, link, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

COUNT_SQL = "SELECT COUNT(*) FROM opportunities"


# ---------------------------------------------------------------------------
# Core seeding logic
# ---------------------------------------------------------------------------
def seed(db_path: str) -> None:
    """
    Opens the database at db_path, checks for existing demo records, and
    inserts any that are missing — all within a single explicit transaction.

    Transaction contract:
      - All inserts succeed  → conn.commit() is called; batch is written.
      - Any insert fails     → conn.rollback() is called; nothing is written.
      - Either way           → conn.close() is called in the finally block.

    The final row count is read back via a separate read-only connection
    whose URI is constructed using Path.resolve().as_uri() so that any
    URI-special characters in the path (e.g. '?' or '#') are correctly
    percent-encoded and do not corrupt the mode=ro query parameter.
    """
    print(f"\nTarget database : {db_path}")
    print(f"Demo records    : {len(DEMO_RECORDS)}")
    print("-" * 60)

    conn = sqlite3.connect(db_path)

    try:
        inserted = 0
        skipped  = 0

        try:
            for rec in DEMO_RECORDS:
                # Application-level duplicate check.
                # Not a database-enforced constraint — see module docstring.
                existing_count = conn.execute(
                    CHECK_SQL, (rec["title"], rec["organization"])
                ).fetchone()[0]

                if existing_count > 0:
                    print(f"  [SKIP]   '{rec['title']}' — already present")
                    skipped += 1
                else:
                    conn.execute(INSERT_SQL, (
                        rec["title"],
                        rec["organization"],
                        rec["category"],
                        rec["status"],
                        rec["priority"],
                        rec["deadline"],
                        rec["link"],
                        rec["notes"],
                    ))
                    print(f"  [INSERT] '{rec['title']}'")
                    inserted += 1

            # All inserts completed without error — commit the entire batch.
            conn.commit()

        except Exception:
            # Something went wrong — roll back every insert in this batch.
            conn.rollback()
            raise  # re-raise so the caller sees the original error

    finally:
        # Always runs: closes the connection whether the transaction
        # committed, rolled back, or raised an unhandled exception.
        conn.close()

    # Read the final row count using a separate read-only connection.
    #
    # Path.resolve() converts db_path to an absolute path (required by
    # as_uri()), then as_uri() percent-encodes any URI-special characters
    # in the path (e.g. '?' -> '%3F', '#' -> '%23', space -> '%20').
    # '?mode=ro' is appended after encoding, so it is always interpreted
    # as the query-string delimiter and never as part of the file path.
    db_uri = Path(db_path).resolve().as_uri() + "?mode=ro"
    conn_ro = sqlite3.connect(db_uri, uri=True)
    try:
        total = conn_ro.execute(COUNT_SQL).fetchone()[0]
    finally:
        conn_ro.close()

    print("-" * 60)
    print(f"Inserted : {inserted}")
    print(f"Skipped  : {skipped}")
    print(f"Total rows in the selected database (opportunities table): {total}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    print("=" * 60)
    print("seed_demo_data.py — Student Opportunity Board")
    print("=" * 60)
    print()
    print("WARNING: Do NOT run this script against:")
    print("  - opportunities.db                        (live project database)")
    print("  - opportunities-backup-20261010-164531.db (verified backup)")
    print()
    print("This script cannot verify that the supplied --db-path is safe.")
    print("You are responsible for confirming the target path before running.")
    print()
    print("Any test of this script must use a separate, disposable database,")
    print("not the original database or the verified backup.")
    print()

    parser = argparse.ArgumentParser(
        description=(
            "Insert fictional demo records into a specified SQLite database. "
            "--db-path is required; there is no default and no fallback."
        )
    )
    parser.add_argument(
        "--db-path",
        required=True,      # argparse errors immediately if this flag is omitted
        metavar="PATH",
        help="Absolute or relative path to the target SQLite database file.",
    )
    args = parser.parse_args()

    # Refuse to proceed if the specified file does not exist.
    # The script never creates a new database file.
    if not os.path.isfile(args.db_path):
        print(
            f"ERROR: Database file not found: {args.db_path}",
            file=sys.stderr,
        )
        print(
            "Ensure the schema has been initialized with `python database.py` "
            "before running this script.",
            file=sys.stderr,
        )
        sys.exit(1)

    seed(args.db_path)


if __name__ == "__main__":
    main()
