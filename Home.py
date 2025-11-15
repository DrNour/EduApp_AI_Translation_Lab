
import streamlit as st

st.set_page_config(page_title="EduApp — AI Translation Lab", layout="wide")

st.title("EduApp — AI Translation Lab")
st.caption("Minor in Translation & AI — Human–Machine collaboration, post-editing, and evaluation")

st.markdown("""
**What do you want to do today?**  
- **MT Lab:** Compare human translation, raw MT, and your post-editing.  
- **Prompt Lab:** Design prompts, control style/terminology, and test outputs.  
- **MQM Annotation:** Label translation errors and compute scores.  
- **Dashboard:** Track class progress and export grades.  
- **Admin:** Upload corpora and manage rosters.
""")
st.divider()
st.markdown("**Tip:** Switch pages from the sidebar ➜")
st.divider()
st.subheader("Jump straight in")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/MT_Lab.py", label="🔁 MT Lab")
    st.page_link("pages/Prompt_Lab.py", label="🧭 Prompt Lab")
with col2:
    st.page_link("pages/MQM_Annotation.py", label="📝 MQM Annotation")
    st.page_link("pages/Dashboard.py", label="📊 Dashboard")
with col3:
    st.page_link("pages/Admin.py", label="🛠️ Admin")

