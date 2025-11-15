# pages/MT_Lab.py (add to your existing page)
import os, pandas as pd, streamlit as st
from utils_mt import ensure_sample_pairs, load_pairs, mt_openai, mt_google_translate, fake_mt

st.title("MT Lab — Human vs MT vs Post-edit")
ensure_sample_pairs()

# --- Simple identity (no auth): student enters a username
student = st.text_input("Your username (e.g., reem.ae)", key="student_name")
if not student:
    st.info("Enter your username to see your tickets.")
    st.stop()

# --- Tickets list
tickets_path = "data/tickets.csv"
if os.path.exists(tickets_path):
    tix = pd.read_csv(tickets_path)
    my_open = tix[(tix["assigned_to"].fillna("")==student) & (tix["status"].isin(["open","claimed"]))]
    st.markdown("### My tickets")
    st.dataframe(my_open)

    # Claim an unassigned ticket
    st.markdown("#### Claim a ticket")
    unassigned = tix[(tix["assigned_to"].isna()) | (tix["assigned_to"]=="")]
    pick = st.selectbox("Unassigned tickets", unassigned["ticket_id"].tolist())
    if st.button("Claim selected"):
        tix.loc[tix["ticket_id"]==pick, ["assigned_to","status"]] = [student, "claimed"]
        tix.to_csv(tickets_path, index=False)
        st.success(f"Claimed {pick} — reload to see it under My tickets")

    # Work on a ticket you own
    st.markdown("#### Work on my ticket")
    mine = my_open["ticket_id"].tolist()
    if mine:
        choose = st.selectbox("Choose ticket", mine)
        row = tix[tix["ticket_id"]==choose].iloc[0]
        source = row["source"]; reference = row.get("reference","")
        src_lang = row.get("src_lang","en"); tgt_lang = row.get("tgt_lang","ar")

        c1,c2 = st.columns(2)
        with c1: st.subheader("Source"); st.write(source)
        with c2: st.subheader("Reference (Human)"); st.write(reference)

        engine = st.radio("Engine", ["OpenAI", "Google Translate", "Demo (fake)"], horizontal=True)
        terms = st.text_input("Terminology (policy=سياسة, ministry=الوزارة)", "")
        system_prompt = st.text_area("System prompt (OpenAI only)",
            "You are a professional Arabic↔English translator. Preserve meaning and tone.")

        if st.button("Translate"):
            if engine == "OpenAI":
                out = mt_openai(source, system_prompt=system_prompt, terms=terms)
            elif engine == "Google Translate":
                tgt = "ar" if str(tgt_lang).lower().startswith("ar") else "en"
                src = "en" if str(src_lang).lower().startswith("en") else "ar"
                out = mt_google_translate(source, target_lang=tgt, source_lang=src)
            else:
                out = fake_mt(source, src_lang=src_lang, tgt_lang=tgt_lang)
            st.session_state["mt_out"] = out

        mt_text = st.text_area("MT Output", value=st.session_state.get("mt_out",""), height=150)
        pe_text = st.text_area("Your Post-edit", value="", height=150)

        if st.button("Submit"):
            # Mark submitted (you can also write to results.csv)
            tix.loc[tix["ticket_id"]==choose, "status"] = "submitted"
            tix.to_csv(tickets_path, index=False)
            st.success("Submitted. Instructor can grade from Dashboard.")
    else:
        st.info("No tickets assigned yet. Claim one above.")
else:
    st.info("No tickets.csv found. Ask your instructor to upload it in Admin.")
