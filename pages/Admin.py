# pages/Admin.py
import os, pandas as pd, streamlit as st
from utils_mt import ensure_sample_pairs

st.title("Admin")
st.caption("Create/upload datasets and assign tickets to students.")

# ---- sample_pairs.csv (for MT Lab demos)
if st.button("Create/Reset sample_pairs.csv"):
    ensure_sample_pairs()
    st.success("Created data/sample_pairs.csv ✅")

uploaded_pairs = st.file_uploader("Upload pairs CSV (id,source,reference,src_lang,tgt_lang)", type=["csv"])
if uploaded_pairs:
    os.makedirs("data", exist_ok=True)
    with open("data/sample_pairs.csv","wb") as w:
        w.write(uploaded_pairs.getvalue())
    st.success("Uploaded to data/sample_pairs.csv")

st.divider()

# ---- tickets.csv (assignment workflow)
os.makedirs("data", exist_ok=True)
tickets_path = "data/tickets.csv"

st.subheader("Tickets (assignments)")
upl_tix = st.file_uploader("Upload tickets.csv", type=["csv"], key="tickets_up")
if upl_tix:
    with open(tickets_path,"wb") as w:
        w.write(upl_tix.getvalue())
    st.success("Uploaded to data/tickets.csv")

if os.path.exists(tickets_path):
    tix = pd.read_csv(tickets_path)
    st.dataframe(tix)
    st.markdown("### Assign or reassign")
    student = st.text_input("Student username (e.g., reem.ae or student ID)")
    which = st.text_input("Ticket ID to assign (e.g., T001)")
    if st.button("Assign ticket"):
        if which in tix["ticket_id"].astype(str).values:
            tix.loc[tix["ticket_id"].astype(str)==which, ["assigned_to","status"]] = [student, "claimed"]
            tix.to_csv(tickets_path, index=False)
            st.success(f"Assigned {which} to {student}")
        else:
            st.error("Ticket ID not found")
else:
    st.info("No data/tickets.csv yet. Upload one above.")
