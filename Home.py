# Home.py
import pathlib, streamlit as st

st.set_page_config(page_title="EduApp — AI Translation Lab", layout="wide")

st.title("EduApp — AI Translation Lab")
st.caption("Minor in Translation & AI — Human–Machine collaboration, post-editing, and evaluation")

# Keep the role available across all pages in this Streamlit session.
role = st.radio(
    "I am using the lab as:",
    ["Student", "Instructor"],
    horizontal=True,
    key="user_role",
)

if role == "Instructor":
    st.success("Instructor mode enabled. You can manage tickets, review progress, and export research data.")
else:
    st.info("Student mode enabled. Use the labs to complete translation and post-editing tasks.")

st.markdown("""
**What do you want to do today?**  
- **Health Check** (first, please)  
- **MT Lab**: Compare human translation, raw MT, and your post-editing.  
- **Prompt Lab**: Design prompts, control style/terminology, and test outputs.  
- **MQM Annotation**: Label translation errors and compute scores.  
- **Dashboard**: Track class progress and export grades.  
- **Admin**: Upload corpora and manage rosters.
""")

st.divider()
st.subheader("Jump straight in")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/0_Health_Check.py", label="🩺 Health Check")
    st.page_link("pages/MT_Lab.py", label="🔁 MT Lab")
with col2:
    st.page_link("pages/Prompt_Lab.py", label="🧭 Prompt Lab")
    st.page_link("pages/MQM_Annotation.py", label="📝 MQM Annotation")
with col3:
    if role == "Instructor":
        st.page_link("pages/Dashboard.py", label="📊 Instructor Dashboard")
        st.page_link("pages/Admin.py", label="🛠️ Instructor Admin")
    else:
        st.page_link("pages/Dashboard.py", label="📊 Dashboard")
        st.caption("Instructor tools are available in Instructor mode.")

pathlib.Path("data").mkdir(parents=True, exist_ok=True)
