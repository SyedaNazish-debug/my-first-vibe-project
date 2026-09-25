"""
app.py - Student Opportunity Board

A Streamlit web application to help students track and manage opportunities
such as internships, hackathons, workshops, scholarships, and courses.
"""

import streamlit as st
from database import init_db, add_opportunity, get_all_opportunities

# Page Configuration
st.set_page_config(
    page_title="Student Opportunity Board",
    page_icon="🎓",
    layout="wide"
)

# Initialize SQLite database and tables
init_db()

# Application Header
st.title("🎓 Student Opportunity Board")
st.write(
    "Welcome! Keep track of your internships, hackathons, workshops, scholarships, "
    "and courses in one centralized place."
)

# Navigation Structure
tab_view, tab_add = st.tabs(["📋 View Opportunities", "➕ Add Opportunity"])

with tab_view:
    st.subheader("Saved Opportunities")

    # Search and Filter Controls
    col_search, col_cat, col_status = st.columns([2, 1, 1])

    with col_search:
        search_query = st.text_input(
            "🔍 Search",
            placeholder="Search by title or organization..."
        )

    with col_cat:
        category_filter = st.selectbox(
            "Category",
            ["All", "Internship", "Hackathon", "Workshop", "Scholarship", "Course"]
        )

    with col_status:
        status_filter = st.selectbox(
            "Status",
            ["All", "Saved", "Applied", "In Review", "Interviewing", "Accepted", "Rejected"]
        )

    # Fetch filtered opportunities from database
    opportunities = get_all_opportunities(
        search_query=search_query,
        category_filter=category_filter,
        status_filter=status_filter
    )

    if not opportunities:
        st.info("No opportunities found matching your criteria. Try adjusting your filters or add a new opportunity in the 'Add Opportunity' tab!")
    else:
        st.caption(f"Showing {len(opportunities)} opportunit{'ies' if len(opportunities) != 1 else 'y'}")

        table_data = [
            {
                "Title": row["title"],
                "Organization": row["organization"],
                "Category": row["category"],
                "Status": row["status"],
                "Priority": row["priority"],
                "Deadline": row["deadline"] if row["deadline"] else "-",
                "Link": row["link"] if row["link"] else None,
                "Notes": row["notes"] if row["notes"] else "-",
            }
            for row in opportunities
        ]

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Link": st.column_config.LinkColumn("Link", display_text="Open Link")
            }
        )

with tab_add:
    st.subheader("Add a New Opportunity")

    with st.form("add_opportunity_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Title *", placeholder="e.g., Software Engineering Intern")
            category = st.selectbox(
                "Category",
                ["Internship", "Hackathon", "Workshop", "Scholarship", "Course"]
            )
            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High"],
                index=1
            )

        with col2:
            organization = st.text_input("Organization *", placeholder="e.g., Google, Major League Hacking")
            status = st.selectbox(
                "Status",
                ["Saved", "Applied", "In Review", "Interviewing", "Accepted", "Rejected"]
            )
            deadline = st.date_input("Deadline", value=None)

        link = st.text_input("Link", placeholder="https://example.com/apply")
        notes = st.text_area("Notes", placeholder="Add notes, requirements, or contacts...")

        submitted = st.form_submit_button("Save Opportunity")

        if submitted:
            if not title.strip() or not organization.strip():
                st.error("Please fill in both required fields: Title and Organization.")
            else:
                deadline_str = deadline.isoformat() if deadline else None
                clean_link = link.strip() if link.strip() else None
                clean_notes = notes.strip() if notes.strip() else None

                add_opportunity(
                    title=title.strip(),
                    organization=organization.strip(),
                    category=category,
                    status=status,
                    priority=priority,
                    deadline=deadline_str,
                    link=clean_link,
                    notes=clean_notes
                )
                st.success(f"Opportunity '{title.strip()}' saved successfully!")
