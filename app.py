import streamlit as st
import matplotlib.pyplot as plt
import re
import fitz  # PyMuPDF

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------- UI STYLE ----------
st.markdown("""
<style>
.big-font {
    font-size:22px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 AI Resume Analyzer")
st.markdown('<p class="big-font">AI Powered Resume Screening & ATS Match System</p>', unsafe_allow_html=True)

# ---------- Load Skills ----------
with open("skills.txt", "r") as f:
    skills_list = [line.strip().lower() for line in f]

# ---------- Extract Text from PDF ----------
def get_resume_text(file):
    text = ""
    try:
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    except:
        text = ""
    return text.lower()

# ---------- Extract Skills ----------
def extract_skills(text):
    text = text.lower().replace("-", " ").replace("\n", " ")
    found = []
    for skill in skills_list:
        if skill in text:
            found.append(skill)
    return list(set(found))

# ---------- Upload / Paste ----------
st.write("Upload resume OR paste resume text manually")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
manual_text = st.text_area("OR Paste Resume Text Here")

job_description = st.text_area("Paste Job Description")

resume_text = ""

if uploaded_file:
    resume_text = get_resume_text(uploaded_file)

if manual_text:
    resume_text = manual_text.lower()

# ---------- Debug Resume Text ----------
if resume_text:
    with st.expander("🔍 Extracted Resume Text (Debug)"):
        st.write(resume_text[:1000])

# ---------- Skill Detection ----------
if resume_text:
    resume_skills = extract_skills(resume_text)

    st.subheader("🧠 Skills Detected")
    st.write(resume_skills)

    # ---------- Skill Graph ----------
    if resume_skills:
        fig, ax = plt.subplots()
        ax.barh(resume_skills, [1]*len(resume_skills))
        ax.set_title("Skills Visualization")
        st.pyplot(fig)

    # ---------- Match Score ----------
    if job_description:
        jd_skills = extract_skills(job_description.lower())
        match = len(set(resume_skills) & set(jd_skills))
        score = (match / len(jd_skills))*100 if jd_skills else 0

        st.subheader("🎯 Resume Match Score")
        st.progress(int(score))
        st.metric("Match Percentage", f"{score:.2f}%")

        # ---------- Missing Skills ----------
        missing = list(set(jd_skills) - set(resume_skills))

        st.subheader("❌ Missing Skills (Improve Resume)")
        if missing:
            st.write(missing)
        else:
            st.success("No missing skills. Great match!")

        # ---------- Result ----------
        if score >= 75:
            st.success("Excellent Match 🚀")
        elif score >= 50:
            st.warning("Moderate Match 👍")
        else:
            st.error("Low Match ❌")
