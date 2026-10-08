# Student Opportunity Board

A web application built as part of my journey into **vibe coding** — using AI-assisted development to turn an idea into a working tool while learning software engineering concepts, database design, and testing practices along the way.

> [!NOTE]
> **Project Disclaimer:** This is an ongoing learning project developed in stages. It is **not in production yet** and is not intended as a commercial application.

---

## About the Project

Students often juggle opportunities across scattered bookmarks, emails, and notes: internships, hackathons, workshops, scholarships, and technical courses.

The **Student Opportunity Board** provides a single place to track these opportunities, monitor application statuses, prioritize focus, and stay aware of upcoming deadlines.

Rather than just generating code blindly, this project is built incrementally to explore how an interactive data-backed Python application comes together from scratch.

---

## Current Features

### 1. Opportunity Management (CRUD)
* **Add Opportunity:** Save new opportunities with Title, Organization, Category, Status, Priority, Deadline date, Application Link, and Notes.
* **Edit Opportunity:** Edit any existing opportunity with an in-place pre-populated form. Updates the record directly in SQLite without creating duplicates or changing IDs.
* **Delete with Confirmation Protection:** To prevent accidental deletion, the delete section is situated below the edit form and requires checking a safety confirmation checkbox (`I confirm that I want to permanently delete this opportunity.`) before the delete action is enabled.

### 2. Search & Filtering
* **Keyword Search:** Search opportunities by title or organization.
* **Category Filter:** Filter by specific opportunity type (`Internship`, `Hackathon`, `Workshop`, `Scholarship`, `Course`, or `All`).
* **Status Filter:** Track progress through the application lifecycle (`Saved`, `Applied`, `In Review`, `Interviewing`, `Accepted`, `Rejected`, or `All`).
* **Priority Management & Filtering:** Prioritize opportunities (`Low`, `Medium`, `High`) and filter views accordingly to focus on high-impact applications.

### 3. Deadline Status Awareness
The board dynamically calculates the urgency of each deadline relative to the current date:
* **No Deadline:** When no date is specified.
* **Expired:** Deadlines that have already passed.
* **Due Today:** Deadlines due on the current day.
* **Due Soon:** Deadlines falling within 1 to 7 days.
* **Upcoming:** Deadlines more than 7 days out.

### 4. Summary Dashboard Metrics
At the top of the board, summary metrics provide a high-level overview of your pipeline:
* **Total Opportunities:** Total number of recorded opportunities.
* **Active Applications:** Count of applications currently in progress (`Applied`, `In Review`, `Interviewing`).
* **High Priority:** Count of entries marked with `High` priority.
* **Due Soon / Today:** Count of actionable opportunities due today or within the next 7 days.

---

## Tech Stack

* **Language:** Python 3.11+
* **Frontend / UI:** [Streamlit](https://streamlit.io/) (`1.63.0`)
* **Database Layer:** SQLite (`sqlite3` standard library with `sqlite3.Row` row factory)
* **Testing:** Streamlit `AppTest` framework & automated Python unit tests
* **Version Control:** Git & GitHub
* **Methodology:** AI-assisted development (Vibe Coding) with hands-on debugging and architectural review

---

## Project Structure

```text
my-first-vibe-project/
│
├── app.py              # Streamlit application UI, metrics, views, forms, and workflows
├── database.py         # SQLite data layer (table schema, CRUD functions, parameterized queries)
├── opportunities.db    # SQLite database file (local storage)
├── requirements.txt    # Project dependencies
├── tests/
│   └── test_app.py     # Automated test suite (UI AppTest, DB filters, deadline logic, cleanup)
├── .gitignore          # Git ignore rules for environments and temporary files
└── README.md           # Project documentation and learning log
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SyedaNazish-debug/my-first-vibe-project.git
cd my-first-vibe-project
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

On macOS / Linux:
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will open automatically in your browser (default: `http://localhost:8501`).

---

## Automated Testing

The project includes an automated test suite in [`tests/test_app.py`](tests/test_app.py) verifying both the interface and data layer:

* **Streamlit UI Tests (`AppTest`):** Verifies app startup, form rendering, required field validation, edit updates, and delete confirmation protection.
* **Database Tests:** Verifies parameterized queries for title/org searches, category filters, status filters, priority filters, and multi-filter combinations.
* **Deadline & Metrics Logic Tests:** Tests all deadline status boundaries (`No Deadline`, `Expired`, `Due Today`, `Due Soon`, `Upcoming`) and summary metric calculations.
* **Data Integrity & Cleanup:** Ensures test-generated records are removed and existing database state is preserved after test execution.

To run the tests:

```bash
python -m tests.test_app
```

---

## Development Progress & Phases

* [x] **Phase 1 — Project Foundation:** Initial SQLite database, Streamlit application, basic opportunity management, and project setup.
* [x] **Phase 2.5.1 — Priority Filtering:** Added priority levels (`Low`, `Medium`, `High`) and priority-based filtering.
* [x] **Phase 2.5.2 — Deadline Awareness:** Added deadline status calculations for `No Deadline`, `Expired`, `Due Today`, `Due Soon`, and `Upcoming`.
* [x] **Phase 2.5.3 — Dashboard Metrics:** Added summary metrics for total opportunities, active applications, high-priority opportunities, and due soon/today deadlines.
* [x] **Phase 2.5.4 — Edit/Delete Workflow:** Improved editing and deletion workflows, including validation, delete confirmation protection, and a clearer Edit → Delete layout.
* [x] **Automated Testing:** Expanded `tests/test_app.py` to verify UI workflows, filtering, deadline logic, dashboard metrics, validation, and database edge cases.
* [ ] **Next:** Further UX improvements, usability testing, and exploration of deployment/production readiness.

---

## What I'm Learning From This Project

This project is helping bridge the gap between learning programming concepts in isolation and assembling a functional software application:

1. **Separation of Concerns:** Keeping database SQL operations isolated in [`database.py`](database.py) rather than scattering queries across the UI in [`app.py`](app.py).
2. **Safe SQL Operations:** Writing parameterized SQL queries (`?` placeholders) to prevent syntax errors and prevent injection risks.
3. **State & Reactive UI in Streamlit:** Managing form submissions, dropdown bindings, and UI re-runs with `st.rerun()`.
4. **Defensive UI Design:** Protecting critical destructive actions with confirmation safeguards (disabling delete until an explicit checkbox is marked).
5. **Boundary Condition Testing:** Understanding how date difference logic handles edges (e.g., exactly today vs 7 days vs 8+ days).
6. **Automated Testing for Web Apps:** Using Streamlit's `AppTest` to simulate user actions and form interactions programmatically.
7. **Pairing with AI ("Vibe Coding" responsibly):** Learning that AI is best used as a collaborative partner — reviewing code line-by-line, verifying test outputs, and understanding the architecture rather than treating AI outputs as a black box.

---

## Current Project Status

🚧 **In Active Development**

Core management, search, priority tracking, deadline calculations, and automated testing are complete. The project remains an educational project and is not deployed to production.

---

**Built while learning, experimenting, debugging, and turning ideas into working code.**
