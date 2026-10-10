# Student Opportunity Board

A web application built as part of my journey into **vibe coding** — using AI-assisted development to turn an idea into a working tool while learning software engineering concepts, database design, and testing practices along the way.

> [!NOTE]
> **Project Disclaimer:** This is an ongoing learning project developed in stages. It is **not in production yet** and is not intended for commercial use.

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

This project helps bridge the gap between learning programming concepts in isolation and applying them in a functional software application.

The following concepts have been explored during development:

1. **Separation of Concerns:** Keeping database operations in [`database.py`](database.py) rather than scattering SQL queries throughout the UI in [`app.py`](app.py).
2. **Safe SQL Operations:** Using parameterized SQL queries with `?` placeholders to handle user input safely and reduce SQL injection risks.
3. **State & Reactive UI in Streamlit:** Understanding form submissions, widget state, and UI reruns using `st.rerun()`.
4. **Defensive UI Design:** Adding confirmation safeguards for destructive actions, such as requiring explicit confirmation before permanently deleting an opportunity.
5. **Date and Boundary Logic:** Handling deadline calculations correctly, including deadlines due today, within seven days, and beyond that range.
6. **Automated Testing:** Using Streamlit's `AppTest` framework and Python tests to verify application behavior and database operations.
7. **AI-Assisted Development:** Using AI as a collaborative development aid while reviewing generated code, understanding implementation decisions, and validating changes rather than treating AI output as a black box.

## What I Learned — Phase 2.5  [8 - 9 October, 2026]

Phase 2.5 marks an important milestone in my journey with the Student Opportunity Board. What started as a simple student opportunity tracker has evolved into a more structured application with priority filtering, deadline awareness, dashboard metrics, safer data-management workflows, and automated testing.

Beyond implementing features, this phase helped me understand the practical decisions involved in building reliable and maintainable software.

## Latest Development Update — [October 10, 2026]

### Demo Data Preparation and Repository Synchronization

This phase focused on preparing a controlled demo-data seeding utility and synchronizing the project repository with the latest changes on GitHub.

**Completed**
- Added `seed_demo_data.py` to prepare a small set of clearly labeled fictional opportunity records for future testing.
- Reviewed the script's database path validation, transaction handling, duplicate checks, connection closure, and final read-only record-count verification.
- Reconciled the local branch with the latest remote changes using Git rebase.
- Successfully pushed the updated `main` branch to GitHub.
- Committed the utility as `b68b913` (`Add demo data seed script`).

**Safety and Scope**
- The seed script has **not been executed**.
- The existing `opportunities.db` and its verified backup have not been modified by this phase.
- No database seeding or production deployment was performed.

**Pending**
- Review the current project state before the next development phase.
- Decide on the next steps for safe demo-data testing and database restoration.
- Continue evaluating the path toward a student-focused, publicly accessible application.

> **Project status:** Ongoing learning project. The demo-data utility is prepared, but its execution and further database changes require a separate review and explicit approval.

### Key Learnings

1. **Thinking Beyond Expected Scenarios:** Building reliable features requires considering edge cases, invalid inputs, expired deadlines, and potentially destructive user actions.
2. **Protecting Data Integrity:** Database updates, record IDs, and test cleanup all play a role in ensuring that application data remains consistent and existing records are preserved.
3. **Verifying Behavior Through Tests:** Automated testing helps check whether application workflows, filters, deadline calculations, and dashboard metrics behave as intended.
4. **Improving Maintainability:** A clear separation between database operations and UI logic makes an application easier to understand, debug, and extend.
5. **Using AI Responsibly:** AI-assisted development is most useful when combined with code review, hands-on debugging, understanding implementation decisions, and verification of results.

## Next Steps

 The next stage will focus on improving usability, evaluating the application through realistic usage scenarios, and exploring the requirements for eventual deployment.
---
 This project continues to be a practical learning experience, helping me connect programming concepts with real-world software engineering practices.

> [!NOTE]
The milestone is not just about adding features, but also about developing a better understanding of how to build, test, and improve software responsibly.**
---

## Current Project Status

🚧 **In Active Development**

Core management, search, priority tracking, deadline calculations, and automated testing are complete. The project remains an educational project and is not deployed to production.

---

**Built while learning, experimenting, debugging, and turning ideas into working code.**
