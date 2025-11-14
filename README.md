
# EduApp (AI-Enhanced Translation Lab) — Starter Kit

A lightweight Streamlit app to support AI-enhanced translation teaching:
- **MT Lab:** run machine translations (via placeholders), compare Human vs MT vs Post-edit.
- **Prompt Lab:** experiment with prompts, constraints, and terminology.
- **MQM Annotation:** label errors with a simple MQM schema.
- **Dashboard:** visualize basic metrics and track assignments.
- **Admin:** upload corpora, manage class rosters, export grades.

> This is a *teaching scaffold*. You can plug in real APIs (OpenAI, DeepL) and proper metrics (COMET, sacreBLEU) later.

## Quick Start
```bash
pip install -r requirements.txt
streamlit run Home.py
```
(Or deploy on Streamlit Community Cloud / campus Docker.)

## Structure
- `Home.py` — landing + navigation
- `pages/1_MT_Lab.py` — Human vs MT vs Post-edit experiment
- `pages/2_Prompt_Lab.py` — prompt engineering exercises
- `pages/3_Annotation_MQM.py` — MQM error labeling
- `pages/4_Dashboard.py` — class dashboard & exports
- `pages/5_Admin.py` — dataset uploads, rosters
- `utils.py` — helper functions & minimal metrics
- `data/sample_pairs.csv` — toy parallel set (EN↔AR)

## Next Steps
- Replace `fake_mt()` with real API calls.
- Swap the toy metrics with COMET/MQM pipelines.
- Connect to your LMS via LTI or export gradebook CSV.
- Add authentication (e.g., Streamlit Secrets + JWT).

## Notes for Arabic
- Use `st.markdown("<div dir='rtl'>النص العربي</div>", unsafe_allow_html=True)` to display RTL.
- Ensure fonts support Arabic in PDF exports.
