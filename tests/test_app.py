"""
tests/test_app.py - Test Suite for Student Opportunity Board

Contains:
1. Streamlit AppTest / UI tests (startup, forms, validation, edit, delete with confirmation)
2. Database-level tests (search, category, status, and combined filtering queries)
3. Data-integrity and cleanup tests (database returned to its exact original state)
"""

import os
import sys
import datetime

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from streamlit.testing.v1 import AppTest
import database

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))


def run_tests():
    print("================================================================")
    print("STARTING TEST SUITE: STUDENT OPPORTUNITY BOARD")
    print("================================================================")

    # Record initial database state to guarantee complete restoration
    initial_rows = database.get_all_opportunities()
    initial_ids = {r["id"] for r in initial_rows}
    print(f"[Initial State] Preserving {len(initial_ids)} existing database records: {initial_ids}")

    # -----------------------------------------------------------------
    # SECTION 1: STREAMLIT APPTEST / UI TESTS
    # -----------------------------------------------------------------
    print("\n>>> SECTION 1: STREAMLIT APPTEST / UI TESTS <<<")

    # 1.1 Application Startup Test
    print("\n--- UI Test 1.1: Application Startup ---")
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()

    assert len(at.exception) == 0, f"Startup failed with exceptions: {at.exception}"
    assert len(at.title) > 0 and "Student Opportunity Board" in at.title[0].value
    print("  [PASS] App title correctly rendered: 'Student Opportunity Board'")

    assert len(at.tabs) == 2, f"Expected 2 tabs, found {len(at.tabs)}"
    print("  [PASS] Navigation tabs rendered ('View Opportunities' & 'Add Opportunity')")

    if len(initial_rows) == 0:
        assert len(at.info) > 0, "Expected empty state info message"
        print(f"  [PASS] Empty state info callout displayed: '{at.info[0].value}'")
    else:
        print(f"  [PASS] Existing records loaded into UI ({len(initial_rows)} record(s) active)")

    # 1.2 Form Validation Test (Empty Submission)
    print("\n--- UI Test 1.2: Add Opportunity Form Validation ---")
    save_btn = [b for b in at.button if b.label == "Save Opportunity"][0]
    save_btn.click().run()
    assert len(at.error) > 0, "Validation error was not displayed for empty required fields"
    print(f"  [PASS] Required fields enforced on empty submission: '{at.error[0].value}'")

    # 1.3 Adding Opportunities via Form
    print("\n--- UI Test 1.3: Adding Opportunities via Form ---")
    # Add 'TEST Opportunity A'
    add_title = [t for t in at.text_input if t.label == "Title *"][-1]
    add_org = [t for t in at.text_input if t.label == "Organization *"][-1]
    add_cat = [s for s in at.selectbox if s.label == "Category"][-1]
    add_priority = [s for s in at.selectbox if s.label == "Priority"][-1]
    add_status = [s for s in at.selectbox if s.label == "Status"][-1]
    add_deadline = [d for d in at.date_input if d.label == "Deadline"][-1]
    add_link = [t for t in at.text_input if t.label == "Link"][-1]
    add_notes = [t for t in at.text_area if t.label == "Notes"][-1]

    add_title.input("TEST Opportunity A").run()
    add_org.input("Acme University").run()
    add_cat.select("Internship").run()
    add_priority.select("High").run()
    add_status.select("Applied").run()
    add_deadline.set_value(datetime.date(2026, 10, 15)).run()
    add_link.input("https://example.com/opp-a").run()
    add_notes.input("Notes for Opp A: High priority backend role").run()

    save_btn = [b for b in at.button if b.label == "Save Opportunity"][0]
    save_btn.click().run()
    assert len(at.success) > 0 and "saved successfully" in at.success[0].value
    print("  [PASS] 'TEST Opportunity A' created and saved via UI form")

    # Add 'TEST Opportunity B'
    add_title = [t for t in at.text_input if t.label == "Title *"][-1]
    add_org = [t for t in at.text_input if t.label == "Organization *"][-1]
    add_cat = [s for s in at.selectbox if s.label == "Category"][-1]
    add_priority = [s for s in at.selectbox if s.label == "Priority"][-1]
    add_status = [s for s in at.selectbox if s.label == "Status"][-1]
    add_deadline = [d for d in at.date_input if d.label == "Deadline"][-1]
    add_link = [t for t in at.text_input if t.label == "Link"][-1]
    add_notes = [t for t in at.text_area if t.label == "Notes"][-1]

    add_title.input("TEST Opportunity B").run()
    add_org.input("Global Hackathon Org").run()
    add_cat.select("Hackathon").run()
    add_priority.select("Medium").run()
    add_status.select("Saved").run()
    add_deadline.set_value(datetime.date(2026, 11, 20)).run()
    add_link.input("https://example.com/opp-b").run()
    add_notes.input("Notes for Opp B: 48h AI hackathon").run()

    save_btn = [b for b in at.button if b.label == "Save Opportunity"][0]
    save_btn.click().run()
    print("  [PASS] 'TEST Opportunity B' created and saved via UI form")

    # Verify both records saved in database
    db_records = database.get_all_opportunities()
    id_a = [r["id"] for r in db_records if r["title"] == "TEST Opportunity A"][0]
    id_b = [r["id"] for r in db_records if r["title"] == "TEST Opportunity B"][0]
    print(f"  [PASS] Verified in database: ID {id_a} ('TEST Opportunity A'), ID {id_b} ('TEST Opportunity B')")

    # 1.4 Edit Opportunity UI Test
    print("\n--- UI Test 1.4: Edit Opportunity & ID Preservation ---")
    at.run()
    manage_sb = [sb for sb in at.selectbox if sb.key == "manage_select"][0]
    label_a = [opt for opt in manage_sb.options if f"#{id_a}" in opt][0]
    manage_sb.select(label_a).run()

    # Verify edit form pre-population
    edit_title_input = [ti for ti in at.text_input if ti.label == "Title *" and ti.value == "TEST Opportunity A"][0]
    print(f"  [PASS] Edit form successfully pre-populated with: '{edit_title_input.value}'")

    # Edit fields
    edit_title_input.input("TEST Opportunity A Updated").run()
    edit_org_input = [ti for ti in at.text_input if ti.label == "Organization *" and ti.value == "Acme University"][0]
    edit_org_input.input("Acme University Updated").run()

    edit_cat_sb = [sb for sb in at.selectbox if sb.label == "Category" and sb.value == "Internship"][0]
    edit_cat_sb.select("Course").run()

    edit_stat_sb = [sb for sb in at.selectbox if sb.label == "Status" and sb.value == "Applied"][0]
    edit_stat_sb.select("Interviewing").run()

    edit_pri_sb = [sb for sb in at.selectbox if sb.label == "Priority" and sb.value == "High"][0]
    edit_pri_sb.select("Low").run()

    edit_date_in = [di for di in at.date_input if di.label == "Deadline" and di.value == datetime.date(2026, 10, 15)][0]
    edit_date_in.set_value(datetime.date(2026, 10, 30)).run()

    edit_link_in = [ti for ti in at.text_input if ti.label == "Link" and ti.value == "https://example.com/opp-a"][0]
    edit_link_in.input("https://example.com/opp-a-updated").run()

    edit_notes_ta = [ta for ta in at.text_area if ta.label == "Notes" and "Notes for Opp A" in ta.value][0]
    edit_notes_ta.input("Updated notes for Opp A").run()

    # Save changes
    save_changes_btn = [btn for btn in at.button if btn.label == "Save Changes"][0]
    save_changes_btn.click().run()

    # Verify update in database
    updated_opp_a = database.get_opportunity_by_id(id_a)
    assert updated_opp_a["title"] == "TEST Opportunity A Updated"
    assert updated_opp_a["organization"] == "Acme University Updated"
    assert updated_opp_a["category"] == "Course"
    assert updated_opp_a["status"] == "Interviewing"
    assert updated_opp_a["priority"] == "Low"
    assert updated_opp_a["deadline"] == "2026-10-30"
    assert updated_opp_a["link"] == "https://example.com/opp-a-updated"
    assert updated_opp_a["notes"] == "Updated notes for Opp A"
    assert updated_opp_a["id"] == id_a, "Opportunity ID changed unexpectedly during edit!"

    # Verify duplicate prevention
    all_curr = database.get_all_opportunities()
    assert len(all_curr) == len(initial_ids) + 2, "Duplicate records were created during edit!"
    print("  [PASS] Edit verified: Values updated in place, ID preserved, no duplicates created")

    # 1.5 Delete Opportunity & Confirmation Protection UI Test
    print("\n--- UI Test 1.5: Delete Opportunity & Confirmation Protection ---")
    at.run()
    manage_sb = [sb for sb in at.selectbox if sb.key == "manage_select"][0]
    label_b = [opt for opt in manage_sb.options if f"#{id_b}" in opt][0]
    manage_sb.select(label_b).run()

    # Check delete warning text
    warning = [w for w in at.warning if f"#{id_b}" in w.value][0]
    print(f"  [PASS] Delete warning identifies target: '{warning.value}'")

    # Verify button is disabled before checkbox is checked
    confirm_cb = [cb for cb in at.checkbox if cb.key == f"confirm_delete_{id_b}"][0]
    del_btn = [btn for btn in at.button if btn.key == f"delete_btn_{id_b}"][0]
    assert confirm_cb.value is False, "Confirmation checkbox should default to unchecked"
    assert del_btn.disabled is True, "Permanently Delete button should be disabled when unchecked"
    print("  [PASS] Delete button is disabled while confirmation checkbox is unchecked")

    # Check confirmation checkbox and verify button is enabled
    confirm_cb.check().run()
    del_btn = [btn for btn in at.button if btn.key == f"delete_btn_{id_b}"][0]
    assert del_btn.disabled is False, "Permanently Delete button should become enabled when checked"
    print("  [PASS] Delete button became enabled after checking confirmation checkbox")

    # Click Permanently Delete
    del_btn.click().run()

    # Verify deletion in database
    assert database.get_opportunity_by_id(id_b) is None, "Opp B was not deleted from database"
    assert database.get_opportunity_by_id(id_a) is not None, "Opp A was deleted accidentally!"
    print(f"  [PASS] Opp B successfully deleted; Opp A (ID {id_a}) remained intact")

    # -----------------------------------------------------------------
    # SECTION 2: DATABASE-LEVEL FILTER TESTS
    # Note: These tests directly evaluate SQL search and filtering logic
    # in database.py without end-to-end browser DOM interaction.
    # -----------------------------------------------------------------
    print("\n>>> SECTION 2: DATABASE-LEVEL FILTER TESTS <<<")

    # 2.1 Search Query Filtering
    print("\n--- DB Filter Test 2.1: Keyword Search Queries ---")
    res_exact = database.get_all_opportunities(search_query="TEST Opportunity A Updated")
    assert any(r["id"] == id_a for r in res_exact)
    print("  [PASS] Exact title query matched test record")

    res_partial = database.get_all_opportunities(search_query="Updated")
    assert any(r["id"] == id_a for r in res_partial)
    print("  [PASS] Partial keyword query ('Updated') matched test record")

    res_org = database.get_all_opportunities(search_query="Acme")
    assert any(r["id"] == id_a for r in res_org)
    print("  [PASS] Organization keyword query ('Acme') matched test record")

    res_none = database.get_all_opportunities(search_query="__NonExistentQueryXYZ123__")
    assert len(res_none) == 0
    print("  [PASS] Non-matching query returned 0 records")

    # 2.2 Category Filtering
    print("\n--- DB Filter Test 2.2: Category Filtering ---")
    res_cat_match = database.get_all_opportunities(category_filter="Course")
    assert any(r["id"] == id_a for r in res_cat_match)
    print("  [PASS] Matching category ('Course') returned test record")

    res_cat_mismatch = database.get_all_opportunities(category_filter="Scholarship")
    assert not any(r["id"] == id_a for r in res_cat_mismatch)
    print("  [PASS] Non-matching category ('Scholarship') excluded test record")

    res_cat_all = database.get_all_opportunities(category_filter="All")
    assert any(r["id"] == id_a for r in res_cat_all)
    print("  [PASS] Category filter 'All' returned all active records")

    # 2.3 Status Filtering
    print("\n--- DB Filter Test 2.3: Status Filtering ---")
    res_stat_match = database.get_all_opportunities(status_filter="Interviewing")
    assert any(r["id"] == id_a for r in res_stat_match)
    print("  [PASS] Matching status ('Interviewing') returned test record")

    res_stat_mismatch = database.get_all_opportunities(status_filter="Rejected")
    assert not any(r["id"] == id_a for r in res_stat_mismatch)
    print("  [PASS] Non-matching status ('Rejected') excluded test record")

    res_stat_all = database.get_all_opportunities(status_filter="All")
    assert any(r["id"] == id_a for r in res_stat_all)
    print("  [PASS] Status filter 'All' returned all active records")

    # 2.4 Priority Filtering
    print("\n--- DB Filter Test 2.4: Priority Filtering ---")
    # Opp A was updated to priority="Low"
    res_pri_low = database.get_all_opportunities(priority_filter="Low")
    assert any(r["id"] == id_a for r in res_pri_low)
    print("  [PASS] Matching priority ('Low') returned test record Opp A")

    res_pri_high = database.get_all_opportunities(priority_filter="High")
    assert not any(r["id"] == id_a for r in res_pri_high)
    print("  [PASS] Non-matching priority ('High') excluded test record Opp A")

    res_pri_med = database.get_all_opportunities(priority_filter="Medium")
    assert not any(r["id"] == id_a for r in res_pri_med)
    print("  [PASS] Non-matching priority ('Medium') excluded test record Opp A")

    # Add temporary records to verify Medium and High priority filtering explicitly
    temp_med_id = database.add_opportunity(
        title="TEST Priority Med Record",
        organization="Priority Org Med",
        category="Internship",
        status="Saved",
        priority="Medium"
    )
    temp_high_id = database.add_opportunity(
        title="TEST Priority High Record",
        organization="Priority Org High",
        category="Hackathon",
        status="Accepted",
        priority="High"
    )

    try:
        # a. filtering by High
        res_high_match = database.get_all_opportunities(priority_filter="High")
        assert any(r["id"] == temp_high_id for r in res_high_match)
        assert not any(r["id"] == temp_med_id for r in res_high_match)
        assert not any(r["id"] == id_a for r in res_high_match)
        print("  [PASS] Filtering by High returns High record and excludes Medium/Low")

        # b. filtering by Medium
        res_med_match = database.get_all_opportunities(priority_filter="Medium")
        assert any(r["id"] == temp_med_id for r in res_med_match)
        assert not any(r["id"] == temp_high_id for r in res_med_match)
        assert not any(r["id"] == id_a for r in res_med_match)
        print("  [PASS] Filtering by Medium returns Medium record and excludes High/Low")

        # c. filtering by Low
        res_low_match = database.get_all_opportunities(priority_filter="Low")
        assert any(r["id"] == id_a for r in res_low_match)
        assert not any(r["id"] == temp_med_id for r in res_low_match)
        assert not any(r["id"] == temp_high_id for r in res_low_match)
        print("  [PASS] Filtering by Low returns Low record and excludes High/Medium")

        # d. no priority filter / 'All' preserves existing behavior
        res_pri_none = database.get_all_opportunities(priority_filter=None)
        res_pri_all = database.get_all_opportunities(priority_filter="All")
        assert any(r["id"] == id_a for r in res_pri_none)
        assert any(r["id"] == temp_med_id for r in res_pri_none)
        assert any(r["id"] == temp_high_id for r in res_pri_none)
        assert len(res_pri_none) == len(res_pri_all)
        print("  [PASS] No priority filter / 'All' preserves all records")

        # e. priority filtering works together with category, status, and search
        res_comb_pri_cat = database.get_all_opportunities(priority_filter="High", category_filter="Hackathon")
        assert any(r["id"] == temp_high_id for r in res_comb_pri_cat)
        assert not any(r["id"] == temp_med_id for r in res_comb_pri_cat)

        res_comb_pri_stat = database.get_all_opportunities(priority_filter="High", status_filter="Accepted")
        assert any(r["id"] == temp_high_id for r in res_comb_pri_stat)
        assert not any(r["id"] == temp_med_id for r in res_comb_pri_stat)

        res_comb_pri_search = database.get_all_opportunities(priority_filter="Medium", search_query="Priority Org Med")
        assert any(r["id"] == temp_med_id for r in res_comb_pri_search)
        assert not any(r["id"] == temp_high_id for r in res_comb_pri_search)
        print("  [PASS] Priority filtering works together with category, status, and search filters")
    finally:
        database.delete_opportunity(temp_med_id)
        database.delete_opportunity(temp_high_id)

    # 2.5 Combined Search & Filtering
    print("\n--- DB Filter Test 2.5: Combined Search and Filters ---")
    res_comb_1 = database.get_all_opportunities(search_query="Updated", category_filter="Course")
    assert any(r["id"] == id_a for r in res_comb_1)
    res_comb_2 = database.get_all_opportunities(search_query="Updated", category_filter="Scholarship")
    assert not any(r["id"] == id_a for r in res_comb_2)
    print("  [PASS] Search + Category conjunction verified")

    res_comb_3 = database.get_all_opportunities(search_query="Updated", status_filter="Interviewing")
    assert any(r["id"] == id_a for r in res_comb_3)
    res_comb_4 = database.get_all_opportunities(search_query="Updated", status_filter="Rejected")
    assert not any(r["id"] == id_a for r in res_comb_4)
    print("  [PASS] Search + Status conjunction verified")

    # -----------------------------------------------------------------
    # SECTION 3: CLEANUP & DATA INTEGRITY TESTS
    # -----------------------------------------------------------------
    print("\n>>> SECTION 3: CLEANUP & DATA INTEGRITY TESTS <<<")

    # Remove remaining test record Opp A
    deleted_a = database.delete_opportunity(id_a)
    assert deleted_a is True, "Failed to delete remaining test record Opp A"

    final_records = database.get_all_opportunities()
    final_ids = {r["id"] for r in final_records}
    assert final_ids == initial_ids, f"Database not restored to original state! Expected: {initial_ids}, Found: {final_ids}"
    print(f"  [PASS] Test record ID {id_a} deleted successfully")
    print(f"  [PASS] Database verified restored to its original state ({len(final_ids)} pre-existing records intact)")

    print("\n================================================================")
    print("ALL TESTS PASSED SUCCESSFULLY! (UI + DB + CLEANUP)")
    print("================================================================")


if __name__ == "__main__":
    run_tests()
