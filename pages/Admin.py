# pages/Admin.py
import os, io
import pandas as pd
import streamlit as st

# Robust import with a helpful error if it fails
try:
    from utils_mt import (
        ensure_sample_pairs, load_pairs,
        ensure_tickets_file, load_tickets, save_tickets, add_ticket
    )
except Exception as e:
    st.error("Could not import from utils_mt. Make sure 'utils_mt.py' exists at the repo root and contains the required functions.")
    st.exception(e)
    st.stop()

st.title("Admin")
st.caption("Create data, paste tickets, assign students, and download CSVs for research.")

# ---------- Sample pairs ----------
st.subheader("Sample Pairs (for MT Lab demo)")
colA, colB = st.columns([1,1])
with colA:
    if st.button("Create/Reset sample_pairs.csv"):
        ensure_sample_pairs()
        st.success("Created data/sample_pairs.csv ✅")
with colB:
    if os.path.exists("data/sample_pairs.csv"):
        buf = io.BytesIO(open("data/sample_pairs.csv","rb").read())
        st.download_button("⬇️ Download sample_pairs.csv", buf, file_name="sample_pairs.csv", mime="text/csv")
    else:
        st.info("sample_pairs.csv not found yet.")

st.divider()

# ---------- Tickets: paste or upload ----------
st.subheader("Tickets (assignments)")
ensure_tickets_file()
tix = load_tickets()
st.dataframe(tix, use_container_width=True, height=240)

st.markdown("### Add a single ticket (paste text)")
with st.form("add_ticket_form", clear_on_submit=True):
    c1, c2 = st.columns([2,1])
    with c1:
        ticket_id = st.text_input("Ticket ID (e.g., T001)", "")
    with c2:
        points = st.number_input("Points", min_value=0, max_value=100, value=5, step=1)

    src_lang = st.selectbox("Source language", ["en","ar"], index=0)
    tgt_lang = st.selectbox("Target language", ["ar","en"], index=0 if src_lang=="en" else 1)
    due_date = st.text_input("Due date (YYYY-MM-DD)", "")
    assigned_to = st.text_input("Assign to (optional username)", "")

    source = st.text_area("Source text", "", height=100, placeholder="Paste the source here…")
    reference = st.text_area("Reference (optional, human translation)", "", height=100)

    submitted = st.form_submit_button("Add ticket")
    if submitted:
        if not ticket_id or not source.strip():
            st.error("Ticket ID and Source are required.")
        else:
            add_ticket(ticket_id=ticket_id.strip(), source=source.strip(), reference=reference.strip(),
                       src_lang=src_lang, tgt_lang=tgt_lang, assigned_to=assigned_to.strip(),
                       due_date=due_date.strip(), status="open", points=int(points))
            st.success(f"Added ticket {ticket_id}")

st.markdown("### Upload many tickets (optional)")
up = st.file_uploader("Upload tickets.csv", type=["csv"])
if up:
    os.makedirs("data", exist_ok=True)
    with open("data/tickets.csv","wb") as w:
        w.write(up.getvalue())
    st.success("Uploaded to data/tickets.csv")

# Download current tickets
if os.path.exists("data/tickets.csv"):
    buf = io.BytesIO(open("data/tickets.csv","rb").read())
    st.download_button("⬇️ Download tickets.csv", buf, file_name="tickets.csv", mime="text/csv")

st.divider()

# ---------- Download research data ----------
st.subheader("Research Exports")
if os.path.exists("data/results.csv"):
    res_buf = io.BytesIO(open("data/results.csv","rb").read())
    st.download_button("⬇️ Download results.csv (edits, scores, metadata)", res_buf,
                       file_name="results.csv", mime="text/csv")
else:
    st.info("No results yet. Students must submit from MT Lab to generate results.csv.")
