# pages/MT_Lab.py
import os, time
import pandas as pd
import streamlit as st
from utils_mt import (
    ensure_sample_pairs, load_pairs, mt_openai,
    ensure_tickets_file, load_tickets, save_tickets, append_result
)
from metrics import score_all

st.title("MT Lab — OpenAI Translation")
st.caption("Work on a dataset item or a ticket, translate with OpenAI, post-edit, and save results for research.")

# Identity (simple — username only)
student = st.text_input("Your username (e.g., student_id or email alias)", key="student")
if not student:
    st.info("Enter your username to enable saving results.")
else:
    st.success(f"Hi {student} — your submissions will be saved.")

# Choose mode
mode = st.radio("Mode", ["Pairs dataset", "My ticket"], horizontal=True)

# ---------- Pairs dataset mode ----------
if mode == "Pairs dataset":
    ensure_sample_pairs()
    pairs = load_pairs()
    if pairs.empty:
        st.info("Go to **Admin** to create or upload data.")
        st.stop()

    row = st.selectbox("Choose a sentence", pairs.to_dict("records"),
                       format_func=lambda r: f"{r['id']}: {r['source'][:80]}")

    c1, c2 = st.columns(2)
    with c1: st.subheader("Source"); st.write(row["source"])
    with c2: st.subheader("Reference (Human)"); st.write(row["reference"])

    st.markdown("### Translate with OpenAI")
    terms = st.text_input("Terminology (optional, e.g., policy=سياسة, ministry=الوزارة)", "")
    sys = st.text_area("System prompt (optional)",
        "You are a professional Arabic↔English translator. Preserve meaning and tone.")

    if st.button("Translate"):
        out = mt_openai(row["source"], system_prompt=sys, terms=terms)
        st.session_state["mt_out"] = out

    mt_text = st.text_area("MT Output", value=st.session_state.get("mt_out",""), height=140)
    pe_text = st.text_area("Your Post-edit", value="", height=140,
                           placeholder="Improve the MT output here...")

    colS1, colS2 = st.columns([1,1])
    with colS1:
        if st.button("Score vs Reference"):
            cand = pe_text.strip() or mt_text.strip()
            if not cand:
                st.warning("Nothing to score yet — generate MT or paste your text.")
            else:
                s = score_all(cand, row["reference"])
                st.success("Scores"); st.write({k: round(v,3) if isinstance(v,float) else v for k,v in s.items()})
                st.session_state["last_scores"] = s
    with colS2:
        if st.button("Submit & Save"):
            cand = pe_text.strip() or mt_text.strip()
            if not cand:
                st.warning("Nothing to save — translate or paste text first.")
            else:
                scores = st.session_state.get("last_scores", {})
                append_result({
                    "timestamp": int(time.time()),
                    "student": student or "",
                    "mode": "pairs",
                    "item_id": row.get("id",""),
                    "source": row["source"],
                    "reference": row["reference"],
                    "mt_output": st.session_state.get("mt_out",""),
                    "post_edit": cand,
                    "terms": terms,
                    "system_prompt": sys,
                    **{f"metric_{k}": v for k,v in scores.items()}
                })
                st.success("Saved to data/results.csv ✅")

# ---------- Ticket mode ----------
else:
    ensure_tickets_file()
    tix = load_tickets()

    # Show my tickets (assigned to me or open to claim)
    mine = tix[(tix["assigned_to"].fillna("")==student) & (tix["status"].isin(["open","claimed"]))]
    open_tix = tix[(tix["assigned_to"].isna()) | (tix["assigned_to"]=="")]

    st.markdown("### My tickets")
    st.dataframe(mine, use_container_width=True, height=180)

    st.markdown("### Claim an open ticket")
    if not open_tix.empty:
        to_claim = st.selectbox("Unassigned tickets", open_tix["ticket_id"].tolist())
        if st.button("Claim selected"):
            tix.loc[tix["ticket_id"]==to_claim, ["assigned_to","status"]] = [student, "claimed"]
            save_tickets(tix); st.success(f"Claimed {to_claim}. Reload to see it under My tickets.")
    else:
        st.info("No unassigned tickets.")

    st.markdown("### Work on a ticket")
    my_ids = mine["ticket_id"].tolist()
    if my_ids:
        choose = st.selectbox("Choose ticket", my_ids)
        row = tix[tix["ticket_id"]==choose].iloc[0]
        source = row["source"]; reference = row.get("reference","")
        c1, c2 = st.columns(2)
        with c1: st.subheader("Source"); st.write(source)
        with c2: st.subheader("Reference (if provided)"); st.write(reference or "—")

        terms = st.text_input("Terminology (optional)", "")
        sys = st.text_area("System prompt (optional)",
            "You are a professional Arabic↔English translator. Preserve meaning and tone.")

        if st.button("Translate"):
            out = mt_openai(source, system_prompt=sys, terms=terms)
            st.session_state["mt_out_tix"] = out

        mt_text = st.text_area("MT Output", value=st.session_state.get("mt_out_tix",""), height=140)
        pe_text = st.text_area("Your Post-edit", value="", height=140)

        colTS1, colTS2 = st.columns([1,1])
        with colTS1:
            if st.button("Score vs Reference (if available)"):
                if not reference.strip():
                    st.info("No reference set for this ticket.")
                else:
                    cand = pe_text.strip() or mt_text.strip()
                    if not cand:
                        st.warning("Nothing to score yet.")
                    else:
                        s = score_all(cand, reference)
                        st.success("Scores"); st.write({k: round(v,3) if isinstance(v,float) else v for k,v in s.items()})
                        st.session_state["last_scores_tix"] = s
        with colTS2:
            if st.button("Submit & Save ticket"):
                cand = pe_text.strip() or mt_text.strip()
                if not cand:
                    st.warning("Nothing to save — translate first.")
                else:
                    scores = st.session_state.get("last_scores_tix", {})
                    append_result({
                        "timestamp": int(time.time()),
                        "student": student or "",
                        "mode": "ticket",
                        "ticket_id": row["ticket_id"],
                        "source": source,
                        "reference": reference,
                        "mt_output": st.session_state.get("mt_out_tix",""),
                        "post_edit": cand,
                        "terms": terms,
                        "system_prompt": sys,
                        **{f"metric_{k}": v for k,v in scores.items()}
                    })
                    # mark submitted
                    tix.loc[tix["ticket_id"]==row["ticket_id"], "status"] = "submitted"
                    save_tickets(tix)
                    st.success("Saved to data/results.csv and marked ticket submitted ✅")
    else:
        st.info("No tickets assigned to you yet. Ask instructor to assign or let you claim one.")
