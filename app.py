import streamlit as st
import PyPDF2 as pdf
from openai import OpenAI
import os
from typing import Optional

# ------------------------------
# Config & Setup
# ------------------------------
st.set_page_config(page_title="Smart ATS — Groq Powered", page_icon="🧠", layout="wide")

# Load Groq API key (from secrets first, fallback to env var)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", None)
if GROQ_API_KEY is None:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ Missing Groq API Key. Add `GROQ_API_KEY` to Streamlit secrets or environment.")
    st.stop()

# Initialize Groq Client
client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

# Available Groq Models
GROQ_MODELS = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768"
]

# ------------------------------
# Helpers
# ------------------------------
def read_pdf(uploaded_file) -> str:
    """Extract text from an uploaded PDF file using PyPDF2."""
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
        return "\n".join(text).strip()
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")
        return ""


def generate_text(prompt: str, model: str, max_tokens: int = 800, temperature: float = 0.5) -> Optional[str]:
    """Call Groq LLM and return response text."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Generation error: {e}")
        return None


# ------------------------------
# UI
# ------------------------------
st.title("Smart ATS — Groq Powered 🚀")
st.caption("Resume vs Job Description analysis powered by Groq LLMs")

col_left, col_right = st.columns([1, 1])
with col_left:
    model_id = st.selectbox(
        "Choose a Groq Model",
        options=GROQ_MODELS,
        index=0,
    )
    max_new_tokens = st.slider("Max new tokens", 64, 1024, 512, step=32)
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, step=0.05)

with col_right:
    st.markdown("**Auth**")
    if GROQ_API_KEY:
        st.success("Groq API key detected")
    else:
        st.error("No Groq API key found!")

st.divider()

jd = st.text_area(
    "📌 Paste the Job Description (JD)",
    height=180,
    placeholder="Paste JD here...",
)

uploaded_file = st.file_uploader("📂 Upload your Resume (PDF)", type=["pdf"], accept_multiple_files=False)

# Extract resume text
resume_text = ""
if uploaded_file is not None:
    with st.spinner("Reading resume..."):
        resume_text = read_pdf(uploaded_file)

# Reset button
if st.button("Clear Inputs"):
    st.experimental_rerun()

st.divider()

# Tabs for different analyses
TAB_TITLES = ["Evaluation", "Improve Skills", "Missing Keywords", "Match %"]

if jd and resume_text:
    tab_eval, tab_skills, tab_keywords, tab_match = st.tabs(TAB_TITLES)

    with tab_eval:
        st.subheader("📊 HR-style Evaluation")
        prompt = f"""
You are an experienced Technical HR Manager. Review the provided resume against the job description.
Highlight strengths, weaknesses, and alignment with the specified job requirements.

### Job Description:
{jd}

### Resume:
{resume_text}

Return a structured analysis with headings for:
- Strengths
- Weaknesses
- Overall Fit
"""
        if st.button("Run Evaluation", key="btn_eval"):
            with st.spinner("Generating evaluation..."):
                output = generate_text(prompt, model_id, max_tokens=max_new_tokens, temperature=temperature)
            if output:
                st.write(output)

    with tab_skills:
        st.subheader("💡 Skill Enhancement Suggestions")
        prompt = f"""
As a Technical HR Manager with expertise in data science, analyze the resume relative to the JD.
Suggest concrete skill improvements (courses, tools, projects) and areas needing development.

### Job Description:
{jd}

### Resume:
{resume_text}

Output in bullet points grouped by:
- Hard Skills
- Soft Skills
- Projects to Build
"""
        if st.button("Suggest Improvements", key="btn_skills"):
            with st.spinner("Generating suggestions..."):
                output = generate_text(prompt, model_id, max_tokens=max_new_tokens, temperature=temperature)
            if output:
                st.write(output)

    with tab_keywords:
        st.subheader("🔑 ATS Missing Keywords")
        prompt = f"""
Act as an ATS scanner. Extract the most important keywords from the JD and identify which are missing or weak in the resume.

### Job Description:
{jd}

### Resume:
{resume_text}

Return two lists:
1. Critical Missing Keywords
2. Nice-to-have Keywords
Also include a short note on how to add them naturally.
"""
        if st.button("Find Missing Keywords", key="btn_keywords"):
            with st.spinner("Finding keywords..."):
                output = generate_text(prompt, model_id, max_tokens=max_new_tokens, temperature=temperature)
            if output:
                st.write(output)

    with tab_match:
        st.subheader("📈 Estimated Match Percentage")
        prompt = f"""
    Analyze the resume vs job description and output in this strict format:

    Match: <number>%

    ### Why this score:
    - Bullet point reason 1
    - Bullet point reason 2
    - Bullet point reason 3

    ### How to Improve:
    - Action 1
    - Action 2
    - Action 3

    ### Job Description:
    {jd}

    ### Resume:
    {resume_text}
    """
        if st.button("Compute Match %", key="btn_match"):
            with st.spinner("Scoring match..."):
                output = generate_text(prompt, model_id, max_tokens=max_new_tokens, temperature=temperature)
            if output:
                st.write(output)

                # Optional: try to extract the percentage and show a progress bar
                import re
                m = re.search(r"Match:\s*([0-9]{1,3})\s*%", output)
                if m:
                    pct = int(m.group(1))
                    pct = max(0, min(100, pct))  # clamp 0-100
                    st.metric(label="Match Percentage", value=f"{pct}%")
                    st.progress(pct)


# Footer
st.divider()
st.caption("Built with Streamlit and Groq LLMs ⚡ | By Abhishek Pandit")
