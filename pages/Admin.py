import os, io
import pandas as pd
import streamlit as st

try:
    from utils_mt import (
        ensure_sample_pairs, load_pairs,
        ensure_tickets_file, load_tickets, save_tickets, add_ticket
    )
except Exception as e:
    st.error("Could not import from utils_mt. Make sure 'utils_mt.py' exists at the repo root and contains the required functions.")
    st.exception(e)
    st.stop()

st.title("Instructor Task Management")
st.caption("Create, assign, monitor, and export student post-editing tasks.")

if st.session_state.get("user_role") != "Instructor":
    st.warning("Select **Instructor** on the home page to access task management.")
    st.stop()

# ---------- Sample pairs ----------
st.subheader("Sample Pairs (for MT Lab demo)")
colA, colB = st.columns([1, 1])
with colA:
    if st.button("Create/Reset sample_pairs.csv"):
        ensure_sample_pairs()
        st.success("Created data/sample_pairs.csv ✅")
with colB:
    if os.path.exists("data/sample_pairs.csv"):
        buf = io.BytesIO(open("data/sample_pairs.csv", "rb").read())
        st.download_button("⬇️ Download sample_pairs.csv", buf, file_name="sample_pairs.csv", mime="text/csv")
    else:
        st.info("sample_pairs.csv not found yet.")

st.divider()

# ---------- Create student task ----------
st.subheader("Create a student task")
st.info("Students will see open tasks in MT Lab. Leave the username blank to let any student claim the task.")

with st.form("create_task_form", clear_on_submit=True):
    c1, c2 = st.columns([2, 1])
    with c1:
        ticket_id = st.text_input("Task ID", placeholder="Example: T001")
    with c2:
        points = st.number_input("Points", min_value=0, max_value=100, value=5, step=1)

    src_lang = st.selectbox("Source language", ["en", "ar"], index=0)
    tgt_lang = st.selectbox("Target language", ["ar", "en"], index=0)
    due_date = st.text_input("Due date (YYYY-MM-DD)", placeholder="Example: 2026-11-15")
    assigned_to = st.text_input("Assign to a student username (optional)", placeholder="Leave blank for open claim")

    source = st.text_area("Source text", height=140, placeholder="Paste the source text students will translate or post-edit.")
    reference = st.text_area("Reference translation (optional)", height=120, placeholder="Add a reference for scoring and research comparison.")

    submitted = st.form_submit_button("Create task")

    if submitted:
        if not ticket_id.strip() or not source.strip():
            st.error("Task ID and source text are required.")
        else:
            existing = load_tickets()
            if ticket_id.strip() in existing["ticket_id"].astype(str).tolist():
                st.error("That task ID already exists. Please use a unique ID.")
            else:
                add_ticket(
                    ticket_id=ticket_id.strip(),
                    source=source.strip(),
                    reference=reference.strip(),
                    src_lang=src_lang,
                    tgt_lang=tgt_lang,
                    assigned_to=assigned_to.strip(),
                    due_date=due_date.strip(),
                    status="open",
                    points=int(points),
                )
                st.success(f"Task {ticket_id.strip()} was created for students.")

st.divider()

# ---------- Task list and bulk upload ----------
st.subheader("Current student tasks")
ensure_tickets_file()
tix = load_tickets()
st.dataframe(tix, use_container_width=True, height=260)

st.markdown("### Upload many tasks (optional)")
up = st.file_uploader("Upload tickets.csv", type=["csv"])
if up:
    os.makedirs("data", exist_ok=True)
    with open("data/tickets.csv", "wb") as w:
        w.write(up.getvalue())
    st.success("Uploaded tasks to data/tickets.csv")

if os.path.exists("data/tickets.csv"):
    buf = io.BytesIO(open("data/tickets.csv", "rb").read())
    st.download_button("⬇️ Download tickets.csv", buf, file_name="tickets.csv", mime="text/csv")

st.divider()

# ---------- Research export ----------
st.subheader("Research exports")
if os.path.exists("data/results.csv"):
    res_buf = io.BytesIO(open("data/results.csv", "rb").read())
    st.download_button(
        "⬇️ Download results.csv (edits, scores, metadata)",
        res_buf,
        file_name="results.csv",
        mime="text/csv",
    )
else:
    st.info("No results yet. Students must submit from MT Lab to generate results.csv.")
