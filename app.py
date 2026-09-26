"""
app.py - Student Opportunity Board

A Streamlit web application to help students track and manage opportunities
such as internships, hackathons, workshops, scholarships, and courses.
"""

import datetime
import streamlit as st
from database import (
    init_db,
    add_opportunity,
    get_all_opportunities,
    get_opportunity_by_id,
    update_opportunity,
    delete_opportunity
)

# Standard dropdown options
CATEGORIES = ["Internship", "Hackathon", "Workshop", "Scholarship", "Course"]
STATUSES = ["Saved", "Applied", "In Review", "Interviewing", "Accepted", "Rejected"]
PRIORITIES = ["Low", "Medium", "High"]


def parse_date(date_str):
    """Safely converts an ISO date string to a datetime.date object."""
    if not date_str:
        return None
    try:
        return datetime.date.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


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

# --- TAB 1: VIEW, EDIT & DELETE OPPORTUNITIES ---
with tab_view:
    st.subheader("Saved Opportunities")

    # Search and Filter Controls
    col_search, col_cat, col_status, col_priority = st.columns([2, 1, 1, 1])

    with col_search:
        search_query = st.text_input(
            "🔍 Search",
            placeholder="Search by title or organization..."
        )

    with col_cat:
        category_filter = st.selectbox(
            "Category",
            ["All"] + CATEGORIES
        )

    with col_status:
        status_filter = st.selectbox(
            "Status",
            ["All"] + STATUSES
        )

    with col_priority:
        priority_filter = st.selectbox(
            "Priority",
            ["All"] + PRIORITIES
        )

    # Fetch filtered opportunities from database
    opportunities = get_all_opportunities(
        search_query=search_query,
        category_filter=category_filter,
        status_filter=status_filter,
        priority_filter=priority_filter
    )

    if not opportunities:
        st.info("No opportunities found matching your criteria. Try adjusting your filters or add a new opportunity in the 'Add Opportunity' tab!")
    else:
        st.caption(f"Showing {len(opportunities)} opportunit{'ies' if len(opportunities) != 1 else 'y'}")

        table_data = [
            {
                "ID": row["id"],
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

        st.divider()

        # --- EDIT & DELETE SECTION ---
        st.subheader("⚙️ Manage an Opportunity")

        manage_options = {
            f"#{row['id']} - {row['title']} ({row['organization']})": row["id"]
            for row in opportunities
        }

        selected_label = st.selectbox(
            "Select an opportunity to edit or delete:",
            options=list(manage_options.keys()),
            key="manage_select"
        )
        selected_id = manage_options[selected_label]
        selected_opp = get_opportunity_by_id(selected_id)

        if selected_opp:
            col_edit, col_del = st.columns([3, 2])

            # EDIT FORM
            with col_edit:
                st.markdown("#### ✏️ Edit Details")
                with st.form(f"edit_form_{selected_id}"):
                    edit_title = st.text_input(
                        "Title *",
                        value=selected_opp["title"]
                    )
                    edit_organization = st.text_input(
                        "Organization *",
                        value=selected_opp["organization"]
                    )

                    cat_index = CATEGORIES.index(selected_opp["category"]) if selected_opp["category"] in CATEGORIES else 0
                    edit_category = st.selectbox(
                        "Category",
                        CATEGORIES,
                        index=cat_index
                    )

                    status_index = STATUSES.index(selected_opp["status"]) if selected_opp["status"] in STATUSES else 0
                    edit_status = st.selectbox(
                        "Status",
                        STATUSES,
                        index=status_index
                    )

                    priority_index = PRIORITIES.index(selected_opp["priority"]) if selected_opp["priority"] in PRIORITIES else 1
                    edit_priority = st.selectbox(
                        "Priority",
                        PRIORITIES,
                        index=priority_index
                    )

                    edit_deadline = st.date_input(
                        "Deadline",
                        value=parse_date(selected_opp["deadline"])
                    )
                    edit_link = st.text_input(
                        "Link",
                        value=selected_opp["link"] or ""
                    )
                    edit_notes = st.text_area(
                        "Notes",
                        value=selected_opp["notes"] or ""
                    )

                    save_changes = st.form_submit_button("Save Changes")

                    if save_changes:
                        if not edit_title.strip() or not edit_organization.strip():
                            st.error("Title and Organization are required.")
                        else:
                            deadline_str = edit_deadline.isoformat() if edit_deadline else None
                            clean_link = edit_link.strip() if edit_link.strip() else None
                            clean_notes = edit_notes.strip() if edit_notes.strip() else None

                            update_opportunity(
                                opportunity_id=selected_id,
                                title=edit_title.strip(),
                                organization=edit_organization.strip(),
                                category=edit_category,
                                status=edit_status,
                                priority=edit_priority,
                                deadline=deadline_str,
                                link=clean_link,
                                notes=clean_notes
                            )
                            st.success(f"Opportunity #{selected_id} updated successfully!")
                            st.rerun()

            # DELETE SECTION
            with col_del:
                st.markdown("#### 🗑️ Delete Opportunity")
                st.warning(
                    f"You are about to delete **#{selected_id}: {selected_opp['title']}** "
                    f"at **{selected_opp['organization']}**."
                )
                confirm_delete = st.checkbox(
                    "I confirm that I want to permanently delete this opportunity.",
                    key=f"confirm_delete_{selected_id}"
                )

                if st.button(
                    "Permanently Delete",
                    type="primary",
                    disabled=not confirm_delete,
                    key=f"delete_btn_{selected_id}"
                ):
                    delete_opportunity(selected_id)
                    st.success(f"Opportunity #{selected_id} has been deleted.")
                    st.rerun()

# --- TAB 2: ADD OPPORTUNITY ---
with tab_add:
    st.subheader("Add a New Opportunity")

    with st.form("add_opportunity_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Title *", placeholder="e.g., Software Engineering Intern")
            category = st.selectbox(
                "Category",
                CATEGORIES
            )
            priority = st.selectbox(
                "Priority",
                PRIORITIES,
                index=1
            )

        with col2:
            organization = st.text_input("Organization *", placeholder="e.g., Google, Major League Hacking")
            status = st.selectbox(
                "Status",
                STATUSES
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
